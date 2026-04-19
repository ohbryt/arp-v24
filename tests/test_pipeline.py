"""
ARP v24 - Test Suite Runner

Run all test modules:
    python tests/test_pipeline.py
"""

import sys
import os

def run_all_tests():
    """Run all test modules."""
    test_modules = [
        ("Candidate Engine", "tests.test_candidate_engine"),
        ("Literature API", "tests.test_literature_api"),
        ("Pipeline Integration", "tests.test_pipeline_integration"),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for name, module_name in test_modules:
        print(f"\n{'='*60}")
        print(f"  Running: {name}")
        print(f"{'='*60}\n")
        
        try:
            # Import the module
            module = __import__(module_name, fromlist=[''])
            
            # Call run_all() - it returns (passed, failed) tuple
            if hasattr(module, 'run_all'):
                result = module.run_all()
                # Handle both tuple and bool returns
                if isinstance(result, tuple):
                    passed, failed = result
                else:
                    passed = module.run_all()
                    failed = 0 if passed else 1
                total_passed += passed
                total_failed += failed
            else:
                print(f"  [SKIP] No run_all() function")
        except Exception as e:
            print(f"  [ERROR] Failed to run {module_name}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"  FINAL RESULTS")
    print(f"{'='*60}")
    print(f"  Total passed: {total_passed}")
    print(f"  Total failed: {total_failed}")
    print(f"{'='*60}\n")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)