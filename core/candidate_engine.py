"""
ARP v24 - Engine 3: Modality -> Candidate Generation

Ported from v22 with bug fixes. Retrieves known compounds and ranks them.
Optionally enriches with live ChEMBL bioactivity data.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class CandidateCompound:
    """A candidate compound for a target"""
    compound_id: str
    name: str
    smiles: Optional[str] = None
    modality: str = "small_molecule"
    source: str = "literature"
    development_stage: str = "preclinical"
    target_name: str = ""
    binding_mode: str = "unknown"
    affinity: Optional[float] = None  # nM

    # ADMET scores (0-1)
    admet_score: float = 0.50
    absorption_score: float = 0.50
    distribution_score: float = 0.50
    metabolism_score: float = 0.50
    excretion_score: float = 0.50
    safety_score: float = 0.50

    # Developability
    solubility: float = 0.50
    permeability: float = 0.50
    metabolic_stability: float = 0.50
    herg_liability: float = 0.50

    # Efficacy
    efficacy_score: float = 0.50
    potency_score: float = 0.50
    modality_fit_score: float = 1.0

    # Composite
    composite_score: float = 0.0
    admet_composite: float = 0.0

    # Metadata
    clinical_trials: List[str] = field(default_factory=list)
    approved_indications: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    def calculate_scores(self):
        admet_c = (self.absorption_score * 0.20 + self.distribution_score * 0.15
                   + self.metabolism_score * 0.20 + self.excretion_score * 0.10
                   + self.safety_score * 0.35)
        self.admet_composite = (admet_c * 0.7 + self.admet_score * 0.3) if self.admet_score != 0.50 else admet_c

        dev = (self.solubility * 0.25 + self.permeability * 0.25
               + self.metabolic_stability * 0.25 + (1 - self.herg_liability) * 0.25)

        self.composite_score = (self.admet_composite * 0.35 + self.efficacy_score * 0.35
                                + dev * 0.20 + self.potency_score * 0.10)

    def to_dict(self) -> Dict[str, Any]:
        self.calculate_scores()
        return {
            "compound_id": self.compound_id, "name": self.name,
            "smiles": self.smiles, "modality": self.modality,
            "source": self.source, "development_stage": self.development_stage,
            "target": self.target_name, "affinity_nM": self.affinity,
            "admet_score": round(self.admet_composite, 3),
            "efficacy_score": round(self.efficacy_score, 3),
            "composite_score": round(self.composite_score, 3),
        }


@dataclass
class CandidateRankingResult:
    target_id: str
    gene_name: str
    disease: str
    modality: str
    candidates: List[CandidateCompound]
    total_candidates: int
    ranking_time_seconds: float = 0.0

    def get_top_candidates(self, n: int = 10) -> List[CandidateCompound]:
        return sorted(self.candidates, key=lambda c: c.composite_score, reverse=True)[:n]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_id": self.target_id, "gene_name": self.gene_name,
            "disease": self.disease, "modality": self.modality,
            "total_candidates": self.total_candidates,
            "top_10": [
                {"name": c.name, "composite_score": round(c.composite_score, 3),
                 "admet_score": round(c.admet_composite, 3), "stage": c.development_stage}
                for c in self.get_top_candidates(10)
            ],
        }


# ============================================================================
# KNOWN COMPOUNDS DATABASE (~40 real drugs)
# ============================================================================

COMPOUND_DATABASE = {
    "masld": {
        "THRB": [
            {"name": "Resmetirom", "stage": "approved", "affinity": 0.21},
            {"name": "ASC-41", "stage": "phase2"},
            {"name": "TERN-101", "stage": "phase2"},
        ],
        "NR1H4": [
            {"name": "Obeticholic acid", "stage": "approved", "affinity": 90.0},
            {"name": "Cilofexor", "stage": "phase2"},
            {"name": "Tropifexor", "stage": "phase2"},
        ],
        "GLP1R": [
            {"name": "Semaglutide", "stage": "approved", "affinity": 0.015},
            {"name": "Liraglutide", "stage": "approved", "affinity": 0.038},
            {"name": "Tirzepatide", "stage": "approved", "affinity": 0.025},
        ],
        "SLC5A2": [
            {"name": "Empagliflozin", "stage": "approved", "affinity": 3.1},
            {"name": "Dapagliflozin", "stage": "approved", "affinity": 1.2},
        ],
    },
    "sarcopenia": {
        "MSTN": [
            {"name": "Bimagrumab", "stage": "phase2"},
            {"name": "Apitegromab", "stage": "phase2"},
            {"name": "Domagrozumab", "stage": "discontinued"},
        ],
        "MTOR": [
            {"name": "Rapamycin", "stage": "approved", "affinity": 0.1},
            {"name": "Everolimus", "stage": "approved", "affinity": 0.3},
        ],
        "SIRT1": [
            {"name": "Resveratrol", "stage": "preclinical", "affinity": 100.0},
            {"name": "SRT2104", "stage": "phase1"},
        ],
        "PRKAA1": [
            {"name": "Metformin", "stage": "approved", "affinity": 100.0},
            {"name": "AICAR", "stage": "preclinical"},
        ],
    },
    "lung_fibrosis": {
        "TGFB1": [
            {"name": "Pirfenidone", "stage": "approved"},
            {"name": "Nintedanib", "stage": "approved", "affinity": 80.0},
            {"name": "Pamrevlumab", "stage": "phase2"},
        ],
    },
    "heart_failure": {
        "SLC5A2": [
            {"name": "Empagliflozin", "stage": "approved", "affinity": 3.1},
            {"name": "Dapagliflozin", "stage": "approved", "affinity": 1.2},
        ],
        "NPPA": [{"name": "Nesiritide", "stage": "approved", "affinity": 0.1}],
    },
    "cancer": {
        "EGFR": [
            {"name": "Osimertinib", "stage": "approved", "affinity": 0.7},
            {"name": "Erlotinib", "stage": "approved", "affinity": 2.0},
            {"name": "Gefitinib", "stage": "approved", "affinity": 1.0},
            {"name": "Afatinib", "stage": "approved", "affinity": 0.5},
        ],
        "ALK": [
            {"name": "Alectinib", "stage": "approved", "affinity": 1.9},
            {"name": "Lorlatinib", "stage": "approved", "affinity": 0.7},
        ],
        "MET": [
            {"name": "Capmatinib", "stage": "approved", "affinity": 0.6},
            {"name": "Tepotinib", "stage": "approved", "affinity": 3.0},
        ],
        "KRAS": [
            {"name": "Sotorasib", "stage": "approved", "affinity": 10.0},
            {"name": "Adagrasib", "stage": "approved", "affinity": 5.0},
        ],
        "CD274": [
            {"name": "Pembrolizumab", "stage": "approved", "affinity": 0.1},
            {"name": "Atezolizumab", "stage": "approved", "affinity": 0.1},
        ],
    },
}

# Stage -> base ADMET/efficacy scores
STAGE_SCORES = {
    "approved": dict(admet_score=0.85, absorption_score=0.85, distribution_score=0.80,
                     metabolism_score=0.80, excretion_score=0.82, safety_score=0.80,
                     solubility=0.82, permeability=0.80, metabolic_stability=0.82,
                     herg_liability=0.15, efficacy_score=0.85, potency_score=0.85),
    "phase3": dict(admet_score=0.78, absorption_score=0.80, distribution_score=0.75,
                   metabolism_score=0.75, excretion_score=0.78, safety_score=0.75,
                   solubility=0.78, permeability=0.75, metabolic_stability=0.75,
                   herg_liability=0.20, efficacy_score=0.80, potency_score=0.80),
    "phase2": dict(admet_score=0.70, absorption_score=0.72, distribution_score=0.68,
                   metabolism_score=0.68, excretion_score=0.70, safety_score=0.68,
                   solubility=0.70, permeability=0.70, metabolic_stability=0.68,
                   herg_liability=0.25, efficacy_score=0.72, potency_score=0.75),
    "phase1": dict(admet_score=0.65, absorption_score=0.68, distribution_score=0.62,
                   metabolism_score=0.62, excretion_score=0.65, safety_score=0.60,
                   solubility=0.65, permeability=0.65, metabolic_stability=0.60,
                   herg_liability=0.30, efficacy_score=0.60, potency_score=0.70),
    "preclinical": dict(admet_score=0.55, absorption_score=0.58, distribution_score=0.52,
                        metabolism_score=0.52, excretion_score=0.55, safety_score=0.50,
                        solubility=0.55, permeability=0.55, metabolic_stability=0.50,
                        herg_liability=0.35, efficacy_score=0.50, potency_score=0.60),
    "discontinued": dict(admet_score=0.30, absorption_score=0.35, distribution_score=0.30,
                         metabolism_score=0.30, excretion_score=0.32, safety_score=0.25,
                         solubility=0.35, permeability=0.32, metabolic_stability=0.30,
                         herg_liability=0.50, efficacy_score=0.30, potency_score=0.40),
}

# Modality compatibility matrix
MODALITY_COMPAT = {
    ("small_molecule", "biologic"): 0.3, ("small_molecule", "peptide"): 0.6,
    ("small_molecule", "antibody"): 0.2, ("small_molecule", "degrader"): 0.7,
    ("biologic", "small_molecule"): 0.3, ("biologic", "antibody"): 0.9,
    ("biologic", "peptide"): 0.8, ("peptide", "small_molecule"): 0.4,
    ("peptide", "biologic"): 0.7, ("antibody", "biologic"): 0.9,
}


class CandidateEngine:
    """Engine 3: Retrieves/ranks candidate compounds for targets."""

    def __init__(self):
        self.db = COMPOUND_DATABASE

    def generate_candidates(
        self, gene_name: str, disease: str,
        modality: str = "small_molecule",
    ) -> CandidateRankingResult:
        start = time.time()
        candidates = []
        target_compounds = self.db.get(disease, {}).get(gene_name, [])

        for i, data in enumerate(target_compounds):
            c = self._create_candidate(f"{gene_name}_{i+1}", gene_name, modality, **data)
            candidates.append(c)

        for c in candidates:
            c.calculate_scores()
            c.composite_score *= c.modality_fit_score

        candidates.sort(key=lambda x: x.composite_score, reverse=True)

        return CandidateRankingResult(
            f"{gene_name}_{disease}", gene_name, disease, modality,
            candidates, len(candidates), time.time() - start,
        )

    def _create_candidate(
        self, cid: str, gene: str, modality_hint: str,
        name: str, stage: str = "preclinical",
        affinity: float = None, smiles: str = None,
    ) -> CandidateCompound:
        scores = STAGE_SCORES.get(stage, STAGE_SCORES["preclinical"])
        actual_mod = "small_molecule" if smiles else "biologic"
        fit = 1.0 if actual_mod == modality_hint else MODALITY_COMPAT.get((actual_mod, modality_hint), 0.5)

        return CandidateCompound(
            compound_id=cid, name=name, smiles=smiles,
            modality=actual_mod, source="literature",
            development_stage=stage, target_name=gene,
            affinity=affinity, modality_fit_score=fit, **scores,
        )
