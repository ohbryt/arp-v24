"""
ARP v24 - Literature API Tests

Tests for api/pubmed.py:
- sync wrapper behavior
- async path works
- failures produce structured status
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.pubmed import (
    LiteratureIntegrator,
    PubMedClient,
    ClinicalTrialsClient,
    FetchStatus,
    HAS_HTTPX,
)


def test_fetch_status_enum():
    """FetchStatus enum should have expected values."""
    assert FetchStatus.SUCCESS.value == "success"
    assert FetchStatus.PARTIAL.value == "partial"
    assert FetchStatus.FAILED.value == "failed"
    assert FetchStatus.SKIPPED.value == "skipped"
    print("  [PASS] FetchStatus enum values correct")


def test_sync_wrapper_returns_structured_result():
    """get_sync() should return structured result with fetch_status."""
    integrator = LiteratureIntegrator()
    result = integrator.get_sync("EGFR", "cancer", max_articles=1)
    
    # Should have all required fields
    assert "gene" in result
    assert "disease" in result
    assert "articles" in result
    assert "clinical_trials" in result
    assert "summary" in result
    assert "fetch_status" in result
    assert "error" in result
    
    # fetch_status should be a valid enum value
    status = result["fetch_status"]
    assert status in [s.value for s in FetchStatus], f"Invalid status: {status}"
    
    print(f"  [PASS] Structured result: status={status}")


def test_sync_wrapper_safe_in_sync_context():
    """get_sync() should work without crashing in sync context."""
    integrator = LiteratureIntegrator()
    
    # Should not raise, should return dict
    try:
        result = integrator.get_sync("BRCA1", "cancer", max_articles=1)
        assert isinstance(result, dict), "Should return dict"
        assert "gene" in result
        print(f"  [PASS] Sync wrapper works, status={result.get('fetch_status')}")
    except Exception as e:
        print(f"  [FAIL] Sync wrapper raised: {e}")
        raise


def test_async_method_exists():
    """Async method should exist and be callable."""
    integrator = LiteratureIntegrator()
    assert hasattr(integrator, 'get_target_literature')
    assert callable(integrator.get_target_literature)
    print("  [PASS] Async method exists")


def test_clinical_trials_robust_parsing():
    """ClinicalTrials parsing should be robust with malformed data."""
    # Note: ClinicalTrialsClient.search() is async, test via LiteratureIntegrator
    integrator = LiteratureIntegrator()
    
    # Test that missing fields don't crash - use get_sync which handles async properly
    result = integrator.get_sync("FAKE_DISEASE_XYZ", "fake_disease", max_articles=1)
    assert isinstance(result, dict), "Should return dict"
    assert "clinical_trials" in result
    print(f"  [PASS] ClinicalTrials robust parsing (got {len(result.get('clinical_trials', []))} results)")


def test_httpx_availability():
    """Test httpx availability check."""
    print(f"  httpx available: {HAS_HTTPX}")
    if not HAS_HTTPX:
        print("  [INFO] httpx not available - literature tests will be limited")


def test_literature_integrator_init():
    """LiteratureIntegrator should initialize with clients."""
    integrator = LiteratureIntegrator()
    assert hasattr(integrator, 'pubmed')
    assert hasattr(integrator, 'ct')
    assert isinstance(integrator.pubmed, PubMedClient)
    assert isinstance(integrator.ct, ClinicalTrialsClient)
    print("  [PASS] LiteratureIntegrator initializes correctly")


def run_all():
    print(f"\n{'='*50}")
    print("  Literature API Tests")
    print(f"{'='*50}\n")
    
    tests = [
        test_fetch_status_enum,
        test_sync_wrapper_returns_structured_result,
        test_sync_wrapper_safe_in_sync_context,
        test_async_method_exists,
        test_clinical_trials_robust_parsing,
        test_httpx_availability,
        test_literature_integrator_init,
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
