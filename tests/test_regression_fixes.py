"""
ARP v24 - Regression Tests for Bug Fixes

Tests for:
1. Engine 3 modality typing (EGFR compounds = small_molecule)
2. Affinity-aware ranking
3. asyncio.run() safety in sync wrapper
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.candidate_engine import CandidateEngine, COMPOUND_DATABASE


def test_egfr_modality_is_small_molecule():
    """Bug fix #1: EGFR kinase inhibitors must be classified as small_molecule, not biologic."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    assert result.total_candidates > 0, "No candidates found for EGFR"
    
    for c in result.candidates:
        assert c.modality == "small_molecule", (
            f"{c.name} has modality '{c.modality}', expected 'small_molecule'. "
            f"EGFR inhibitors are small molecules, not biologics!"
        )
    
    print(f"  [PASS] EGFR compounds: all classified as small_molecule")
    for c in result.candidates:
        print(f"        - {c.name}: {c.modality}")


def test_pembrolizumab_is_antibody():
    """PD-1 antibodies should remain classified as antibody/biologic."""
    engine = CandidateEngine()
    result = engine.generate_candidates("CD274", "cancer", modality="antibody")
    
    assert result.total_candidates > 0, "No candidates found for CD274"
    
    for c in result.candidates:
        assert c.modality == "antibody", (
            f"{c.name} has modality '{c.modality}', expected 'antibody'"
        )
    
    print(f"  [PASS] CD274 (PD-1) compounds: all classified as antibody")


def test_affinity_affects_ranking():
    """Bug fix #2: Affinity should influence candidate ranking."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    assert result.total_candidates > 0, "No candidates found"
    
    # Check that affinity is stored and used
    osimertinib = next((c for c in result.candidates if c.name == "Osimertinib"), None)
    erlotinib = next((c for c in result.candidates if c.name == "Erlotinib"), None)
    
    assert osimertinib is not None, "Osimertinib not found"
    assert erlotinib is not None, "Erlotinib not found"
    
    # Osimertinib has better affinity (0.7 nM) than Erlotinib (2.0 nM)
    # After affinity-aware scoring, it should rank higher
    osimertinib.calculate_scores()
    erlotinib.calculate_scores()
    
    assert osimertinib.affinity == 0.7, f"Osimertinib affinity: {osimertinib.affinity}"
    assert erlotinib.affinity == 2.0, f"Erlotinib affinity: {erlotinib.affinity}"
    
    # Affinity potency score should be better for lower nM
    assert osimertinib.affinity_potency_score > erlotinib.affinity_potency_score, (
        f"Osimertinib potency ({osimertinib.affinity_potency_score:.3f}) should be > "
        f"Erlotinib ({erlotinib.affinity_potency_score:.3f})"
    )
    
    print(f"  [PASS] Affinity-aware ranking:")
    for c in result.candidates:
        print(f"        - {c.name}: affinity={c.affinity} nM, "
              f"potency_score={c.affinity_potency_score:.3f}, "
              f"final={c.composite_score:.3f}")


def test_affinity_normalization():
    """Test that affinity normalization works correctly."""
    engine = CandidateEngine()
    
    # Create a test candidate
    from core.candidate_engine import CandidateCompound
    import math
    
    # Very potent: 0.1 nM should give ~0.97
    c1 = CandidateCompound(compound_id="test1", name="test1", affinity=0.1)
    s1 = c1._normalize_affinity_to_potency_score()
    
    # Moderate: 10 nM should give ~0.67
    c2 = CandidateCompound(compound_id="test2", name="test2", affinity=10.0)
    s2 = c2._normalize_affinity_to_potency_score()
    
    # Weak: 1000 nM should give ~0.33
    c3 = CandidateCompound(compound_id="test3", name="test3", affinity=1000.0)
    s3 = c3._normalize_affinity_to_potency_score()
    
    # Verify ordering
    assert s1 > s2 > s3, f"Affinity scores should decrease with higher nM: {s1:.3f} > {s2:.3f} > {s3:.3f}"
    
    # Verify range
    assert 0.0 <= s1 <= 1.0, f"Potency score should be 0-1, got {s1}"
    assert 0.0 <= s2 <= 1.0, f"Potency score should be 0-1, got {s2}"
    assert 0.0 <= s3 <= 1.0, f"Potency score should be 0-1, got {s3}"
    
    print(f"  [PASS] Affinity normalization:")
    print(f"        - 0.1 nM → potency={s1:.3f}")
    print(f"        - 10 nM  → potency={s2:.3f}")
    print(f"        - 1000 nM → potency={s3:.3f}")


def test_score_breakdown_exists():
    """Score breakdown should be present in output."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    assert result.total_candidates > 0, "No candidates"
    
    c = result.candidates[0]
    d = c.to_dict()
    
    assert "score_breakdown" in d, "score_breakdown missing from output"
    assert "intrinsic_score" in d["score_breakdown"], "intrinsic_score missing"
    assert "affinity_potency_score" in d["score_breakdown"], "affinity_potency_score missing"
    assert "modality_fit_score" in d["score_breakdown"], "modality_fit_score missing"
    assert "final_adjusted_score" in d["score_breakdown"], "final_adjusted_score missing"
    
    print(f"  [PASS] Score breakdown present:")
    for k, v in d["score_breakdown"].items():
        print(f"        - {k}: {v}")


def test_bimagrumab_is_antibody_not_small_molecule():
    """MSTN antibodies should be classified as antibody, not small_molecule."""
    engine = CandidateEngine()
    result = engine.generate_candidates("MSTN", "sarcopenia", modality="antibody")
    
    assert result.total_candidates > 0, "No candidates found for MSTN"
    
    bimagrumab = next((c for c in result.candidates if c.name == "Bimagrumab"), None)
    assert bimagrumab is not None, "Bimagrumab not found"
    assert bimagrumab.modality == "antibody", (
        f"Bimagrumab has modality '{bimagrumab.modality}', expected 'antibody'"
    )
    
    print(f"  [PASS] Bimagrumab correctly classified as: {bimagrumab.modality}")


def test_modality_compat_matrix():
    """Same modality should have perfect fit (1.0)."""
    from core.candidate_engine import MODALITY_COMPAT
    
    # Small molecule requesting small molecule = 1.0
    assert MODALITY_COMPAT[("small_molecule", "small_molecule")] == 1.0, (
        "Same modality should have fit = 1.0"
    )
    
    # Antibody requesting antibody = 1.0
    assert MODALITY_COMPAT[("antibody", "antibody")] == 1.0, (
        "Antibody requesting antibody should have fit = 1.0"
    )
    
    # Cross-modality should be less than 1.0
    assert MODALITY_COMPAT[("small_molecule", "antibody")] < 1.0, (
        "Cross-modality should have fit < 1.0"
    )
    
    print(f"  [PASS] Modality compatibility matrix:")
    print(f"        - small_molecule → small_molecule: {MODALITY_COMPAT[('small_molecule', 'small_molecule')]}")
    print(f"        - antibody → antibody: {MODALITY_COMPAT[('antibody', 'antibody')]}")
    print(f"        - small_molecule → antibody: {MODALITY_COMPAT[('small_molecule', 'antibody')]}")


def test_peptide_modality():
    """Peptides like Semaglutide should be classified as peptide."""
    engine = CandidateEngine()
    result = engine.generate_candidates("GLP1R", "masld", modality="peptide")
    
    assert result.total_candidates > 0, "No candidates found for GLP1R"
    
    semaglutide = next((c for c in result.candidates if c.name == "Semaglutide"), None)
    assert semaglutide is not None, "Semaglutide not found"
    assert semaglutide.modality == "peptide", (
        f"Semaglutide has modality '{semaglutide.modality}', expected 'peptide'"
    )
    
    print(f"  [PASS] Semaglutide correctly classified as: {semaglutide.modality}")


def test_asyncio_safe_sync_wrapper():
    """Test that get_sync is safe to call from sync context."""
    import asyncio
    
    # This should not raise or hang even if called from sync context
    from api.pubmed import PubMedClient, LiteratureIntegrator
    
    # Create integrator
    integrator = LiteratureIntegrator()
    
    # Call sync wrapper - should not crash
    result = integrator.get_sync("EGFR", "cancer", max_articles=1)
    
    assert "gene" in result, "Result should have 'gene' key"
    assert "disease" in result, "Result should have 'disease' key"
    assert "articles" in result, "Result should have 'articles' key"
    assert "error" not in result or result.get("error") is None, f"Unexpected error: {result.get('error')}"
    
    print(f"  [PASS] get_sync() is safe for sync context")


def run_all():
    print(f"\n{'='*60}")
    print("  ARP v24 Regression Tests - Bug Fixes")
    print(f"{'='*60}\n")
    
    tests = [
        # Bug #1: Modality typing
        test_egfr_modality_is_small_molecule,
        test_pembrolizumab_is_antibody,
        test_bimagrumab_is_antibody_not_small_molecule,
        test_peptide_modality,
        test_modality_compat_matrix,
        # Bug #2: Affinity-aware ranking
        test_affinity_affects_ranking,
        test_affinity_normalization,
        # Bug #3: asyncio safety
        test_asyncio_safe_sync_wrapper,
        # Explainability
        test_score_breakdown_exists,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*60}\n")
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
