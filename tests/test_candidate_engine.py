"""
ARP v24 - Candidate Engine Tests

Tests for Engine 3 (Candidate Engine):
- Modality typing correctness
- Affinity-aware ranking
- Score breakdown
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.candidate_engine import CandidateEngine, COMPOUND_DATABASE


def test_egfr_modality_is_small_molecule():
    """EGFR kinase inhibitors must be classified as small_molecule, not biologic."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    assert result.total_candidates > 0, "No candidates found for EGFR"
    
    for c in result.candidates:
        assert c.modality == "small_molecule", (
            f"{c.name} has modality '{c.modality}', expected 'small_molecule'"
        )
    
    print(f"  [PASS] EGFR compounds: all small_molecule")
    for c in result.candidates:
        print(f"        - {c.name}: {c.modality}")


def test_pembrolizumab_is_antibody():
    """PD-1 antibodies should remain classified as antibody."""
    engine = CandidateEngine()
    result = engine.generate_candidates("CD274", "cancer", modality="antibody")
    
    assert result.total_candidates > 0, "No candidates found for CD274"
    
    for c in result.candidates:
        assert c.modality == "antibody", (
            f"{c.name} has modality '{c.modality}', expected 'antibody'"
        )
    
    print(f"  [PASS] CD274 compounds: all antibody")


def test_bimagrumab_is_antibody():
    """MSTN antibodies should be classified as antibody."""
    engine = CandidateEngine()
    result = engine.generate_candidates("MSTN", "sarcopenia", modality="antibody")
    
    bimagrumab = next((c for c in result.candidates if c.name == "Bimagrumab"), None)
    assert bimagrumab is not None, "Bimagrumab not found"
    assert bimagrumab.modality == "antibody", (
        f"Bimagrumab has modality '{bimagrumab.modality}', expected 'antibody'"
    )
    
    print(f"  [PASS] Bimagrumab: {bimagrumab.modality}")


def test_semaglutide_is_peptide():
    """GLP1R peptides like Semaglutide should be classified as peptide."""
    engine = CandidateEngine()
    result = engine.generate_candidates("GLP1R", "masld", modality="peptide")
    
    semaglutide = next((c for c in result.candidates if c.name == "Semaglutide"), None)
    assert semaglutide is not None, "Semaglutide not found"
    assert semaglutide.modality == "peptide", (
        f"Semaglutide has modality '{semaglutide.modality}', expected 'peptide'"
    )
    
    print(f"  [PASS] Semaglutide: {semaglutide.modality}")


def test_affinity_affects_ranking():
    """Affinity should influence candidate ranking."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    osimertinib = next((c for c in result.candidates if c.name == "Osimertinib"), None)
    erlotinib = next((c for c in result.candidates if c.name == "Erlotinib"), None)
    
    assert osimertinib is not None, "Osimertinib not found"
    assert erlotinib is not None, "Erlotinib not found"
    
    osimertinib.calculate_scores()
    erlotinib.calculate_scores()
    
    # Lower nM = better potency = higher score
    assert osimertinib.affinity_potency_score > erlotinib.affinity_potency_score, (
        f"Osimertinib potency ({osimertinib.affinity_potency_score:.3f}) should be > "
        f"Erlotinib ({erlotinib.affinity_potency_score:.3f})"
    )
    
    print(f"  [PASS] Affinity ranking:")
    for c in result.candidates:
        print(f"        - {c.name}: {c.affinity} nM → potency={c.affinity_potency_score:.3f}")


def test_affinity_normalization():
    """Test log-scale affinity normalization."""
    from core.candidate_engine import CandidateCompound
    
    # Very potent: 0.1 nM → high score
    c1 = CandidateCompound(compound_id="t1", name="t1", affinity=0.1)
    s1 = c1._normalize_affinity_to_potency_score()
    
    # Weak: 1000 nM → low score
    c2 = CandidateCompound(compound_id="t2", name="t2", affinity=1000.0)
    s2 = c2._normalize_affinity_to_potency_score()
    
    assert s1 > s2, f"Lower nM should give higher score: {s1:.3f} vs {s2:.3f}"
    assert 0.0 <= s1 <= 1.0 and 0.0 <= s2 <= 1.0
    
    print(f"  [PASS] Affinity normalization: 0.1nM→{s1:.3f}, 1000nM→{s2:.3f}")


def test_score_breakdown_exists():
    """Score breakdown should be present in output."""
    engine = CandidateEngine()
    result = engine.generate_candidates("EGFR", "cancer", modality="small_molecule")
    
    c = result.candidates[0]
    d = c.to_dict()
    
    assert "score_breakdown" in d, "score_breakdown missing"
    for key in ["intrinsic_score", "affinity_potency_score", "modality_fit_score", "final_adjusted_score"]:
        assert key in d["score_breakdown"], f"{key} missing from breakdown"
    
    print(f"  [PASS] Score breakdown: {d['score_breakdown']}")


def test_modality_compat_same_is_1():
    """Same modality should have perfect fit (1.0)."""
    from core.candidate_engine import MODALITY_COMPAT
    
    assert MODALITY_COMPAT[("small_molecule", "small_molecule")] == 1.0
    assert MODALITY_COMPAT[("antibody", "antibody")] == 1.0
    assert MODALITY_COMPAT[("peptide", "peptide")] == 1.0
    
    print(f"  [PASS] Same modality = 1.0")


def run_all():
    print(f"\n{'='*50}")
    print("  Candidate Engine Tests")
    print(f"{'='*50}\n")
    
    tests = [
        test_egfr_modality_is_small_molecule,
        test_pembrolizumab_is_antibody,
        test_bimagrumab_is_antibody,
        test_semaglutide_is_peptide,
        test_affinity_affects_ranking,
        test_affinity_normalization,
        test_score_breakdown_exists,
        test_modality_compat_same_is_1,
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
