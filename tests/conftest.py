import pytest
import os
import sys

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import common modules needed for testing
from agents.base_agent import BaseAgent
from agents.professor_agent import ProfessorAgent
from agents.phd_student_agent import PhDStudentAgent
# PostdocAgent import removed due to class not being available
# from agents.postdoc_agent import PostdocAgent
from agents.reviewers_agent import ReviewersAgent
from agents.ml_engineer_agent import MLEngineerAgent
from agents.sw_engineer_agent import SWEngineerAgent

# Define fixtures that can be used across all test files

@pytest.fixture
def research_dir(tmpdir):
    """Create a temporary research directory for testing."""
    return str(tmpdir)

@pytest.fixture
def base_agent():
    """Create a standard BaseAgent for testing."""
    return BaseAgent(
        name="Test Agent",
        expertise=["Machine Learning", "Deep Learning"],
        personality_traits=["analytical", "curious"],
        model="gpt-4o"
    )

@pytest.fixture
def professor_agent():
    """Create a standard ProfessorAgent for testing."""
    return ProfessorAgent(
        name="Dr. Smith",
        expertise=["Machine Learning", "NLP"],
        personality_traits=["meticulous", "analytical"],
        model="gpt-4o"
    )

@pytest.fixture
def phd_student_agent():
    """Create a standard PhDStudentAgent for testing."""
    return PhDStudentAgent(
        name="Jane Doe",
        expertise=["Deep Learning", "Computer Vision"],
        personality_traits=["creative", "curious"],
        model="gpt-4o"
    )

# Postdoc agent fixture removed due to missing class
# @pytest.fixture
# def postdoc_agent():
#     """Create a standard PostdocAgent for testing."""
#     return PostdocAgent(
#         name="John Smith",
#         expertise=["Data Science", "Statistical Analysis"],
#         personality_traits=["methodical", "thorough"],
#         model="gpt-4o"
#     )

@pytest.fixture
def reviewers_agent():
    """Create a standard ReviewersAgent for testing."""
    return ReviewersAgent(
        name="Review Committee",
        expertise=["Research Methods", "Statistics", "Machine Learning"],
        personality_traits=["critical", "detail-oriented"],
        model="gpt-4o"
    )

@pytest.fixture
def ml_engineer_agent():
    """Create a standard MLEngineerAgent for testing."""
    return MLEngineerAgent(
        name="Alex Lee",
        expertise=["TensorFlow", "PyTorch", "Model Optimization"],
        personality_traits=["practical", "detail-oriented"],
        model="gpt-4o"
    )

@pytest.fixture
def sw_engineer_agent():
    """Create a standard SWEngineerAgent for testing."""
    return SWEngineerAgent(
        name="Sam Chen",
        expertise=["Python", "Software Architecture", "Testing"],
        personality_traits=["methodical", "efficient"],
        model="gpt-4o"
    )

@pytest.fixture
def sample_research_plan():
    """Create a sample research plan for testing."""
    return {
        "research_questions": [
            "How can attention mechanisms improve transformer model performance?",
            "What are the computational trade-offs of different attention mechanisms?"
        ],
        "objectives": [
            "Evaluate different attention mechanisms on standard NLP tasks",
            "Measure computational efficiency of each mechanism",
            "Identify optimal configurations for different application scenarios"
        ],
        "methodology": [
            "Literature review of attention mechanisms",
            "Implementation of key attention variants",
            "Benchmarking on GLUE tasks",
            "Profiling of computational requirements"
        ],
        "experiments": [
            "Compare vanilla attention, sparse attention, and linear attention",
            "Measure accuracy vs. throughput trade-offs",
            "Test on varying sequence lengths"
        ],
        "evaluation_metrics": [
            "Accuracy",
            "F1 score",
            "Throughput (tokens/second)",
            "Memory usage"
        ]
    }

@pytest.fixture
def sample_literature_review():
    """Create a sample literature review for testing."""
    return {
        "papers": [
            {
                "title": "Attention Is All You Need",
                "authors": ["Vaswani et al."],
                "year": 2017,
                "summary": "Introduced the transformer architecture with self-attention mechanism."
            },
            {
                "title": "Efficient Transformers: A Survey",
                "authors": ["Tay et al."],
                "year": 2020,
                "summary": "Comprehensive survey of efficient transformer variants."
            }
        ],
        "key_insights": [
            "Self-attention enables parallel processing of sequences",
            "Attention mechanisms have quadratic complexity with sequence length",
            "Various sparse and linear attention variants have been proposed to improve efficiency"
        ],
        "methodologies": [
            "Benchmark comparisons",
            "Theoretical complexity analysis",
            "Ablation studies"
        ],
        "research_gaps": [
            "Limited understanding of attention behavior on very long sequences",
            "Trade-offs between different efficient attention mechanisms not fully explored",
            "Domain-specific optimizations still an open area"
        ],
        "synthesis": "While transformers with attention mechanisms have revolutionized NLP, efficiency remains a challenge for long sequences. Various approaches to efficient attention show promise but require systematic evaluation."
    }

@pytest.fixture
def sample_experiment_results():
    """Create sample experiment results for testing."""
    return {
        "models": {
            "vanilla_transformer": {
                "accuracy": 0.92,
                "f1_score": 0.91,
                "throughput": 1000,
                "memory_usage": "5.2GB"
            },
            "sparse_transformer": {
                "accuracy": 0.90,
                "f1_score": 0.89,
                "throughput": 2500,
                "memory_usage": "3.1GB"
            },
            "linear_transformer": {
                "accuracy": 0.88,
                "f1_score": 0.87,
                "throughput": 4000,
                "memory_usage": "2.8GB"
            }
        },
        "sequence_length_impact": {
            "vanilla": [
                {"length": 512, "throughput": 2000},
                {"length": 1024, "throughput": 1000},
                {"length": 2048, "throughput": 500}
            ],
            "sparse": [
                {"length": 512, "throughput": 3500},
                {"length": 1024, "throughput": 2500},
                {"length": 2048, "throughput": 1800}
            ],
            "linear": [
                {"length": 512, "throughput": 4500},
                {"length": 1024, "throughput": 4000},
                {"length": 2048, "throughput": 3800}
            ]
        },
        "analysis": "Linear attention maintains consistent performance across sequence lengths, while vanilla attention degrades rapidly. Sparse attention offers a middle ground with better accuracy than linear approaches but still good efficiency."
    }