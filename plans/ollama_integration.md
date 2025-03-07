# Ollama Integration Plan for AgentLaboratory

## Overview

This document outlines the comprehensive plan for integrating Ollama into the AgentLaboratory codebase. Ollama is an open-source framework for running large language models (LLMs) locally, which will enable significant improvements to the AgentLaboratory system:

1. **Local Model Access**: Run models locally without API costs or internet dependency
2. **Custom Model Support**: Use specialized models not available through commercial APIs
3. **Reduced Operating Costs**: Eliminate token-based costs associated with commercial API providers
4. **Enhanced Privacy**: Keep all research data and queries local to maintain privacy
5. **DeepSeek Integration**: Leverage existing DeepSeek model running on Ollama

## Current Architecture

The current AgentLaboratory architecture relies on API-based LLM interaction:

- `inference.py` handles all model interactions through providers like OpenAI and Anthropic
- `query_model()` function serves as the unified interface for all LLM queries
- Token tracking and cost estimation are built around API-based models
- Command line arguments allow specifying model selection and API keys

## Ollama Integration Architecture

The proposed integration will:

1. Add an Ollama-specific client layer that handles HTTP requests to the local Ollama server
2. Extend the model selection mechanism to include Ollama models
3. Maintain compatibility with existing API-based models
4. Add token counting estimation for local models
5. Update cost tracking to reflect free usage of local models

## Implementation Plan

### Phase 1: Ollama Client Implementation

#### 1.1 Create `ollama_client.py`

```python
import requests
import json
import tiktoken
import time
from typing import List, Dict, Any, Optional, Union

class OllamaClient:
    """Client for interacting with Ollama API for local LLM inference."""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        """Initialize the Ollama client.
        
        Args:
            base_url: Base URL for the Ollama API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.api_url = f"{base_url}/api"
        
    def list_models(self) -> List[str]:
        """Get a list of available models from the Ollama server."""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=self.timeout)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [model["name"] for model in models]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama server: {e}")
            
    def generate(self, 
                 model: str, 
                 prompt: str, 
                 system: Optional[str] = None,
                 temperature: Optional[float] = None,
                 stream: bool = False) -> str:
        """Generate text using the specified model."""
        url = f"{self.api_url}/generate"
        
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        if system:
            payload["system"] = system
            
        if temperature is not None:
            payload["options"] = {"temperature": temperature}
            
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to generate text with Ollama: {e}")
            
    def chat(self, 
             model: str, 
             messages: List[Dict[str, str]],
             temperature: Optional[float] = None) -> str:
        """Chat completion with the specified model."""
        url = f"{self.api_url}/chat"
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if temperature is not None:
            payload["options"] = {"temperature": temperature}
            
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to chat with Ollama: {e}")
            
    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in the given text.
        
        This is an approximation as Ollama models may use different tokenizers.
        """
        try:
            # Use cl100k_base as a reasonable proxy for most LLMs
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            # Fallback to character-based estimation (rough approximation)
            return len(text) // 4
```

#### 1.2 Create `ollama_config.py`

```python
from typing import Dict, Any, List, Optional

# Default Ollama server configuration
DEFAULT_OLLAMA_URL = "http://localhost:11434"

# Mapping of friendly model names to Ollama model names
MODEL_MAPPING = {
    "llama2": "llama2",
    "llama3": "llama3",
    "mistral": "mistral",
    "mixtral": "mixtral",
    "vicuna": "vicuna",
    "deepseek": "deepseek:latest",
    "deepseek-coder": "deepseek-coder:latest"
}

# Model context window sizes (aproximate)
MODEL_CONTEXT_SIZES = {
    "llama2": 4096,
    "llama3": 8192,
    "mistral": 8192,
    "mixtral": 32768,
    "vicuna": 4096,
    "deepseek": 8192,
    "deepseek-coder": 16384
}

# Default parameters for Ollama models
DEFAULT_PARAMETERS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1
}

def get_ollama_model_name(model_str: str) -> str:
    """Get the Ollama model name from the given model string."""
    return MODEL_MAPPING.get(model_str, model_str)

def get_context_size(model_str: str) -> int:
    """Get the approximate context size for the given model."""
    return MODEL_CONTEXT_SIZES.get(model_str, 4096)
```

### Phase 2: Inference Module Integration

#### 2.1 Update `inference.py`

```python
# Add imports at the top
from ollama_client import OllamaClient
from ollama_config import get_ollama_model_name, DEFAULT_OLLAMA_URL
import os

# Create global Ollama client
ollama_client = None

# Update query_model function to handle Ollama models
def query_model(model_str, prompt, system_prompt, openai_api_key=None, anthropic_api_key=None, 
                ollama_url=None, tries=5, timeout=5.0, temp=None, print_cost=True, version="1.5"):
    global ollama_client
    
    # Initialize Ollama client if needed
    if model_str.startswith("ollama:") and ollama_client is None:
        ollama_base_url = ollama_url or os.getenv("OLLAMA_API_URL", DEFAULT_OLLAMA_URL)
        ollama_client = OllamaClient(base_url=ollama_base_url)
    
    # Extract actual model name for Ollama models (format: "ollama:modelname")
    if model_str.startswith("ollama:"):
        ollama_model_name = model_str[7:]  # Remove "ollama:" prefix
        ollama_model_name = get_ollama_model_name(ollama_model_name)
        
        for _ in range(tries):
            try:
                # Prepare messages for chat completion
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                
                # Call Ollama API
                answer = ollama_client.chat(
                    model=ollama_model_name,
                    messages=messages,
                    temperature=temp
                )
                
                # Update token tracking
                try:
                    if model_str not in TOKENS_IN:
                        TOKENS_IN[model_str] = 0
                        TOKENS_OUT[model_str] = 0
                    
                    # Estimate tokens for tracking purposes
                    TOKENS_IN[model_str] += ollama_client.estimate_tokens(system_prompt + prompt)
                    TOKENS_OUT[model_str] += ollama_client.estimate_tokens(answer)
                    
                    if print_cost:
                        print(f"Current experiment cost = ${curr_cost_est()}, ** Approximate values, may not reflect true cost")
                except Exception as e:
                    if print_cost:
                        print(f"Cost approximation has an error? {e}")
                
                return answer
            except Exception as e:
                print(f"Ollama Inference Exception: {e}")
                time.sleep(timeout)
                continue
                
        raise Exception("Max retries: timeout")
        
    # Continue with existing model handling for non-Ollama models
    # ... [existing code]
```

#### 2.2 Update `curr_cost_est()` in `inference.py`

```python
def curr_cost_est():
    costmap_in = {
        "gpt-4o": 2.50 / 1000000,
        "gpt-4o-mini": 0.150 / 1000000,
        "o1-preview": 15.00 / 1000000,
        "o1-mini": 3.00 / 1000000,
        "claude-3-5-sonnet": 3.00 / 1000000,
        "deepseek-chat": 1.00 / 1000000,
        "o1": 15.00 / 1000000,
        # Ollama models cost $0
    }
    costmap_out = {
        "gpt-4o": 10.00 / 1000000,
        "gpt-4o-mini": 0.6 / 1000000,
        "o1-preview": 60.00 / 1000000,
        "o1-mini": 12.00 / 1000000,
        "claude-3-5-sonnet": 12.00 / 1000000,
        "deepseek-chat": 5.00 / 1000000,
        "o1": 60.00 / 1000000,
        # Ollama models cost $0
    }
    
    total_cost = 0
    
    for model in TOKENS_IN:
        # For Ollama models, cost is $0
        if model.startswith("ollama:"):
            continue
            
        # Calculate cost for API models
        if model in costmap_in:
            total_cost += costmap_in[model] * TOKENS_IN[model]
        if model in costmap_out:
            total_cost += costmap_out[model] * TOKENS_OUT[model]
            
    return total_cost
```

### Phase 3: CLI and Configuration Updates

#### 3.1 Update `ai_lab_repo.py` (Command Line Arguments)

```python
def parse_arguments():
    parser = argparse.ArgumentParser(description="AgentLaboratory Research Workflow")
    
    # Add existing arguments
    # ...
    
    # Add Ollama-specific arguments
    parser.add_argument(
        '--ollama-url',
        type=str,
        default="http://localhost:11434",
        help='URL for the Ollama API server (default: http://localhost:11434)'
    )
    
    parser.add_argument(
        '--ollama-model',
        type=str,
        help='Ollama model to use (e.g., llama3, mistral, deepseek)'
    )
    
    return parser.parse_args()
```

#### 3.2 Update `ai_lab_repo.py` (Main)

```python
if __name__ == "__main__":
    args = parse_arguments()
    
    llm_backend = args.llm_backend
    
    # Handle Ollama model selection
    if args.ollama_model:
        llm_backend = f"ollama:{args.ollama_model}"
    
    # Configure Ollama URL
    if args.ollama_url:
        os.environ["OLLAMA_API_URL"] = args.ollama_url
    
    # Continue with existing code
    # ...
```

### Phase 4: Testing and Validation

#### 4.1 Create Test Script (`test_ollama_integration.py`)

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ollama_client import OllamaClient
from inference import query_model

def test_ollama_client():
    """Test basic Ollama client functionality."""
    client = OllamaClient()
    
    print("Testing Ollama client...")
    try:
        models = client.list_models()
        print(f"Available models: {models}")
        
        if not models:
            print("No models found. Please make sure Ollama is running and has models loaded.")
            return False
            
        print("Ollama client test successful!")
        return True
    except Exception as e:
        print(f"Ollama client test failed: {e}")
        return False

def test_inference():
    """Test inference with Ollama through the query_model function."""
    print("Testing inference with Ollama...")
    
    try:
        # Simple test prompt
        test_prompt = "Explain what Ollama is in one sentence."
        system_prompt = "You are a helpful assistant."
        
        # Test with a model we know exists
        client = OllamaClient()
        models = client.list_models()
        
        if not models:
            print("No models found. Please make sure Ollama is running and has models loaded.")
            return False
            
        test_model = f"ollama:{models[0]}"
        print(f"Testing with model: {test_model}")
        
        response = query_model(
            model_str=test_model,
            prompt=test_prompt,
            system_prompt=system_prompt
        )
        
        print(f"Response: {response}")
        print("Inference test successful!")
        return True
    except Exception as e:
        print(f"Inference test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running Ollama integration tests...")
    
    client_test = test_ollama_client()
    if client_test:
        inference_test = test_inference()
    else:
        inference_test = False
        
    if client_test and inference_test:
        print("All tests passed!")
        sys.exit(0)
    else:
        print("Tests failed!")
        sys.exit(1)
```

### Phase 5: Documentation Updates

#### 5.1 Update `requirements.txt`

```
# Add to requirements.txt
requests>=2.28.0
```

#### 5.2 Update `CLAUDE.md` (Project Documentation)

```markdown
# Ollama Integration

## Running with Local Models

AgentLaboratory now supports running with local models via Ollama. This enables:
- Free inference with locally hosted models
- Higher privacy by keeping all data local
- Support for custom models not available via APIs

## Setup Instructions

1. Install Ollama: https://ollama.com/download
2. Pull your desired model (e.g., `ollama pull deepseek` or `ollama pull llama3`)
3. Run Ollama server (default runs on http://localhost:11434)
4. Run AgentLaboratory with Ollama model:

```bash
python ai_lab_repo.py --ollama-model deepseek --research-topic "Your research topic"
```

## Supported Models

Any model that can be run with Ollama is supported, including:
- deepseek
- llama3
- mistral
- mixtral
- vicuna
- and many more

Check available models on your local Ollama server with: `ollama list`

## Advanced Configuration

To connect to a remote Ollama server:
```bash
python ai_lab_repo.py --ollama-url "http://remote-server:11434" --ollama-model deepseek
```
```

## Implementation Schedule

### Week 1: Core Infrastructure
- Create `ollama_client.py` - Estimated: 3 hours
- Create `ollama_config.py` - Estimated: 2 hours
- Basic testing with local Ollama server - Estimated: 2 hours

### Week 2: Integration with Inference Module
- Update `inference.py` to support Ollama models - Estimated: 4 hours
- Add token counting and cost estimation for Ollama models - Estimated: 2 hours
- Integration testing - Estimated: 3 hours

### Week 3: Command Line Integration and Testing
- Update `ai_lab_repo.py` to support Ollama parameters - Estimated: 2 hours
- Create test suite for Ollama integration - Estimated: 4 hours
- Final integration testing - Estimated: 3 hours

### Week 4: Documentation and Release
- Update documentation in `CLAUDE.md` - Estimated: 1 hour
- Update `requirements.txt` - Estimated: 0.5 hours
- Final testing with multiple Ollama models - Estimated: 3 hours
- Create example scripts and workflows - Estimated: 2 hours

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Ollama API changes | High | Low | Design client with version detection and fallback mechanisms |
| Performance issues with large models | Medium | Medium | Implement timeouts and provide memory requirement guidance |
| Token counting inaccuracies | Low | High | Develop better token estimation for different model families |
| Compatibility with all phases | Medium | Medium | Extensive testing across all research phases |
| Different model capabilities | Medium | High | Document model-specific limitations and provide guidance |

## File Changes Summary

### Files to Modify:
1. `inference.py` - ~70 lines modified
2. `ai_lab_repo.py` - ~20 lines modified
3. `requirements.txt` - ~2 lines added
4. `CLAUDE.md` - ~40 lines added

### Files to Create:
1. `ollama_client.py` - ~120 lines
2. `ollama_config.py` - ~40 lines
3. `test_ollama_integration.py` - ~80 lines

**Total estimated lines of code: ~372 lines**

## Conclusion

Integrating Ollama into AgentLaboratory will provide significant benefits in terms of cost savings, privacy, and model flexibility. The proposed changes are relatively isolated to the model interface layer, which minimizes the risk to the rest of the codebase. The implementation is designed to maintain compatibility with existing cloud-based models while enabling seamless use of local models via Ollama.