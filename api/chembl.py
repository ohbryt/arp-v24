"""
ARP v24 - ChEMBL REST API Client

Live bioactivity data from ChEMBL (CC BY-SA 3.0).

Ready for optional Engine 3 enrichment:
- Fetch top bioactive compounds for a gene
- Use ChEMBL data to augment internal COMPOUND_DATABASE
- No runtime coupling: call only when explicitly requested

Usage:
    from api.chembl import ChEMBLClient
    client = ChEMBLClient()
    compounds = client.enrich_gene("THRB")
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


@dataclass
class ChEMBLCompound:
    """Structured compound from ChEMBL."""
    chembl_id: str
    smiles: Optional[str]
    activity_type: str
    activity_value_nM: float
    pchembl: Optional[float]
    assay_id: Optional[str]
    
    def to_candidate_dict(self) -> Dict[str, Any]:
        """Convert to CandidateCompound-compatible dict."""
        return {
            "name": self.chembl_id,
            "smiles": self.smiles,
            "affinity": self.activity_value_nM,
            "modality": "small_molecule" if self.smiles else "biologic",
            "stage": self._stage_from_pchembl(),
        }
    
    def _stage_from_pchembl(self) -> str:
        if self.pchembl is None:
            return "preclinical"
        if self.pchembl >= 6:
            return "clinical"
        if self.pchembl >= 5:
            return "phase1"
        return "preclinical"


class ChEMBLClient:
    """
    ChEMBL REST API client for bioactivity data.
    
    Minimal implementation - ready for optional enrichment.
    Does NOT fetch on init; call methods explicitly.
    """
    BASE = "https://www.ebi.ac.uk/chembl/api"

    def __init__(self, timeout: float = 30.0):
        if not HAS_HTTPX:
            raise ImportError("httpx required for ChEMBL: pip install httpx")
        self._client = httpx.Client(timeout=timeout)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        r = self._client.get(f"{self.BASE}/{endpoint}", params=params)
        r.raise_for_status()
        return r.json()

    def fetch_target_by_gene(self, gene_name: str) -> List[Dict]:
        """Find ChEMBL target(s) by gene name."""
        data = self._get("target.json", {
            "target_name__icontains": gene_name,
            "target_type": "SINGLE PROTEIN",
        })
        return data.get("targets", [])

    def fetch_activities_by_target(
        self, target_chembl_id: str, max_value_nm: float = 10000,
    ) -> List[ChEMBLCompound]:
        """Fetch bioactivity records for a ChEMBL target ID."""
        records = []
        try:
            data = self._get("activity.json", {
                "target_chembl_id": target_chembl_id,
                "assay_type": "B",
                "limit": "500",
            })
            for act in data.get("activities", []):
                val = self._float(act.get("value"))
                pchembl = self._float(act.get("pchembl_value"))
                if val is not None and val <= max_value_nm:
                    records.append(ChEMBLCompound(
                        chembl_id=act.get("molecule_chembl_id") or "",
                        smiles=act.get("canonical_smiles"),
                        activity_type=act.get("standard_type") or "",
                        activity_value_nM=val,
                        pchembl=pchembl,
                        assay_id=act.get("assay_chembl_id"),
                    ))
        except Exception as e:
            pass  # Silently fail - not critical
        return records

    def enrich_gene(self, gene_name: str, max_compounds: int = 20) -> List[ChEMBLCompound]:
        """
        High-level gene enrichment: returns top bioactive compounds.
        
        This is the integration seam for Engine 3.
        Call this to augment COMPOUND_DATABASE with live ChEMBL data.
        
        Args:
            gene_name: Gene symbol (e.g., "THRB", "EGFR")
            max_compounds: Maximum number of compounds to return
            
        Returns:
            List of ChEMBLCompound objects sorted by potency
        """
        targets = self.fetch_target_by_gene(gene_name)
        if not targets:
            return []

        target_id = targets[0].get("target_chembl_id")
        if not target_id:
            return []

        activities = self.fetch_activities_by_target(target_id)

        # Sort by pchembl (higher = more potent) and dedupe by molecule
        seen = set()
        unique = []
        for a in sorted(activities, key=lambda x: x.pchembl or 0, reverse=True):
            if a.chembl_id and a.chembl_id not in seen:
                seen.add(a.chembl_id)
                unique.append(a)
            if len(unique) >= max_compounds:
                break

        return unique

    @staticmethod
    def _float(v) -> Optional[float]:
        if v is None:
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None


# Integration seam for CandidateEngine
def chembl_to_candidate_data(compound: ChEMBLCompound) -> Dict[str, Any]:
    """
    Convert ChEMBLCompound to CandidateCompound-compatible dict.
    
    Usage in Engine 3 future enrichment:
        from api.chembl import ChEMBLClient, chembl_to_candidate_data
        client = ChEMBLClient()
        chembl_comps = client.enrich_gene("THRB")
        candidate_data = [chembl_to_candidate_data(c) for c in chembl_comps]
    """
    return compound.to_candidate_dict()