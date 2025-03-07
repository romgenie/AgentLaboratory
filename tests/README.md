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
    ├── test_coverage_setup.py        # Tests for coverage setup
    └── test_mocking_strategy.py      # Tests for mocking strategy
```

## Running Tests

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

## CI/CD Integration
Tests are automatically run on GitHub Actions for all pull requests and pushes to the main branch. The configuration can be found in `.github/workflows/tests.yml`.

## Test Fixtures
Common test fixtures are defined in `conftest.py` and include:
- Agent instances for different roles (professor, phd_student, etc.)
- Sample research plans and literature reviews
- Experiment results for testing interpretation
- Temporary research directories

These fixtures can be used across all tests to maintain consistency and reduce code duplication.