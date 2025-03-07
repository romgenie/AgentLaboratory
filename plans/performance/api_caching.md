# API Call Caching Implementation

## Overview
Currently, API calls to external services (arXiv, Semantic Scholar) are made without any caching, resulting in duplicate calls that waste API rate limits, time, and potentially money. This plan outlines the implementation of a caching layer for these API calls.

## Problem
- ArxivSearch and SemanticScholarSearch make redundant API calls for the same queries
- Each API call has fixed sleep delays, slowing down the research process
- No persistence between program runs, wasting previous results

## Solution
Implement a multi-level caching system for API calls:
1. In-memory LRU cache for current session
2. Disk-based cache for persistence between runs

## Implementation Steps

### 1. Create a Generic API Cache Class
```python
from functools import lru_cache
import os
import json
import hashlib
import time

class APICache:
    def __init__(self, cache_dir="./cache", max_size=100, ttl=86400): # 24 hour TTL default
        self.cache_dir = cache_dir
        self.max_size = max_size
        self.ttl = ttl
        os.makedirs(cache_dir, exist_ok=True)
        
    def _get_cache_key(self, func_name, args, kwargs):
        # Create a deterministic cache key from function name and arguments
        args_str = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(f"{func_name}:{args_str}".encode()).hexdigest()
        
    def get(self, func_name, args, kwargs):
        key = self._get_cache_key(func_name, args, kwargs)
        
        # Check memory cache first (implemented with decorator)
        
        # Then check disk cache
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                # Check if cache is still valid
                if time.time() - cache_data['timestamp'] < self.ttl:
                    return cache_data['result']
        
        return None
        
    def set(self, func_name, args, kwargs, result):
        key = self._get_cache_key(func_name, args, kwargs)
        cache_data = {
            'timestamp': time.time(),
            'result': result
        }
        
        # Save to disk cache
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
```

### 2. Create Caching Decorator
```python
def api_cached(cache_instance):
    """Decorator to cache API call results both in memory and on disk"""
    def decorator(func):
        # Use functools LRU cache for in-memory caching
        @lru_cache(maxsize=cache_instance.max_size)
        def cached_func(*args, **kwargs):
            # Try to get from cache first
            cached_result = cache_instance.get(func.__name__, args, kwargs)
            if cached_result is not None:
                return cached_result
                
            # If not in cache, call the function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_instance.set(func.__name__, args, kwargs, result)
            return result
            
        return cached_func
    return decorator
```

### 3. Apply to Existing API Functions
```python
# Initialize cache
api_cache = APICache(cache_dir="./research_dir/api_cache")

# In ArxivSearch class
@api_cached(api_cache)
def find_papers_by_str(self, query, N=20):
    # Existing implementation
    
@api_cached(api_cache)
def retrieve_full_paper_text(self, query):
    # Existing implementation

# Same for SemanticScholarSearch methods
```

## Benefits
- Significantly reduces API calls for repeated queries
- Eliminates redundant paper downloads
- Speeds up research cycles by avoiding sleep times on cache hits
- Persists results between program runs
- Makes the system more resilient to API rate limiting and failures

## Metrics for Success
- 50%+ reduction in API calls for typical research workflows
- Elimination of redundant downloads for the same paper
- Improved response time for literature reviews on similar topics