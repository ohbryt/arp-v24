"""
ARP v24 - End-to-end smoke tests

Tests all three engines across all 5 diseases without network calls.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.schema import DiseaseType, TargetScores, TargetDossier, ScoringEngineConfig
from core.weights import Disease, get_disease_weights, get_penalties_for_disease, WeightConfig
from core.scoring_engine import DiseaseEngine, TargetScorer, TARGET_REGISTRY, DISEASE_CONTEXTS
from core.modality_routing import ModalityRouter, AssayEngine
from core.candidate_engine import CandidateEngine, COMPOUND_DATABASE


def test_weights_sum_to_one():
    """All disease weight configs must sum to 1.0"""
    for d in Disease:
        w = get_disease_weights(d)
        assert w.validate(), f"{d.value} weights don't sum to 1.0"
    print("  [PASS] All weight configs sum to 1.0")


def test_target_registry_complete():
    """Every disease must have targets in the registry"""
    for dt in DiseaseType:
        targets = TARGET_REGISTRY.get(dt.value, {})
        assert len(targets) >= 3, f"{dt.value} has only {len(targets)} targets"
    print(f"  [PASS] Target registry: {sum(len(v) for v in TARGET_REGISTRY.values())} targets across {len(TARGET_REGISTRY)} diseases")


def test_engine1_all_diseases():
    """Engine 1 must produce ranked targets for every disease"""
    engine = DiseaseEngine()
    for dt in DiseaseType:
        result = engine.prioritize_targets(dt)
        assert len(result.targets) >= 3, f"{dt.value}: only {len(result.targets)} targets"
        assert result.targets[0].priority_score > 0, f"{dt.value}: zero score"
        assert result.targets[0].rank == 1, f"{dt.value}: rank not assigned"
        # Scores should be ordered
        scores = [t.priority_score for t in result.targets]
        assert scores == sorted(scores, reverse=True), f"{dt.value}: not sorted"
    print("  [PASS] Engine 1: All 5 diseases produce ranked targets")


def test_engine2_routing():
    """Engine 2 must route targets to modalities"""
    engine1 = DiseaseEngine()
    router = ModalityRouter()

    for dt in DiseaseType:
        result = engine1.prioritize_targets(dt)
        top = result.targets[0]
        routing = router.route_target(top, dt)
        assert routing.recommended_modalities, f"{dt.value}: no modalities"
        assert routing.recommended_modalities[0].recommended is True
        assert routing.get_top_modality() is not None
    print("  [PASS] Engine 2: All diseases route to modalities")


def test_engine3_candidates():
    """Engine 3 must return candidates for known targets"""
    engine = CandidateEngine()
    found = 0
    for disease, targets in COMPOUND_DATABASE.items():
        for gene in targets:
            result = engine.generate_candidates(gene, disease)
            assert result.total_candidates > 0, f"{gene}/{disease}: no candidates"
            for c in result.candidates:
                assert c.composite_score > 0, f"{c.name}: zero score"
            found += result.total_candidates
    print(f"  [PASS] Engine 3: {found} candidates across all disease-target pairs")


def test_engine3_unknown_target():
    """Engine 3 must handle unknown targets gracefully"""
    engine = CandidateEngine()
    result = engine.generate_candidates("FAKE_GENE", "masld")
    assert result.total_candidates == 0
    print("  [PASS] Engine 3: Unknown target returns empty (no crash)")


def test_assay_recommendations():
    """Assay engine must return recommendations"""
    engine = AssayEngine()
    for dt in DiseaseType:
        assays = engine.get_assays(dt)
        assert len(assays) >= 1, f"{dt.value}: no assays"
    print("  [PASS] Assay engine: All diseases have recommendations")


def test_full_pipeline():
    """Full pipeline integration test"""
    from pipeline import ARPv24Pipeline
    pipeline = ARPv24Pipeline()

    for disease in ["masld", "sarcopenia", "lung_fibrosis", "heart_failure", "cancer"]:
        result = pipeline.run(disease, top_n=5, run_engine2=True, run_engine3=True)
        assert len(result.targets) >= 3
        assert result.execution_time_seconds < 5.0  # Should be fast
        d = result.to_dict()
        assert d["pipeline"] == "ARP v24"
        assert d["targets_returned"] >= 3
    print("  [PASS] Full pipeline: All 5 diseases run end-to-end")


def test_single_target_analysis():
    """Single target deep analysis"""
    from pipeline import analyze_target
    result = analyze_target("THRB", "masld")
    assert "target" in result
    assert "modality_routing" in result
    assert "candidates" in result
    assert result["target"]["gene_name"] == "THRB"
    print("  [PASS] Single target analysis: THRB/MASLD")


def run_all():
    print(f"\n{'='*50}")
    print("  ARP v24 Smoke Tests")
    print(f"{'='*50}\n")

    tests = [
        test_weights_sum_to_one,
        test_target_registry_complete,
        test_engine1_all_diseases,
        test_engine2_routing,
        test_engine3_candidates,
        test_engine3_unknown_target,
        test_assay_recommendations,
        test_full_pipeline,
        test_single_target_analysis,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
