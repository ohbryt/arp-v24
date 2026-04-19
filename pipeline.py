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
from enum import Enum

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


class LiteratureStatus(Enum):
    """Structured status for literature enrichment."""
    SUCCESS = "success"
    PARTIAL_FAILURE = "partial_failure"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass
class PipelineResult:
    """Complete pipeline result with structured status reporting."""
    disease: str
    targets: List[TargetDossier]
    total_targets_evaluated: int
    execution_time_seconds: float
    
    # Engine results
    engine1_result: Any = None
    engine2_results: Dict[str, Any] = field(default_factory=dict)
    engine3_results: Dict[str, Any] = field(default_factory=dict)
    
    # Structured status reporting (Phase 4)
    literature_status: LiteratureStatus = LiteratureStatus.SKIPPED
    literature_error: Optional[str] = None
    literature_summary: Dict[str, Any] = field(default_factory=dict)
    literature_articles: List[Dict[str, Any]] = field(default_factory=list)
    literature_trials: List[Dict[str, Any]] = field(default_factory=list)
    
    # Warnings (Phase 4)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Rich serialized output with status fields."""
        return {
            "pipeline": "ARP v24",
            "disease": self.disease,
            "total_targets_evaluated": self.total_targets_evaluated,
            "targets_returned": len(self.targets),
            "execution_time_seconds": round(self.execution_time_seconds, 2),
            
            # Structured status (Phase 4)
            "literature_status": self.literature_status.value,
            "literature_error": self.literature_error,
            "literature_summary": self.literature_summary,
            
            # Warnings and errors
            "warnings": self.warnings,
            "errors": self.errors,
            
            # Engine breakdowns
            "engine2_runs": len(self.engine2_results),
            "engine3_runs": len(self.engine3_results),
            
            # Top targets with richer info
            "top_targets": [
                {
                    "rank": t.rank,
                    "gene": t.gene_name,
                    "score": round(t.priority_score, 3),
                    "recommended_modalities": t.recommended_modalities[:3] if t.recommended_modalities else [],
                    "engine2_modality": self.engine2_results.get(t.gene_name, {}).get("primary_modality"),
                    "engine3_top_candidate": (
                        self.engine3_results.get(t.gene_name, {})
                        .get("top_10", [{}])[0].get("name")
                        if self.engine3_results.get(t.gene_name) and self.engine3_results.get(t.gene_name, {}).get("top_10")
                        else None
                    ),
                }
                for t in self.targets[:10]
            ],
            
            # Engine 2 modality recommendations for comparison with Engine 3
            "engine2_modalities": {
                gene: {
                    "primary_modality": data.get("primary_modality"),
                    "recommended_modalities": data.get("recommended_modalities", [])[:3],
                }
                for gene, data in self.engine2_results.items()
            },
            
            # Engine 3 candidates with modality for comparison
            "engine3_candidates": {
                gene: {
                    "requested_modality": data.get("modality"),
                    "candidates": [
                        {
                            "name": c.get("name"),
                            "modality": c.get("modality"),  # Actual modality from DB
                            "composite_score": c.get("composite_score"),
                            "affinity_nM": c.get("affinity_nM"),
                        }
                        for c in data.get("top_10", [])[:5]
                    ],
                }
                for gene, data in self.engine3_results.items()
            },
        }

    def save_json(self, filepath: str):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def print_summary(self):
        """CLI-friendly summary with status indicators."""
        print(f"\n{'='*60}")
        print(f"  ARP v24 Pipeline Results: {self.disease.upper()}")
        print(f"{'='*60}")
        print(f"  Targets evaluated: {self.total_targets_evaluated}")
        print(f"  Time: {self.execution_time_seconds:.1f}s\n")

        # Literature status indicator
        lit_icon = {
            LiteratureStatus.SUCCESS: "✓",
            LiteratureStatus.PARTIAL_FAILURE: "⚠",
            LiteratureStatus.SKIPPED: "-",
            LiteratureStatus.FAILED: "✗",
        }.get(self.literature_status, "?")
        print(f"  Literature: {lit_icon} {self.literature_status.value}")
        if self.literature_error:
            print(f"    Error: {self.literature_error[:50]}...")
        
        # Warnings indicator
        if self.warnings:
            print(f"  Warnings: {len(self.warnings)}")
            for w in self.warnings[:3]:
                print(f"    - {w[:60]}...")
        
        print()
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
        warnings = []
        errors = []

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
                
                # Check for modality mismatches (warnings)
                for c in r.candidates:
                    if c.warnings:
                        warnings.extend([f"{t.gene_name}/{c.name}: {w}" for w in c.warnings])

        # Optional: Literature enrichment (Phase 4 - structured status)
        lit_status = LiteratureStatus.SKIPPED
        lit_error = None
        lit_summary = {}
        lit_articles = []
        lit_trials = []
        
        if with_literature:
            print(f"  [Literature] Fetching PubMed + ClinicalTrials...")
            try:
                from api.pubmed import LiteratureIntegrator
                integrator = LiteratureIntegrator()
                if targets:
                    result = integrator.get_sync(targets[0].gene_name, disease)
                    
                    # Check for structured error in result
                    if result.get("error"):
                        lit_status = LiteratureStatus.PARTIAL_FAILURE
                        lit_error = result.get("error")
                        lit_summary = result.get("summary", {})
                    elif result.get("summary", {}).get("total_articles", 0) > 0:
                        lit_status = LiteratureStatus.SUCCESS
                        lit_summary = result.get("summary", {})
                        lit_articles = result.get("articles", [])
                        lit_trials = result.get("clinical_trials", [])
                        print(f"  [Literature] {lit_summary.get('total_articles', 0)} articles found")
                    else:
                        lit_status = LiteratureStatus.PARTIAL_FAILURE
                        lit_error = "No articles found"
                        lit_summary = result.get("summary", {})
                        
            except Exception as e:
                lit_status = LiteratureStatus.FAILED
                lit_error = str(e)[:200]
                warnings.append(f"Literature integration failed: {e}")
                print(f"  [Literature] Failed: {e}")

        elapsed = time.time() - start

        return PipelineResult(
            disease=disease,
            targets=targets,
            total_targets_evaluated=e1.total_candidates_evaluated,
            execution_time_seconds=elapsed,
            engine1_result=e1,
            engine2_results=e2_results,
            engine3_results=e3_results,
            literature_status=lit_status,
            literature_error=lit_error,
            literature_summary=lit_summary,
            literature_articles=lit_articles,
            literature_trials=lit_trials,
            warnings=warnings,
            errors=errors,
        )

    def _resolve_disease(self, disease: str) -> DiseaseType:
        """Resolve disease string to DiseaseType enum."""
        if disease.lower() in DISEASE_MAP:
            return DISEASE_MAP[disease.lower()]
        raise ValueError(f"Unknown disease: {disease}. Valid: {list(DISEASE_MAP.keys())}")


def analyze_target(gene: str, disease: str) -> Dict[str, Any]:
    """Single target deep analysis."""
    pipeline = ARPv24Pipeline()
    disease_type = pipeline._resolve_disease(disease)
    
    # Get target from engine 1
    e1 = pipeline.engine1.prioritize_targets(disease_type)
    target = next((t for t in e1.targets if t.gene_name == gene), None)
    
    if not target:
        return {"error": f"Target {gene} not found for {disease}"}
    
    # Engine 2 routing
    routing = pipeline.engine2.route_target(target, disease_type)
    
    # Engine 3 candidates
    mod = target.recommended_modalities[0] if target.recommended_modalities else "small_molecule"
    candidates = pipeline.engine3.generate_candidates(gene, disease, mod)
    
    return {
        "target": target.to_dict(),
        "modality_routing": routing.to_dict(),
        "candidates": candidates.to_dict(),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ARP v24 Pipeline")
    parser.add_argument("disease", help="Disease: masld, sarcopenia, lung_fibrosis, heart_failure, cancer")
    parser.add_argument("--top-n", type=int, default=10, help="Number of targets")
    parser.add_argument("--no-engine2", action="store_true", help="Skip Engine 2")
    parser.add_argument("--no-engine3", action="store_true", help="Skip Engine 3")
    parser.add_argument("--with-literature", action="store_true", help="Include literature")
    parser.add_argument("--save-json", help="Save results to JSON file")
    args = parser.parse_args()

    pipeline = ARPv24Pipeline()
    result = pipeline.run(
        args.disease, top_n=args.top_n,
        run_engine2=not args.no_engine2,
        run_engine3=not args.no_engine3,
        with_literature=args.with_literature,
    )
    
    result.print_summary()
    
    if args.save_json:
        result.save_json(args.save_json)
        print(f"Results saved to {args.save_json}")


if __name__ == "__main__":
    main()
