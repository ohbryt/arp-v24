"""
ARP v24 - Main Pipeline Orchestrator

Unified interface to all three engines + optional API enrichment.
This pipeline actually runs end-to-end.

Usage:
    python pipeline.py masld
    python pipeline.py sarcopenia --top-n 5
    python pipeline.py cancer --with-literature
"""

import json
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.scoring_engine import DiseaseEngine, TargetScorer, TARGET_REGISTRY
from core.modality_routing import ModalityRouter, AssayEngine
from core.candidate_engine import CandidateEngine, CandidateRankingResult
from core.schema import TargetDossier, ScoringEngineConfig, DiseaseType


DISEASE_MAP = {
    "masld": DiseaseType.MASLD, "sarcopenia": DiseaseType.SARCOPENIA,
    "lung_fibrosis": DiseaseType.LUNG_FIBROSIS, "lung-fibrosis": DiseaseType.LUNG_FIBROSIS,
    "heart_failure": DiseaseType.HEART_FAILURE, "heart-failure": DiseaseType.HEART_FAILURE,
    "cancer": DiseaseType.CANCER,
}


@dataclass
class PipelineResult:
    """Complete pipeline result"""
    disease: str
    targets: List[TargetDossier]
    total_targets_evaluated: int
    execution_time_seconds: float
    engine1_result: Any = None
    engine2_results: Dict[str, Any] = field(default_factory=dict)
    engine3_results: Dict[str, Any] = field(default_factory=dict)
    literature: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipeline": "ARP v24",
            "disease": self.disease,
            "total_targets_evaluated": self.total_targets_evaluated,
            "targets_returned": len(self.targets),
            "execution_time_seconds": round(self.execution_time_seconds, 2),
            "top_targets": [
                {"rank": t.rank, "gene": t.gene_name, "score": round(t.priority_score, 3),
                 "modalities": t.recommended_modalities[:2]}
                for t in self.targets[:10]
            ],
            "engine2_runs": len(self.engine2_results),
            "engine3_runs": len(self.engine3_results),
        }

    def save_json(self, filepath: str):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"  ARP v24 Pipeline Results: {self.disease.upper()}")
        print(f"{'='*60}")
        print(f"  Targets evaluated: {self.total_targets_evaluated}")
        print(f"  Time: {self.execution_time_seconds:.1f}s\n")

        for t in self.targets[:10]:
            mods = ", ".join(t.recommended_modalities[:2]) if t.recommended_modalities else "N/A"
            print(f"  {t.rank:2d}. {t.gene_name:<10s} score={t.priority_score:.3f}  [{mods}]")

            # Show Engine 2 result if available
            e2 = self.engine2_results.get(t.gene_name)
            if e2:
                primary = e2.get("primary_modality", "N/A")
                print(f"      Engine 2: {primary}")

            # Show Engine 3 result if available
            e3 = self.engine3_results.get(t.gene_name)
            if e3:
                top = e3.get("top_10", [])
                if top:
                    names = [c["name"] for c in top[:3]]
                    print(f"      Engine 3: {', '.join(names)}")

        print(f"\n{'='*60}\n")


class ARPv24Pipeline:
    """Main pipeline: Disease -> Target -> Modality -> Candidate"""

    def __init__(self, config: Optional[ScoringEngineConfig] = None):
        self.engine1 = DiseaseEngine(config)
        self.engine2 = ModalityRouter()
        self.engine3 = CandidateEngine()
        self.assay_engine = AssayEngine()

    def run(
        self, disease: str, top_n: int = 10,
        run_engine2: bool = True, run_engine3: bool = True,
        with_literature: bool = False,
    ) -> PipelineResult:
        start = time.time()
        disease_type = self._resolve_disease(disease)

        # Engine 1: Target Prioritization
        print(f"  [Engine 1] Prioritizing targets for {disease}...")
        e1 = self.engine1.prioritize_targets(disease_type)
        targets = e1.get_top_targets(top_n)
        print(f"  [Engine 1] {len(targets)} targets scored")

        # Engine 2: Modality Routing (top 5)
        e2_results = {}
        if run_engine2:
            print(f"  [Engine 2] Routing modalities...")
            for t in targets[:5]:
                r = self.engine2.route_target(t, disease_type)
                e2_results[t.gene_name] = r.to_dict()

        # Engine 3: Candidate Generation (top 5)
        e3_results = {}
        if run_engine3:
            print(f"  [Engine 3] Generating candidates...")
            for t in targets[:5]:
                mod = t.recommended_modalities[0] if t.recommended_modalities else "small_molecule"
                r = self.engine3.generate_candidates(t.gene_name, disease, mod)
                e3_results[t.gene_name] = r.to_dict()

        # Optional: Literature enrichment
        lit = {}
        if with_literature:
            print(f"  [Literature] Fetching PubMed + ClinicalTrials...")
            try:
                from api.pubmed import LiteratureIntegrator
                integrator = LiteratureIntegrator()
                if targets:
                    lit = integrator.get_sync(targets[0].gene_name, disease)
                    print(f"  [Literature] {lit.get('summary', {}).get('total_articles', 0)} articles found")
            except Exception as e:
                print(f"  [Literature] Skipped: {e}")

        elapsed = time.time() - start

        return PipelineResult(
            disease=disease, targets=targets,
            total_targets_evaluated=e1.total_candidates_evaluated,
            execution_time_seconds=elapsed,
            engine1_result=e1, engine2_results=e2_results,
            engine3_results=e3_results, literature=lit,
        )

    def analyze_target(self, gene: str, disease: str) -> Dict[str, Any]:
        """Deep analysis of a single target"""
        disease_type = self._resolve_disease(disease)
        from core.scoring_engine import TARGET_REGISTRY
        from core.schema import TargetClass, Status
        from datetime import date

        target = TargetDossier(
            target_id=f"{gene}_{disease}", gene_name=gene,
            disease=disease_type, status=Status.PRIORITIZED,
            created_date=date.today(), last_updated=date.today(),
        )

        info = TARGET_REGISTRY.get(disease, {}).get(gene)
        if info:
            scores, penalties, ps = TargetScorer().score_target(info, disease_type)
            target.scores = scores
            target.priority_score = ps
            target.penalties = penalties
            target.target_class = info.target_class
            target.is_extracellular = info.is_extracellular

        mod = self.engine2.route_target(target, disease_type)
        assays = self.assay_engine.get_assays(disease_type)
        top_mod = mod.get_top_modality() or "small_molecule"
        cands = self.engine3.generate_candidates(gene, disease, top_mod)

        return {
            "target": target.to_dict(),
            "modality_routing": mod.to_dict(),
            "assays": [{"name": a.assay_name, "type": a.assay_type, "readout": a.readout} for a in assays[:5]],
            "candidates": cands.to_dict(),
        }

    @staticmethod
    def _resolve_disease(disease: str) -> DiseaseType:
        key = disease.lower().strip()
        if key not in DISEASE_MAP:
            raise ValueError(f"Unknown disease: {disease!r}. Options: {list(DISEASE_MAP.keys())}")
        return DISEASE_MAP[key]


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def run_pipeline(disease: str, top_n: int = 10, with_literature: bool = False) -> PipelineResult:
    """Run the full ARP v24 pipeline"""
    return ARPv24Pipeline().run(disease, top_n, with_literature=with_literature)


def analyze_target(gene: str, disease: str) -> Dict[str, Any]:
    """Analyze a single target"""
    return ARPv24Pipeline().analyze_target(gene, disease)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ARP v24 Drug Discovery Pipeline")
    parser.add_argument("disease", help="Disease: masld, sarcopenia, lung_fibrosis, heart_failure, cancer")
    parser.add_argument("--top-n", type=int, default=10, help="Number of top targets")
    parser.add_argument("--with-literature", action="store_true", help="Include PubMed/CT.gov")
    parser.add_argument("--output", help="Save JSON output to file")
    parser.add_argument("--target", help="Analyze a single target gene")
    args = parser.parse_args()

    if args.target:
        result = analyze_target(args.target, args.disease)
        print(json.dumps(result, indent=2, default=str))
    else:
        result = run_pipeline(args.disease, args.top_n, args.with_literature)
        result.print_summary()
        if args.output:
            result.save_json(args.output)
            print(f"Saved to {args.output}")
