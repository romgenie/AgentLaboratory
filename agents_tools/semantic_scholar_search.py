def search_semantic_scholar(query, max_results=5):
    """
    Search for papers on Semantic Scholar.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        
    Returns:
        list: List of paper data
    """
    # This would use the Semantic Scholar API in a real implementation
    # For testing, we'll return mock results
    return [
        {
            'paperId': 'abc123',
            'title': 'Deep Learning in Natural Language Processing',
            'authors': [{'name': 'John Smith'}, {'name': 'Jane Doe'}],
            'abstract': 'This paper explores deep learning approaches in NLP.',
            'year': 2021,
            'citationCount': 150
        },
        {
            'paperId': 'def456',
            'title': 'Transformers for Computer Vision',
            'authors': [{'name': 'Alice Johnson'}, {'name': 'Bob Williams'}],
            'abstract': 'This paper applies transformer architectures to computer vision tasks.',
            'year': 2022,
            'citationCount': 75
        }
    ][:max_results]
