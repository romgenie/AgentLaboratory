# Agent Laboratory Test Suite

## Overview
This test suite provides comprehensive testing for the Agent Laboratory project. The tests are organized into the following categories:

- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing interactions between components
- **Performance Tests**: Testing resource utilization and optimization
- **Implementation Tests**: Tests for testing infrastructure itself

Current test coverage is at **27%** with over 318 test cases across all modules. Several critical components including arxiv_search, code_executor, and query_model now have 95-100% test coverage.

## Test Structure
```
tests/
├── conftest.py                       # Common test fixtures and configuration
├── unit_tests/                       # Tests for individual components
│   ├── simple_test.py                # Basic sanity checks
│   ├── test_agent_advanced_behaviors.py # Tests for complex agent behaviors
│   ├── test_agent_classes.py         # Tests for agent base classes
│   ├── test_agent_tools/             # Tests for agent tools
│   │   ├── test_arxiv_search.py      # Tests for arXiv search tool
│   │   ├── test_code_executor.py     # Tests for code execution tool
│   │   ├── test_hf_data_search.py    # Tests for HuggingFace data search
│   │   └── test_semantic_scholar_search.py # Tests for Semantic Scholar search
│   ├── test_agent_types/             # Tests for specialized agent types
│   │   └── test_specialized_agents.py # Tests for agent specializations
│   ├── test_agents_phases/           # Tests for research phases
│   │   ├── test_data_preparation.py  # Tests for data preparation phase
│   │   └── test_running_experiments.py # Tests for running experiments phase
│   ├── test_file_utils.py            # Tests for file utilities
│   ├── test_inference_system.py      # Tests for inference system
│   ├── test_inference/               # Tests for inference components
│   │   ├── test_cost_estimation.py   # Tests for cost estimation
│   │   └── test_query_model.py       # Tests for model querying
│   ├── test_laboratory_workflow/     # Tests for workflow components
│   │   └── test_workflow_methods.py  # Tests for workflow methods
│   ├── test_mlsolver.py              # Tests for ML solver
│   ├── test_papersolver/             # Tests for paper solver components
│   │   └── test_papersolver.py       # Tests for paper solver functionality
│   ├── test_research_phases.py       # Tests for research phases
│   ├── test_text_utils.py            # Tests for text utilities
│   ├── test_token_utils.py           # Tests for token utilities
│   ├── test_tools_framework.py       # Tests for tools framework
│   ├── test_utils.py                 # Tests for utility functions
│   ├── test_workflow_phases.py       # Tests for workflow phases
├── integration_tests/                # Tests for component interactions
│   ├── test_agent_collaboration.py   # Tests for agent collaboration
│   ├── test_agent_consensus.py       # Tests for agent consensus
│   ├── test_application.py           # Tests for main application
│   ├── test_cli_interactions.py      # Tests for command-line interface
│   ├── test_end_to_end_phase_flow.py # Tests for end-to-end phase flow
│   ├── test_end_to_end_workflows.py  # Tests for end-to-end workflows
│   ├── test_external_api_integration.py # Tests for external API integration
│   └── test_real_world_scenarios.py  # Tests for real-world scenarios
├── performance_tests/                # Tests for performance
│   ├── test_inference_optimization.py # Tests for inference optimization
│   ├── test_memory_optimization.py   # Tests for memory optimization
│   ├── test_resource_utilization.py  # Tests for resource utilization
│   ├── test_throughput.py            # Tests for throughput
│   ├── test_token_optimization.py    # Tests for token usage optimization
│   └── test_long_running_stability.py # Tests for long-running stability
└── implementation_details/           # Tests for implementation details
    ├── pytest_config.py              # Pytest configuration
    ├── security_testing.py           # Tests for secure API key handling
    ├── test_coverage_setup.py        # Tests for coverage setup
    └── test_mocking_strategy.py      # Tests for mocking strategy
```

## Running Tests

### Running with Adapter-based Framework
The adapter-based testing framework provides a way to run tests without modifying the original code:

```bash
# Run all adapter tests
python -m tests.test_run_adapters.run_all_adapter_tests

# Run specific component tests
python -m tests.test_run_adapters.run_token_utils_test
python -m tests.test_run_adapters.run_inference_tests
python -m tests.test_run_adapters.run_integration_test
python -m tests.test_run_adapters.run_hf_data_test
python -m tests.test_run_adapters.run_arxiv_tests
python -m tests.test_run_adapters.run_semantic_scholar_tests
```

### Running with Pytest Directly
You can also run tests directly with pytest, but some tests may require the adapter framework:

### Running all unit tests
```bash
python -m pytest tests/unit_tests/ -v
```

### Running tests with coverage
```bash
python -m pytest --cov=./ tests/unit_tests/ -v
```

### Running specific test categories
```bash
# Run integration tests
python -m pytest tests/integration_tests/ -v

# Run performance tests
python -m pytest tests/performance_tests/ -v

# Run stability tests (requires psutil)
python -m pytest tests/performance_tests/test_long_running_stability.py -v
```

### Running a specific test file
```bash
python -m pytest tests/unit_tests/test_token_utils.py -v
```

## Using Test Adapters

The test suite includes adapter files that allow tests to run without modifying the original codebase. These adapters are located in the `test_adapters/` directory and provide compatibility interfaces for tests.

### Available adapters:
```
test_adapters/
├── __init__.py                       # Adapter package initialization
├── arxiv_adapter.py                  # Adapter for ArXiv search
├── code_executor_adapter.py          # Adapter for code execution
├── hf_data_adapter.py                # Adapter for HuggingFace data
├── inference_adapter.py              # Adapter for inference functionality
├── integration_adapter.py            # Adapter for end-to-end testing
├── laboratory_adapter.py             # Adapter for laboratory workflow
├── latex_utils_adapter.py            # Adapter for LaTeX utilities
├── mlsolver_adapter.py               # Adapter for ML solver
├── semantic_scholar_adapter.py       # Adapter for Semantic Scholar
├── text_utils_adapter.py             # Adapter for text utilities
├── token_adapter.py                  # Adapter for token utilities
├── utils_adapter.py                  # Adapter for general utilities
└── workflow_methods_adapter.py       # Adapter for workflow methods
```

To use the adapters in tests, import from the adapter modules instead of directly from the application:

```python
# Instead of: from ai_lab_repo import AgentLabRepository
from test_adapters.laboratory_adapter import AgentLabRepository

# Instead of: from utils.token_utils import count_tokens
from test_adapters.token_adapter import get_token_count
```

## Test Coverage
The project aims for at least 80% test coverage. Current coverage is tracked using pytest-cov and can be viewed by running:
```bash
python -m pytest --cov=./ --cov-report=html tests/
```

This will generate an HTML coverage report in the `htmlcov/` directory.

## Adding New Tests
When adding new functionality to the project, please follow these guidelines:
1. Create unit tests for all new components
2. Ensure tests are isolated and don't rely on external services
3. Use mocks for external dependencies
4. Keep tests fast and deterministic
5. Follow the naming conventions established in the project
6. Use test adapters instead of modifying the original code

### Creating a New Adapter

1. Create a new adapter file in the `test_adapters/` directory:

```python
"""
Component adapter for tests.

This module provides adapter functions that expose the component functionality
that tests expect, without modifying the original code.
"""

import sys
import os

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the original functionality
from original.module import function

# Create a test-friendly interface
def adapted_function(*args, **kwargs):
    # Modify behavior for testing or call the original
    return function(*args, **kwargs)

# Export the functions and classes
__all__ = ['adapted_function']
```

2. Create adapter versions of test files with `.adapter` suffix:

```python
# Import from the adapter instead of the original module
from test_adapters.component_adapter import adapted_function

def test_component_functionality():
    # Test using the adapter
    result = adapted_function(...)
    assert result == expected_value
```

3. Create a test runner in `tests/test_run_adapters/`:

```python
#!/usr/bin/env python3
"""
Adapter script to run component tests.

This script runs the component tests using the component adapter.
"""

import os
import sys
import shutil
import subprocess

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def main():
    """Main function to run component tests."""
    # Get the file paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    original_file = os.path.join(project_root, "tests/path/to/test_file.py")
    adapter_file = os.path.join(project_root, "tests/path/to/test_file.py.adapter")
    backup_file = os.path.join(project_root, "tests/path/to/test_file.py.original")
    
    # Check if adapter file exists
    if not os.path.exists(adapter_file):
        print(f"Error: Adapter file not found: {adapter_file}")
        return 1
    
    # Backup the original file if it exists
    if os.path.exists(original_file):
        shutil.copy2(original_file, backup_file)
        print(f"Original file backed up to: {backup_file}")
    
    try:
        # Copy the adapter file to the test location
        shutil.copy2(adapter_file, original_file)
        print(f"Adapter file copied to: {original_file}")
        
        # Run the tests
        print("\n* Running component tests *\n")
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/path/to/test_file.py", "-v"], 
            cwd=project_root
        )
        
        # Check the result
        if result.returncode == 0:
            print("\n✅ Component tests passed successfully!\n")
        else:
            print("\n❌ Component tests failed.\n")
            
        return result.returncode
    
    finally:
        # Restore the original file
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, original_file)
            os.remove(backup_file)
            print(f"Original file restored.")

if __name__ == "__main__":
    sys.exit(main())
```

4. Update `run_all_adapter_tests.py` to include your new test:

```python
# Add your new test to the list of test scripts
test_scripts = [
    # ... existing tests ...
    os.path.join(test_dir, "run_component_test.py"),
]
```

## CI/CD Integration
Tests are automatically run on GitHub Actions for all pull requests and pushes to the main branch. The configuration can be found in `.github/workflows/tests.yml`.

## Test Fixtures
Common test fixtures are defined in `conftest.py` and include:
- Agent instances for different roles (professor, phd_student, etc.)
- Sample research plans and literature reviews
- Experiment results for testing interpretation
- Temporary research directories

These fixtures can be used across all tests to maintain consistency and reduce code duplication.