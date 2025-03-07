import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from agents_tools.semantic_scholar_search import search_semantic_scholar

class TestSemanticScholarSearch:
    """Test suite for Semantic Scholar search functionality."""
    
    def test_search_semantic_scholar_returns_list(self):
        """Test that search_semantic_scholar returns a list of results."""
        results = search_semantic_scholar("deep learning")
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_search_semantic_scholar_max_results(self):
        """Test that search_semantic_scholar respects max_results parameter."""
        max_results = 1
        results = search_semantic_scholar("transformers", max_results=max_results)
        assert len(results) <= max_results
    
    def test_search_semantic_scholar_result_structure(self):
        """Test that search_semantic_scholar results have the expected structure."""
        results = search_semantic_scholar("computer vision")
        
        for paper in results:
            assert isinstance(paper, dict)
            assert 'paperId' in paper
            assert 'title' in paper
            assert 'authors' in paper
            assert 'abstract' in paper
            assert 'year' in paper
            assert 'citationCount' in paper
            
            assert isinstance(paper['paperId'], str)
            assert isinstance(paper['title'], str)
            assert isinstance(paper['authors'], list)
            assert isinstance(paper['abstract'], str)
            assert isinstance(paper['year'], int)
            assert isinstance(paper['citationCount'], int)
            
            # Check author structure
            for author in paper['authors']:
                assert isinstance(author, dict)
                assert 'name' in author