import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from agents_tools.arxiv_search import search_arxiv

class TestArxivSearch:
    """Test suite for ArXiv search functionality."""
    
    def test_search_arxiv_returns_list(self):
        """Test that search_arxiv returns a list of results."""
        results = search_arxiv("machine learning")
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_search_arxiv_max_results(self):
        """Test that search_arxiv respects max_results parameter."""
        max_results = 1
        results = search_arxiv("neural networks", max_results=max_results)
        assert len(results) <= max_results
    
    def test_search_arxiv_result_structure(self):
        """Test that search_arxiv results have the expected structure."""
        results = search_arxiv("deep learning")
        
        for paper in results:
            assert isinstance(paper, dict)
            assert 'id' in paper
            assert 'title' in paper
            assert 'authors' in paper
            assert 'summary' in paper
            assert 'published' in paper
            
            assert isinstance(paper['id'], str)
            assert isinstance(paper['title'], str)
            assert isinstance(paper['authors'], list)
            assert isinstance(paper['summary'], str)
            assert isinstance(paper['published'], str)