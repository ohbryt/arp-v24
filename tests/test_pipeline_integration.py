"""
ARP v24 - Pipeline Integration Tests

Tests for:
- with_literature=True returns structured status
- pipeline result contains warnings/errors/status fields
- core end-to-end flow still passes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import ARPv24Pipeline, PipelineResult, LiteratureStatus
from core.candidate_engine import CandidateEngine, COMPOUND_DATABASE


def test_weights_sum_to_one():
    """All disease weight configs must sum to 1.0."""
    from core.weights import get_disease_weights, Disease
    for d in Disease:
        w = get_disease_weights(d)
        assert w.validate(), f"{d.value} weights don't sum to 1.0"
    print("  [PASS] All weight configs sum to 1.0")


def test_target_registry_complete():
    """Every disease must have targets in the registry."""
    from core.scoring_engine import TARGET_REGISTRY
    from core.schema import DiseaseType
    for dt in DiseaseType:
        targets = TARGET_REGISTRY.get(dt.value, {})
        assert len(targets) >= 3, f"{dt.value} has only {len(targets)} targets"
    print(f"  [PASS] Target registry: {sum(len(v) for v in TARGET_REGISTRY.values())} targets")


def test_engine1_all_diseases():
    """Engine 1 must produce ranked targets for every disease."""
    from core.scoring_engine import DiseaseEngine
    from core.schema import DiseaseType
    
    engine = DiseaseEngine()
    for dt in DiseaseType:
        result = engine.prioritize_targets(dt)
        assert len(result.targets) >= 3, f"{dt.value}: only {len(result.targets)} targets"
        assert result.targets[0].priority_score > 0
        assert result.targets[0].rank == 1
        scores = [t.priority_score for t in result.targets]
        assert scores == sorted(scores, reverse=True)
    print("  [PASS] Engine 1: All 5 diseases produce ranked targets")


def test_engine2_routing():
    """Engine 2 must route targets to modalities."""
    from core.scoring_engine import DiseaseEngine
    from core.modality_routing import ModalityRouter
    from core.schema import DiseaseType
    
    engine1 = DiseaseEngine()
    router = ModalityRouter()
    
    for dt in DiseaseType:
        result = engine1.prioritize_targets(dt)
        top = result.targets[0]
        routing = router.route_target(top, dt)
        assert routing.recommended_modalities
        assert routing.recommended_modalities[0].recommended is True
        assert routing.get_top_modality() is not None
    print("  [PASS] Engine 2: All diseases route to modalities")


def test_engine3_candidates():
    """Engine 3 must return candidates for known targets."""
    engine = CandidateEngine()
    found = 0
    for disease, targets in COMPOUND_DATABASE.items():
        for gene in targets:
            result = engine.generate_candidates(gene, disease)
            assert result.total_candidates > 0, f"{gene}/{disease}: no candidates"
            for c in result.candidates:
                assert c.composite_score > 0
            found += result.total_candidates
    print(f"  [PASS] Engine 3: {found} candidates across all disease-target pairs")


def test_engine3_unknown_target():
    """Engine 3 must handle unknown targets gracefully."""
    engine = CandidateEngine()
    result = engine.generate_candidates("FAKE_GENE", "masld")
    assert result.total_candidates == 0
    print("  [PASS] Engine 3: Unknown target returns empty (no crash)")


def test_assay_recommendations():
    """Assay engine must return recommendations."""
    from core.modality_routing import AssayEngine
    from core.schema import DiseaseType
    
    engine = AssayEngine()
    for dt in DiseaseType:
        assays = engine.get_assays(dt)
        assert len(assays) >= 1
    print("  [PASS] Assay engine: All diseases have recommendations")


def test_pipeline_result_has_structured_status():
    """PipelineResult must have literature_status field."""
    assert hasattr(PipelineResult, '__dataclass_fields__')
    fields = PipelineResult.__dataclass_fields__
    
    # Check for structured status fields
    assert 'literature_status' in fields, "literature_status missing"
    assert 'literature_error' in fields, "literature_error missing"
    assert 'literature_summary' in fields, "literature_summary missing"
    assert 'warnings' in fields, "warnings missing"
    assert 'errors' in fields, "errors missing"
    
    print("  [PASS] PipelineResult has structured status fields")


def test_pipeline_literature_status_in_result():
    """run(with_literature=True) should return structured literature status."""
    pipeline = ARPv24Pipeline()
    
    # Run with literature (may not fetch real data but should not crash)
    result = pipeline.run("masld", top_n=3, with_literature=True)
    
    # Check structured status fields exist in result
    assert hasattr(result, 'literature_status')
    assert hasattr(result, 'literature_error')
    assert hasattr(result, 'literature_summary')
    
    # Status should be a LiteratureStatus enum
    assert isinstance(result.literature_status, LiteratureStatus)
    
    print(f"  [PASS] Literature status: {result.literature_status.value}")


def test_pipeline_warnings_in_result():
    """Pipeline result should have warnings list."""
    pipeline = ARPv24Pipeline()
    result = pipeline.run("cancer", top_n=3, run_engine3=True)
    
    assert hasattr(result, 'warnings')
    assert isinstance(result.warnings, list)
    
    print(f"  [PASS] Warnings field exists: {len(result.warnings)} warnings")


def test_pipeline_to_dict_has_status():
    """to_dict() should include status fields."""
    pipeline = ARPv24Pipeline()
    result = pipeline.run("sarcopenia", top_n=3)
    
    d = result.to_dict()
    
    assert 'literature_status' in d, "literature_status missing from to_dict"
    assert 'warnings' in d, "warnings missing from to_dict"
    assert 'errors' in d, "errors missing from to_dict"
    assert 'literature_summary' in d, "literature_summary missing from to_dict"
    
    print(f"  [PASS] to_dict() includes status: {d['literature_status']}")


def test_engine2_vs_engine3_modality_comparison():
    """Engine 2 modality should be comparable to Engine 3 candidate modality."""
    pipeline = ARPv24Pipeline()
    result = pipeline.run("cancer", top_n=5, run_engine2=True, run_engine3=True)
    
    d = result.to_dict()
    
    # Engine 2 modalities should be in output
    assert 'engine2_modalities' in d
    
    # Engine 3 candidates with modality should be in output
    assert 'engine3_candidates' in d
    
    # Top targets should have both
    for target in d['top_targets'][:2]:
        assert 'engine2_modality' in target
        assert 'engine3_top_candidate' in target
    
    print(f"  [PASS] Modality comparison fields present in output")


def test_full_pipeline():
    """Full pipeline integration test."""
    pipeline = ARPv24Pipeline()
    
    for disease in ["masld", "sarcopenia", "lung_fibrosis", "heart_failure", "cancer"]:
        result = pipeline.run(disease, top_n=5, run_engine2=True, run_engine3=True)
        assert len(result.targets) >= 3
        assert result.execution_time_seconds < 5.0
        d = result.to_dict()
        assert d["pipeline"] == "ARP v24"
        assert d["targets_returned"] >= 3
    print("  [PASS] Full pipeline: All 5 diseases run end-to-end")


def test_single_target_analysis():
    """Single target deep analysis."""
    from pipeline import analyze_target
    
    result = analyze_target("THRB", "masld")
    assert "target" in result
    assert "modality_routing" in result
    assert "candidates" in result
    assert result["target"]["gene_name"] == "THRB"
    print("  [PASS] Single target analysis: THRB/MASLD")


def run_all():
    print(f"\n{'='*50}")
    print("  ARP v24 Pipeline Integration Tests")
    print(f"{'='*50}\n")
    
    tests = [
        # Core engine tests
        test_weights_sum_to_one,
        test_target_registry_complete,
        test_engine1_all_diseases,
        test_engine2_routing,
        test_engine3_candidates,
        test_engine3_unknown_target,
        test_assay_recommendations,
        # Pipeline structured status tests
        test_pipeline_result_has_structured_status,
        test_pipeline_literature_status_in_result,
        test_pipeline_warnings_in_result,
        test_pipeline_to_dict_has_status,
        test_engine2_vs_engine3_modality_comparison,
        # Integration tests
        test_full_pipeline,
        test_single_target_analysis,
    ]
    
    passed = failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {t.__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
