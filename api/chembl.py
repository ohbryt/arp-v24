"""
ARP v24 - ChEMBL REST API Client

Live bioactivity data from ChEMBL (CC BY-SA 3.0).
"""

import time
from typing import Dict, List, Optional, Any, Iterator
from pathlib import Path

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class ChEMBLClient:
    """
    ChEMBL REST API client for bioactivity data.

    Usage:
        client = ChEMBLClient()
        targets = client.fetch_target_by_gene("THRB")
        df = client.fetch_activities_by_target("CHEMBL2093872")
    """
    BASE = "https://www.ebi.ac.uk/chembl/api"

    def __init__(self, timeout: float = 60.0):
        if not HAS_HTTPX:
            raise ImportError("httpx required: pip install httpx")
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
        """Find ChEMBL target(s) by gene name"""
        data = self._get("target.json", {
            "target_name__icontains": gene_name,
            "target_type": "SINGLE PROTEIN",
        })
        return data.get("targets", [])

    def fetch_activities_by_target(
        self, target_chembl_id: str, max_value_nm: float = 10000,
    ) -> List[Dict[str, Any]]:
        """Fetch bioactivity data for a ChEMBL target ID"""
        records = []
        params = {
            "target_chembl_id": target_chembl_id,
            "assay_type": "B",  # Binding assays
            "limit": "500",
        }
        try:
            data = self._get("activity.json", params)
            for act in data.get("activities", []):
                val = self._float(act.get("value"))
                pchembl = self._float(act.get("pchembl_value"))
                if val is not None and val <= max_value_nm:
                    records.append({
                        "molecule_chembl_id": act.get("molecule_chembl_id"),
                        "smiles": act.get("canonical_smiles"),
                        "activity_type": act.get("standard_type"),
                        "activity_value_nM": val,
                        "pchembl": pchembl,
                        "assay_id": act.get("assay_chembl_id"),
                    })
        except Exception as e:
            print(f"ChEMBL activity fetch error: {e}")
        return records

    def fetch_molecule(self, chembl_id: str) -> Dict:
        """Fetch molecule details"""
        return self._get(f"molecule/{chembl_id}.json")

    def enrich_gene(self, gene_name: str, max_compounds: int = 20) -> List[Dict]:
        """
        High-level: gene name -> top bioactive compounds.
        Useful for Engine 3 enrichment.
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
        for a in sorted(activities, key=lambda x: x.get("pchembl") or 0, reverse=True):
            mid = a.get("molecule_chembl_id")
            if mid and mid not in seen:
                seen.add(mid)
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
