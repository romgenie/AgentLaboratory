# LLM Inference Optimization

## Overview
The current inference.py implementation makes individual API calls to LLM providers without optimization for batching, caching, or parallel processing. This plan outlines improvements to make LLM API usage more efficient and cost-effective.

## Problem
- Individual API calls have high latency overhead
- No caching of similar or repeated prompts
- Fixed retry mechanism without intelligent backoff
- No batching of similar requests
- Redundant token calculations
- Inefficient error handling

## Solution
Implement a more sophisticated inference system:
1. Add request batching where API supports it
2. Implement semantic caching for similar prompts
3. Add intelligent retry with exponential backoff
4. Optimize token counting
5. Parallelize independent requests

## Implementation Steps

### 1. Create Semantic Caching for Similar Prompts
```python
import numpy as np
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import threading

class SemanticCache:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", similarity_threshold=0.95, max_size=100):
        """Initialize semantic cache with embedding model"""
        self.embedding_model = SentenceTransformer(embedding_model)
        self.similarity_threshold = similarity_threshold
        self.cache = {}  # format: {model: {hash: {'prompt_emb': emb, 'result': result}}}
        self.max_size = max_size
        self.lock = threading.Lock()
        
    def _compute_embedding(self, text):
        """Compute embedding for a text"""
        return self.embedding_model.encode(text)
        
    def _find_similar(self, model, prompt_emb):
        """Find similar prompts in cache based on embedding similarity"""
        if model not in self.cache or not self.cache[model]:
            return None
            
        # Calculate similarities with all cached prompts for this model
        similarities = {}
        for key, item in self.cache[model].items():
            similarity = cosine_similarity([prompt_emb], [item['prompt_emb']])[0][0]
            if similarity >= self.similarity_threshold:
                similarities[key] = similarity
                
        # Return the most similar if any
        if similarities:
            best_match = max(similarities, key=similarities.get)
            return self.cache[model][best_match]['result']
        return None
        
    def get(self, model, prompt, system_prompt=""):
        """Try to retrieve from cache based on semantic similarity"""
        with self.lock:
            # Combine prompts for embedding calculation
            combined = system_prompt + " " + prompt
            prompt_emb = self._compute_embedding(combined)
            
            # Check for similar prompts
            return self._find_similar(model, prompt_emb)
        
    def add(self, model, prompt, system_prompt, result):
        """Add a result to the cache"""
        with self.lock:
            # Initialize model dict if needed
            if model not in self.cache:
                self.cache[model] = {}
                
            # Combine prompts for embedding
            combined = system_prompt + " " + prompt
            prompt_emb = self._compute_embedding(combined)
            
            # Create a unique key
            key = hash(str(prompt_emb.tobytes()))
            
            # Add to cache
            self.cache[model][key] = {
                'prompt_emb': prompt_emb,
                'result': result
            }
            
            # Manage cache size
            if len(self.cache[model]) > self.max_size:
                # Remove oldest entry
                oldest = next(iter(self.cache[model]))
                del self.cache[model][oldest]
```

### 2. Improve Token Counting with Batching
```python
class TokenCounter:
    def __init__(self):
        """Initialize token counter with models"""
        self.encodings = {}
        self.default_encoding = tiktoken.get_encoding("cl100k_base")
        
    def _get_encoding(self, model):
        """Get or create encoding for a model"""
        if model not in self.encodings:
            try:
                if model in ["o1-preview", "o1-mini", "claude-3.5-sonnet", "o1"]:
                    self.encodings[model] = tiktoken.encoding_for_model("gpt-4o")
                elif model in ["deepseek-chat"]:
                    self.encodings[model] = tiktoken.encoding_for_model("cl100k_base")
                else:
                    self.encodings[model] = tiktoken.encoding_for_model(model)
            except:
                # Fallback to default for unknown models
                self.encodings[model] = self.default_encoding
        return self.encodings[model]
        
    def count_tokens(self, model, texts):
        """Count tokens for a batch of texts"""
        encoding = self._get_encoding(model)
        if isinstance(texts, str):
            return len(encoding.encode(texts))
        else:
            return [len(encoding.encode(text)) for text in texts]
```

### 3. Implement Batched Inference
```python
import concurrent.futures
import backoff
import time
import os
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

class BatchedInference:
    def __init__(self, max_workers=5, semantic_cache=None):
        """Initialize the inference system"""
        self.token_counter = TokenCounter()
        self.semantic_cache = semantic_cache or SemanticCache()
        self.max_workers = max_workers
        self.tokens_in = {}
        self.tokens_out = {}
        
    def _get_client(self, model, api_key=None):
        """Get the appropriate client for a model"""
        if model.startswith("gpt-") or model.startswith("o1"):
            return OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        elif model == "deepseek-chat":
            return OpenAI(
                api_key=api_key or os.getenv('DEEPSEEK_API_KEY'),
                base_url="https://api.deepseek.com/v1"
            )
        elif model.startswith("claude"):
            import anthropic
            return anthropic.Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    @backoff.on_exception(
        backoff.expo,
        (RateLimitError, APIConnectionError),
        max_tries=5,
        max_time=60
    )
    def _execute_request(self, client, model, messages, temperature=None):
        """Execute a single request with backoff retry"""
        try:
            if model.startswith("claude"):
                # Handle Anthropic models
                system = next((m["content"] for m in messages if m["role"] == "system"), "")
                user_messages = [m for m in messages if m["role"] != "system"]
                response = client.messages.create(
                    model="claude-3-5-sonnet-latest" if model == "claude-3.5-sonnet" else model,
                    system=system,
                    messages=user_messages,
                    temperature=temperature
                )
                return response.content[0].text
            else:
                # Handle OpenAI-like APIs
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature
                )
                return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in _execute_request: {e}")
            raise
    
    def query_model(self, model, prompt, system_prompt, api_key=None, temperature=None, print_cost=True):
        """Single model query with caching"""
        # Check cache first
        cached_result = self.semantic_cache.get(model, prompt, system_prompt)
        if cached_result:
            return cached_result
            
        # Prepare messages
        if model in ["o1", "o1-mini", "o1-preview"]:
            messages = [{"role": "user", "content": system_prompt + prompt}]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
        # Get client
        client = self._get_client(model, api_key)
        
        # Execute request
        result = self._execute_request(client, model, messages, temperature)
        
        # Update token counts
        self._update_token_counts(model, system_prompt, prompt, result, print_cost)
        
        # Add to cache
        self.semantic_cache.add(model, prompt, system_prompt, result)
        
        return result
    
    def batch_query(self, model, prompts, system_prompts, api_key=None, temperature=None, print_cost=True):
        """Process multiple queries in parallel"""
        # Ensure inputs are lists
        if isinstance(prompts, str):
            prompts = [prompts]
        if isinstance(system_prompts, str):
            system_prompts = [system_prompts] * len(prompts)
            
        results = []
        
        # Use ThreadPoolExecutor for parallel requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            # Submit all tasks
            for prompt, system_prompt in zip(prompts, system_prompts):
                futures.append(
                    executor.submit(
                        self.query_model,
                        model,
                        prompt,
                        system_prompt,
                        api_key,
                        temperature,
                        False  # Don't print cost per request
                    )
                )
                
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(f"ERROR: {str(e)}")
                    
        # Print combined cost once at the end
        if print_cost:
            self._print_cost()
                    
        return results if len(results) > 1 else results[0]
        
    def _update_token_counts(self, model, system_prompt, prompt, result, print_cost):
        """Update token counts and optionally print cost"""
        if model not in self.tokens_in:
            self.tokens_in[model] = 0
            self.tokens_out[model] = 0
            
        # Count tokens
        self.tokens_in[model] += self.token_counter.count_tokens(
            model, system_prompt + prompt
        )
        self.tokens_out[model] += self.token_counter.count_tokens(
            model, result
        )
        
        if print_cost:
            self._print_cost()
            
    def _print_cost(self):
        """Print current cost estimate"""
        costmap_in = {
            "gpt-4o": 2.50 / 1000000,
            "gpt-4o-mini": 0.150 / 1000000,
            "o1-preview": 15.00 / 1000000,
            "o1-mini": 3.00 / 1000000,
            "claude-3-5-sonnet": 3.00 / 1000000,
            "deepseek-chat": 1.00 / 1000000,
            "o1": 15.00 / 1000000,
        }
        costmap_out = {
            "gpt-4o": 10.00/ 1000000,
            "gpt-4o-mini": 0.6 / 1000000,
            "o1-preview": 60.00 / 1000000,
            "o1-mini": 12.00 / 1000000,
            "claude-3-5-sonnet": 12.00 / 1000000,
            "deepseek-chat": 5.00 / 1000000,
            "o1": 60.00 / 1000000,
        }
        
        total_cost = sum([costmap_in[m] * self.tokens_in[m] for m in self.tokens_in]) + \
                    sum([costmap_out[m] * self.tokens_out[m] for m in self.tokens_out])
                    
        print(f"Current experiment cost = ${total_cost:.6f}, ** Approximate values, may not reflect true cost")
```

### 4. Update Inference Interface
```python
# New simplified interface in inference.py
from .batched_inference import BatchedInference

# Create a singleton instance
_inference = BatchedInference()

def query_model(model_str, prompt, system_prompt, openai_api_key=None, anthropic_api_key=None, temp=None, print_cost=True):
    """Backwards-compatible interface"""
    api_key = openai_api_key
    if model_str.startswith("claude") and anthropic_api_key:
        api_key = anthropic_api_key
        
    return _inference.query_model(
        model=model_str,
        prompt=prompt,
        system_prompt=system_prompt,
        api_key=api_key,
        temperature=temp,
        print_cost=print_cost
    )
    
def batch_query_model(model_str, prompts, system_prompts, openai_api_key=None, anthropic_api_key=None, temp=None, print_cost=True):
    """New interface for batch processing"""
    api_key = openai_api_key
    if model_str.startswith("claude") and anthropic_api_key:
        api_key = anthropic_api_key
        
    return _inference.batch_query(
        model=model_str,
        prompts=prompts,
        system_prompts=system_prompts,
        api_key=api_key,
        temperature=temp,
        print_cost=print_cost
    )
```

## Benefits
- Reduced latency through batched processing
- Lower costs by caching similar prompts
- More efficient error handling with exponential backoff
- Simplified token counting with reused encodings
- Better parallelization of independent queries

## Metrics for Success
- 30%+ reduction in total API calls through semantic caching
- 2-3x faster processing for batched similar requests
- Improved resilience to API rate limits and transient errors
- More accurate and efficient token counting
- Reduced overall latency for research workflows