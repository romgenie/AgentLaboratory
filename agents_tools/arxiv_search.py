def search_arxiv(query, max_results=5):
    """
    Search for papers on arXiv.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results
        
    Returns:
        list: List of paper data
    """
    # This would use the arXiv API in a real implementation
    # For testing, we'll return mock results
    return [
        {
            'id': '2201.12345',
            'title': 'Advanced Methods in Machine Learning',
            'authors': ['John Smith', 'Jane Doe'],
            'summary': 'This paper presents advanced methods in machine learning.',
            'published': '2022-01-15'
        },
        {
            'id': '2202.54321',
            'title': 'Neural Networks for Time Series Analysis',
            'authors': ['Alice Johnson', 'Bob Williams'],
            'summary': 'This paper explores neural network approaches for time series analysis.',
            'published': '2022-02-20'
        }
    ][:max_results]
