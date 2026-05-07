"""
MolViBench-Style Evaluation Benchmarks
=======================================
Benchmarks to measure pipeline quality on BioMiner + TxConformal tasks.

Metrics:
  - Pass@1 rate (executability + chemical correctness)
  - Executability rate (code runs without errors)
  - Chemical correctness rate (output SMILES valid + drug-like)

Based on MolViBench evaluation framework (arxiv:2605.02351).
"""

import time
import json
import tempfile
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

# RDKit
from rdkit import Chem

# Local modules
from rdkit_validator import validate_smiles, batch_validate
from pipeline_evaluator import (
    evaluate_pipeline_code, EvalScore,
    execute_pipeline_code, ExecutionResult,
)


# ============================================================
# Benchmark tasks (L4-L5 complexity)
# ============================================================

# Realistic pipeline tasks matching BioMiner + TxConformal workflow
BENCHMARK_TASKS = [
    # ── L4: Multi-step filtering ──────────────────────────────────────────
    {
        "id": "L4_filter_01",
        "level": 4,
        "task": (
            "Given a list of SMILES, filter to only drug-like molecules "
            "(MW 200-700, LogP -1 to 6, HBD ≤ 5, HBA ≤ 10). "
            "Return canonical SMILES of filtered molecules."
        ),
        "test_input": [
            "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1",
            "Cc1ccc2c(c1)oc(=O)o2",
            "CCO",  # too small
            "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",  # too large
            "c1ccccc1",  # too small
            "CC(=O)NCCc1ccc(O)cc1",
        ],
        "expected_n_output": 3,  # first 3 should pass
    },
    {
        "id": "L4_filter_02",
        "level": 4,
        "task": (
            "Given a SMILES, compute molecular weight, LogP, QED score, "
            "and determine if it passes Lipinski's rule of 5. "
            "Return a dict with keys: mw, logp, qed, passes_ro5."
        ),
        "test_input": "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1",
        "expected_keys": ["mw", "logp", "qed", "passes_ro5"],
    },
    {
        "id": "L4_filter_03",
        "level": 4,
        "task": (
            "Given a list of SMILES, apply PAINS filter and return "
            "only molecules that have no PAINS alerts. "
            "Return a list of canonical SMILES."
        ),
        "test_input": [
            "CC(=O)NNC(=O)CSC[C@@H]([NH3+])C(=O)[O-]",
            "Cc1cccc(NC(=O)C[NH+]2CCN(CC(=O)N3C[C@H](C)C[C@@H](C)C3)CC2)c1C",
            "O=C(c1ccccn1)N1CCC(C(=O)N2C[C@H]3C[C@H](O)[C@H](O)C[C@H]3C2)CC1",
        ],
        "expected_n_output_min": 2,
    },
    {
        "id": "L4_transform_01",
        "level": 4,
        "task": (
            "Given a SMILES, canonicalize it and add a甲基 group (add CH3 to a random carbon). "
            "Return the canonical SMILES of the modified molecule."
        ),
        "test_input": "CCO",  # ethanol → propanol
        "expected_property": "mw > 46",  # MW should increase
    },
    {
        "id": "L4_rank_01",
        "level": 4,
        "task": (
            "Given a list of SMILES with scores (a list of dicts with 'smiles' and 'score'), "
            "sort by score descending and return canonical SMILES sorted by drug-likeness (QED). "
            "Return a list of canonical SMILES."
        ),
        "test_input": [
            {"smiles": "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1", "score": 0.9},
            {"smiles": "Cc1ccc2c(c1)oc(=O)o2", "score": 0.7},
            {"smiles": "CC(=O)NCCc1ccc(O)cc1", "score": 0.85},
        ],
        "expected_n_output": 3,
    },

    # ── L5: End-to-end pipelines ────────────────────────────────────────────
    {
        "id": "L5_biomer_filter",
        "level": 5,
        "task": (
            "You have BioMiner AI scores for 10 molecules. "
            "Filter to those with score > 0.7, then filter by MW 200-700, "
            "then apply PAINS filter, return canonical SMILES of passed molecules."
        ),
        "test_input": [
            {"smiles": "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1", "score": 0.95},
            {"smiles": "Cc1ccc2c(c1)oc(=O)o2", "score": 0.6},  # low score
            {"smiles": "CC(=O)NCCc1ccc(O)cc1", "score": 0.88},
            {"smiles": "CCO", "score": 0.5},  # too small
            {"smiles": "CN1CCC23C4C1Cc5cccc(c5)C2C3O4", "score": 0.75},
            {"smiles": "Cc1nc2n(n1)CCC[C@H]2[NH2+]Cc1cnn(-c2ccc(F)cc2)c1", "score": 0.82},
            {"smiles": "O=C(c1cn(CCN2CCOCC2)nn1)N1CCCC[C@@H]1c1nc2ccc(F)cc2[nH]1", "score": 0.71},
            {"smiles": "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC", "score": 0.9},  # too large
            {"smiles": "Cc1nn([C@H]2CCS(=O)(=O)C2)c(C)c1CC(=O)Nc1nc2c(C)cccc2s1", "score": 0.78},
            {"smiles": "CCc1ccc(CCNC(=O)N2C[C@@H](C)O[C@H](C)C2)cc1", "score": 0.85},
        ],
        "expected_n_output_min": 5,  # at least 5 should pass all filters
    },
    {
        "id": "L5_conformal_prep",
        "level": 5,
        "task": (
            "Given calibration data (list of dicts with 'smiles', 'y_true' labels) "
            "and test data (list of dicts with 'smiles', 'ai_score'), "
            "prepare the inputs for TxConformal: "
            "1. Separate calibration (y_true known) from test (y_true unknown) "
            "2. Return arrays f_calib, y_calib, f_test as JSON-serializable lists."
        ),
        "test_input": {
            "calib": [
                {"smiles": "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1", "y_true": 1},
                {"smiles": "Cc1ccc2c(c1)oc(=O)o2", "y_true": 0},
                {"smiles": "CC(=O)NCCc1ccc(O)cc1", "y_true": 1},
            ],
            "test": [
                {"smiles": "CN1CCC23C4C1Cc5cccc(c5)C2C3O4", "ai_score": 0.8},
                {"smiles": "O=C(c1cn(CCN2CCOCC2)nn1)N1CCCC[C@@H]1c1nc2ccc(F)cc2[nH]1", "ai_score": 0.7},
            ],
        },
        "expected_keys": ["f_calib", "y_calib", "f_test"],
    },
    {
        "id": "L5_full_screening",
        "level": 5,
        "task": (
            "End-to-end virtual screening: "
            "1. Take a list of SMILES with ai_score "
            "2. Filter by ai_score > 0.75 "
            "3. Filter by MW 250-650 "
            "4. Filter by LogP -1 to 5 "
            "5. Apply PAINS filter "
            "6. Rank by ai_score * QED "
            "7. Return top 5 as list of dicts with smiles, score, mw, qed."
        ),
        "test_input": [
            {"smiles": "CC(C)c1ccc([C@@H]2CCC[C@H](C(N)=O)CC2)cc1", "ai_score": 0.95, "mw": 259},
            {"smiles": "Cc1ccc2c(c1)oc(=O)o2", "ai_score": 0.55, "mw": 146},
            {"smiles": "CC(=O)NCCc1ccc(O)cc1", "ai_score": 0.88, "mw": 137},
            {"smiles": "CN1CCC23C4C1Cc5cccc(c5)C2C3O4", "ai_score": 0.78, "mw": 283},
            {"smiles": "Cc1nc2n(n1)CCC[C@H]2[NH2+]Cc1cnn(-c2ccc(F)cc2)c1", "ai_score": 0.82, "mw": 312},
            {"smiles": "O=C(c1cn(CCN2CCOCC2)nn1)N1CCCC[C@@H]1c1nc2ccc(F)cc2[nH]1", "ai_score": 0.71, "mw": 356},
            {"smiles": "Cc1nn([C@H]2CCS(=O)(=O)C2)c(C)c1CC(=O)Nc1nc2c(C)cccc2s1", "ai_score": 0.78, "mw": 389},
            {"smiles": "CCc1ccc(CCNC(=O)N2C[C@@H](C)O[C@H](C)C2)cc1", "ai_score": 0.85, "mw": 302},
        ],
        "expected_n_output_min": 3,
    },
]


# ============================================================
# Result types
# ============================================================

@dataclass
class BenchmarkResult:
    task_id: str
    level: int
    executability: float   # 0-1: code runs
    chemical_correctness: float  # 0-1: outputs valid + drug-like
    quality_score: float   # 0-1: composite
    execution_time_s: float
    error: str = ""
    output_preview: str = ""


@dataclass
class BenchmarkReport:
    n_total: int
    n_executable: int
    n_chem_correct: int
    n_quality: int
    pass_at_1: float     # executability * chemical_correctness
    executability_rate: float
    chemical_correctness_rate: float
    quality_rate: float
    results: list[BenchmarkResult]
    by_level: dict[int, dict] = field(default_factory=dict)


# ============================================================
# Benchmark runner
# ============================================================

class PipelineBenchmark:
    """
    Run MolViBench-style benchmarks on the incremental repair pipeline.
    """

    def __init__(
        self,
        tasks: list[dict] | None = None,
        max_rounds: int = 3,
        verbose: bool = True,
    ):
        self.tasks = tasks or BENCHMARK_TASKS
        self.max_rounds = max_rounds
        self.verbose = verbose

    def run_single(
        self,
        task: dict,
        pipeline,  # IncrementalRepairPipeline
    ) -> BenchmarkResult:
        """Run a single benchmark task."""
        task_id = task["id"]
        level = task["level"]
        test_input = task.get("test_input")

        start = time.time()

        try:
            result = pipeline.run(
                task=task["task"],
                test_input=test_input,
                target=task_id,
            )
            execution_time = time.time() - start

            # Compute chemical correctness
            if result.final_output is not None:
                smiles_list = pipeline._extract_smiles(result.final_output)
                if smiles_list:
                    vr = batch_validate(smiles_list, strict=True)
                    chem_score = sum(1 for r in vr if r.valid) / len(vr)
                else:
                    chem_score = 0.0
            else:
                chem_score = 0.0

            quality = result.quality_score if result.quality_score >= 0 else chem_score

            output_preview = ""
            if result.final_output:
                if isinstance(result.final_output, str):
                    output_preview = result.final_output[:80]
                elif isinstance(result.final_output, list):
                    output_preview = str(result.final_output[:3])
                elif isinstance(result.final_output, dict):
                    keys = list(result.final_output.keys())[:5]
                    output_preview = f"dict(keys={keys})"

            return BenchmarkResult(
                task_id=task_id,
                level=level,
                executability=1.0 if result.success else 0.0,
                chemical_correctness=chem_score,
                quality_score=quality,
                execution_time_s=round(execution_time, 2),
                error="" if result.success else "No successful round",
                output_preview=output_preview,
            )

        except Exception as e:
            return BenchmarkResult(
                task_id=task_id,
                level=level,
                executability=0.0,
                chemical_correctness=0.0,
                quality_score=0.0,
                execution_time_s=time.time() - start,
                error=str(e)[:200],
            )

    def run_all(
        self,
        pipeline,
        output_dir: str | Path | None = None,
    ) -> BenchmarkReport:
        """
        Run all benchmark tasks and return aggregate report.
        """
        from collections import defaultdict

        results = []
        by_level = defaultdict(lambda: {"n": 0, "n_exe": 0, "n_chem": 0, "n_qual": 0})

        for task in self.tasks:
            if self.verbose:
                print(f"  Running {task['id']} (L{task['level']})...")

            r = self.run_single(task, pipeline)
            results.append(r)

            level = r.level
            by_level[level]["n"] += 1
            if r.executability > 0:
                by_level[level]["n_exe"] += 1
            if r.chemical_correctness >= 0.8:
                by_level[level]["n_chem"] += 1
            if r.quality_score >= 0.75:
                by_level[level]["n_qual"] += 1

        n_total = len(results)
        n_exe = sum(1 for r in results if r.executability > 0)
        n_chem = sum(1 for r in results if r.chemical_correctness >= 0.8)
        n_qual = sum(1 for r in results if r.quality_score >= 0.75)

        # Per-level breakdown
        level_summary = {}
        for level, stats in sorted(by_level.items()):
            level_summary[level] = {
                "n": stats["n"],
                "executability_rate": stats["n_exe"] / max(stats["n"], 1),
                "chemical_correctness_rate": stats["n_chem"] / max(stats["n"], 1),
                "quality_rate": stats["n_qual"] / max(stats["n"], 1),
            }

        report = BenchmarkReport(
            n_total=n_total,
            n_executable=n_exe,
            n_chem_correct=n_chem,
            n_quality=n_qual,
            pass_at_1=(n_exe / n_total) * (n_chem / n_total) if n_total > 0 else 0.0,
            executability_rate=n_exe / n_total if n_total > 0 else 0.0,
            chemical_correctness_rate=n_chem / n_total if n_total > 0 else 0.0,
            quality_rate=n_qual / n_total if n_total > 0 else 0.0,
            results=results,
            by_level=level_summary,
        )

        # Save to disk
        if output_dir:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            results_path = out_path / "benchmark_results.json"
            with open(results_path, 'w') as f:
                json.dump(self._report_to_dict(report), f, indent=2, default=str)
            if self.verbose:
                print(f"Saved: {results_path}")

        return report

    def _report_to_dict(self, report: BenchmarkReport) -> dict:
        return {
            "summary": {
                "n_total": report.n_total,
                "n_executable": report.n_executable,
                "n_chem_correct": report.n_chem_correct,
                "n_quality": report.n_quality,
                "pass_at_1": round(report.pass_at_1, 4),
                "executability_rate": round(report.executability_rate, 4),
                "chemical_correctness_rate": round(report.chemical_correctness_rate, 4),
                "quality_rate": round(report.quality_rate, 4),
            },
            "by_level": {str(k): v for k, v in report.by_level.items()},
            "tasks": [
                {
                    "id": r.task_id,
                    "level": r.level,
                    "executability": r.executability,
                    "chemical_correctness": r.chemical_correctness,
                    "quality_score": r.quality_score,
                    "execution_time_s": r.execution_time_s,
                    "error": r.error,
                    "output_preview": r.output_preview,
                }
                for r in report.results
            ],
        }


# ============================================================
# Convenience CLI
# ============================================================

def run_benchmarks(
    llm_provider: str = "groq",
    model: str = "llama-3.3-70b-versatile",
    max_rounds: int = 3,
    output_dir: str = "./benchmark_results",
    verbose: bool = True,
):
    """
    Run all benchmarks with the specified LLM.

    Example:
        python pipeline_benchmarks.py --provider groq --model llama-3.3-70b-versatile
    """
    from incremental_repair_pipeline import IncrementalRepairPipeline, LLMClient

    llm = LLMClient(provider=llm_provider, model=model)
    pipeline = IncrementalRepairPipeline(llm_client=llm, max_rounds=max_rounds, verbose=verbose)
    benchmark = PipelineBenchmark(verbose=verbose)

    report = benchmark.run_all(pipeline, output_dir=output_dir)

    print(f"\n{'='*60}")
    print("BENCHMARK REPORT")
    print(f"{'='*60}")
    print(f"Total tasks:     {report.n_total}")
    print(f"Executability:   {report.n_executable}/{report.n_total} = {report.executability_rate:.1%}")
    print(f"Chem correct:    {report.n_chem_correct}/{report.n_total} = {report.chemical_correctness_rate:.1%}")
    print(f"Quality ≥0.75:   {report.n_quality}/{report.n_total} = {report.quality_rate:.1%}")
    print(f"Pass@1 (est):    {report.pass_at_1:.1%}")
    print()
    print("By Level:")
    for level, stats in sorted(report.by_level.items()):
        print(f"  L{level}: n={stats['n']}  "
              f"exe={stats['executability_rate']:.0%}  "
              f"chem={stats['chemical_correctness_rate']:.0%}  "
              f"qual={stats['quality_rate']:.0%}")

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="groq", choices=["groq", "openai", "ollama"])
    parser.add_argument("--model", default="llama-3.3-70b-versatile")
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--output-dir", default="./benchmark_results")
    args = parser.parse_args()

    run_benchmarks(
        llm_provider=args.provider,
        model=args.model,
        max_rounds=args.max_rounds,
        output_dir=args.output_dir,
    )
