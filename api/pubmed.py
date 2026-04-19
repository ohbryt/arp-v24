"""
ARP v24 - PubMed + ClinicalTrials.gov Integration

Phase 5 improvements:
- Async method as primary implementation
- Safe sync wrapper (ThreadPoolExecutor for running event loops)
- Structured fetch status reporting
- Robust ClinicalTrials parsing
"""

import json
import os
import asyncio
import concurrent.futures
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class FetchStatus(Enum):
    """Structured fetch status."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    SKIPPED = "skipped"  # httpx not available


@dataclass
class PubMedArticle:
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    year: int
    mesh_terms: List[str]


@dataclass
class ClinicalTrial:
    nct_id: str
    title: str
    phase: str
    status: str
    conditions: List[str]
    interventions: List[str]
    enrollment: int


class PubMedClient:
    """NCBI E-utilities client"""
    BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("NCBI_API_KEY")

    async def search_and_fetch(self, query: str, max_results: int = 10) -> List[PubMedArticle]:
        if not HAS_HTTPX:
            return []
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"db": "pubmed", "term": query, "retmax": str(max_results),
                      "retmode": "json", "sort": "relevance"}
            if self.api_key:
                params["api_key"] = self.api_key
            try:
                r = await client.get(f"{self.BASE}/esearch.fcgi", params=params)
                r.raise_for_status()
                pmids = json.loads(r.text).get("esearchresult", {}).get("idlist", [])
                if not pmids:
                    return []
                return await self._fetch(client, pmids)
            except Exception as e:
                print(f"PubMed error: {e}")
                return []

    async def _fetch(self, client, pmids: List[str]) -> List[PubMedArticle]:
        import xml.etree.ElementTree as ET
        params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
        if self.api_key:
            params["api_key"] = self.api_key
        try:
            r = await client.get(f"{self.BASE}/efetch.fcgi", params=params)
            r.raise_for_status()
            root = ET.fromstring(r.content)
            articles = []
            for elem in root.findall(".//PubmedArticle"):
                try:
                    pmid = (elem.find(".//PMID").text or "") if elem.find(".//PMID") is not None else ""
                    title = (elem.find(".//ArticleTitle").text or "") if elem.find(".//ArticleTitle") is not None else ""
                    parts = []
                    ab = elem.find(".//Abstract")
                    if ab is not None:
                        for t in ab.findall(".//AbstractText"):
                            if t.text:
                                parts.append(t.text)
                    authors = []
                    for a in elem.findall(".//Author"):
                        ln = a.find("LastName")
                        if ln is not None and ln.text:
                            authors.append(ln.text)
                    journal = (elem.find(".//Journal/Title").text or "") if elem.find(".//Journal/Title") is not None else ""
                    year = 2024
                    ye = elem.find(".//Journal/JournalIssue/PubDate/Year")
                    if ye is not None and ye.text:
                        try: year = int(ye.text)
                        except: pass
                    mesh = [m.text for m in elem.findall(".//MeshHeading/DescriptorName") if m.text]
                    articles.append(PubMedArticle(pmid, title, " ".join(parts), authors[:5], journal, year, mesh[:10]))
                except Exception:
                    continue
            return articles
        except Exception as e:
            print(f"PubMed fetch error: {e}")
            return []


class ClinicalTrialsClient:
    """ClinicalTrials.gov API v2 - Robust parsing"""
    BASE = "https://clinicaltrials.gov/api/v2"

    async def search(self, condition: str, intervention: Optional[str] = None, max_results: int = 10) -> List[ClinicalTrial]:
        if not HAS_HTTPX:
            return []
        async with httpx.AsyncClient(timeout=30.0) as client:
            q = f"{condition} {intervention}" if intervention else condition
            try:
                r = await client.get(f"{self.BASE}/studies", params={"query.term": q, "pageSize": str(max_results)})
                r.raise_for_status()
                trials = []
                data = r.json()
                for s in data.get("studies", []):
                    try:
                        # Robust parsing with safe .get() calls
                        p = s.get("protocolSection", {})
                        ident = p.get("identificationModule", {})
                        status = p.get("statusModule", {})
                        design = p.get("designModule", {})

                        # Safe phase extraction
                        phases = design.get("phases", ["Unknown"])
                        if isinstance(phases, str):
                            phases = [phases]

                        # Safe enrollment extraction
                        enr = design.get("enrollmentInfo", {})
                        if isinstance(enr, dict):
                            enrollment = enr.get("count", 0) or 0
                        else:
                            enrollment = 0

                        # Safe conditions/interventions extraction
                        conditions = ident.get("conditions", [])
                        if not isinstance(conditions, list):
                            conditions = []

                        trials.append(ClinicalTrial(
                            ident.get("nctId", "") or "",
                            ident.get("briefTitle", "") or "",
                            "/".join(str(x) for x in phases) if phases else "Unknown",
                            status.get("overallStatus", "") or "Unknown",
                            conditions[:5],
                            [],
                            enrollment,
                        ))
                    except Exception:
                        continue
                return trials
            except Exception as e:
                print(f"ClinicalTrials error: {e}")
                return []


class LiteratureIntegrator:
    """Unified PubMed + ClinicalTrials integration with structured status."""

    def __init__(self):
        self.pubmed = PubMedClient()
        self.ct = ClinicalTrialsClient()

    async def get_target_literature(self, gene: str, disease: str, max_articles: int = 10) -> Dict[str, Any]:
        """Primary async method. Returns structured result with status."""
        status = FetchStatus.SUCCESS
        error_msg = None
        
        query = f"{gene}[Title/Abstract] AND {disease}[Title/Abstract]"
        
        try:
            articles, trials = await asyncio.gather(
                self.pubmed.search_and_fetch(query, max_articles),
                self.ct.search(disease, gene, max_articles // 2),
            )
        except Exception as e:
            status = FetchStatus.PARTIAL
            error_msg = str(e)[:200]
            articles, trials = [], []

        # Determine actual status based on results
        if not HAS_HTTPX:
            status = FetchStatus.SKIPPED
            error_msg = "httpx not available"
        elif len(articles) == 0 and len(trials) == 0:
            status = FetchStatus.PARTIAL
            error_msg = "No articles or trials found"

        return {
            "gene": gene,
            "disease": disease,
            "articles": [{"pmid": a.pmid, "title": a.title, "year": a.year,
                          "journal": a.journal, "authors": a.authors[:3]} for a in articles],
            "clinical_trials": [{"nct_id": t.nct_id, "title": t.title, "phase": t.phase,
                                 "status": t.status, "enrollment": t.enrollment} for t in trials],
            "summary": {
                "total_articles": len(articles),
                "total_trials": len(trials),
            },
            # Structured status
            "fetch_status": status.value,
            "error": error_msg,
        }

    def get_sync(self, gene: str, disease: str, max_articles: int = 10) -> Dict[str, Any]:
        """
        Synchronous wrapper - safe for both sync and async contexts.
        
        Uses ThreadPoolExecutor when called inside an existing event loop
        to avoid "asyncio.run() cannot be called from a running event loop".
        """
        try:
            # Check if we're already inside an event loop
            try:
                loop = asyncio.get_running_loop()
                is_running = loop.is_running()
            except RuntimeError:
                loop = None
                is_running = False

            if is_running:
                # Inside an active event loop - use ThreadPoolExecutor
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(
                        asyncio.run,
                        self.get_target_literature(gene, disease, max_articles)
                    )
                    return future.result(timeout=60.0)  # 60s timeout
            else:
                # No running loop - safe to use asyncio.run directly
                return asyncio.run(self.get_target_literature(gene, disease, max_articles))
                
        except concurrent.futures.TimeoutError:
            return {
                "gene": gene,
                "disease": disease,
                "articles": [],
                "clinical_trials": [],
                "summary": {"total_articles": 0, "total_trials": 0},
                "fetch_status": FetchStatus.FAILED.value,
                "error": "Timeout fetching literature (60s)",
            }
        except Exception as e:
            return {
                "gene": gene,
                "disease": disease,
                "articles": [],
                "clinical_trials": [],
                "summary": {"total_articles": 0, "total_trials": 0},
                "fetch_status": FetchStatus.FAILED.value,
                "error": str(e)[:200],
            }
