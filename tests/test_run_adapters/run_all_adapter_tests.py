#!/usr/bin/env python3
"""
Adapter script to run all tests using adapters.

This script runs all the adapter test scripts in sequence.
"""

import os
import sys
import subprocess

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def run_script(script_path):
    """Run a test script and return the result."""
    print(f"\n{'='*80}\n")
    print(f"Running: {os.path.basename(script_path)}\n")
    result = subprocess.run(["python", script_path])
    return result.returncode

def main():
    """Main function to run all adapter tests."""
    # Get the directory path
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test scripts to run
    test_scripts = [
        os.path.join(test_dir, "run_token_utils_test.py"),
        os.path.join(test_dir, "run_text_utils_test.py"),
        os.path.join(test_dir, "run_file_utils_test.py"),
        os.path.join(test_dir, "run_code_executor_test.py"),
        os.path.join(test_dir, "run_latex_utils_test.py"),
        os.path.join(test_dir, "run_mlsolver_test.py"),
        os.path.join(test_dir, "run_workflow_methods_test.py"),
        os.path.join(test_dir, "run_integration_test.py"),
        os.path.join(test_dir, "run_arxiv_tests.py"),
        os.path.join(test_dir, "run_semantic_scholar_tests.py"),
        os.path.join(test_dir, "run_hf_data_test.py"),
        os.path.join(test_dir, "run_inference_tests.py"),
    ]
    
    # Track results
    results = {}
    all_passed = True
    
    # Run each test script
    for script in test_scripts:
        script_name = os.path.basename(script)
        returncode = run_script(script)
        results[script_name] = returncode == 0
        if returncode != 0:
            all_passed = False
    
    # Print summary
    print("\n" + "="*40)
    print("Test Summary:")
    print("="*40)
    for script_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{script_name}: {status}")
    print("="*40)
    
    if all_passed:
        print("\n✅ All adapter tests passed successfully!\n")
        return 0
    else:
        print("\n❌ Some adapter tests failed. See details above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())