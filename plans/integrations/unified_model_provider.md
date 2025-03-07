# Unified Model Provider Interface

## Overview
- **Name**: Unified Model Provider Interface
- **Purpose**: Create a standardized interface for all LLM providers to ensure consistent access patterns and interoperability
- **Implementation Complexity**: High - Requires careful design to accommodate different provider capabilities while maintaining a unified interface
- **Timeline**: 4 weeks
- **Business Value**: High - Enables model provider flexibility, simplifies maintenance, and future-proofs the application

## Details
- **Estimated Lines of Code**: ~850 LOC
- **New Files to Create**:
  - `inference/providers/__init__.py`: Package initialization - ~20 LOC
  - `inference/providers/base.py`: Abstract base provider interface - ~150 LOC
  - `inference/providers/openai_provider.py`: OpenAI implementation - ~120 LOC
  - `inference/providers/anthropic_provider.py`: Anthropic implementation - ~120 LOC
  - `inference/providers/deepseek_provider.py`: DeepSeek implementation - ~100 LOC
  - `inference/providers/ollama_provider.py`: Ollama implementation - ~100 LOC
  - `inference/providers/factory.py`: Provider factory for dynamic instantiation - ~50 LOC
  - `inference/providers/config.py`: Provider configuration system - ~50 LOC
  - `inference/providers/model_specs.py`: Model specifications and capabilities - ~70 LOC
  - `inference/providers/token_counter.py`: Unified token counting - ~100 LOC
  - `inference/providers/exceptions.py`: Provider-specific exception handling - ~70 LOC

- **Files to Modify**:
  - `inference/query_model.py`: Update to use provider interface - ~50 LOC changes
  - `ai_lab_repo.py`: Update LLM initialization - ~20 LOC changes
  - `common_imports.py`: Add provider imports - ~10 LOC changes
  - `inference/cost_estimation.py`: Update to use provider interface - ~30 LOC changes

## Implementation Phases
### Phase 1: Core Interface Design (1 week)
- **Timeline**: Days 1-7
- **Tasks**:
  - Design abstract base provider interface
  - Define common methods and properties
  - Create capability detection system
  - Design factory pattern for provider instantiation
  - Implement configuration system
- **Code Examples**:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any
from enum import Enum, auto

class ModelCapability(Enum):
    """Capabilities that providers may support."""
    TOOL_CALLS = auto()
    FUNCTION_CALLING = auto()
    STREAMING = auto()
    JSON_MODE = auto()
    VISION = auto()

class ModelProvider(ABC):
    """Abstract base class for all model providers."""
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the name of this provider."""
        pass
        
    @property
    @abstractmethod
    def supported_models(self) -> List[str]:
        """Get list of supported models for this provider."""
        pass
        
    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, List[ModelCapability]]:
        """Get map of model names to their capabilities."""
        pass
    
    @abstractmethod
    def generate(self, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None) -> str:
        """Generate text from the model."""
        pass
        
    @abstractmethod
    def generate_with_tools(self,
                           prompt: str,
                           tools: List[Dict[str, Any]],
                           system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate text with tool-use capabilities."""
        pass
        
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        pass
        
    @abstractmethod
    def get_token_limit(self, model_name: str) -> int:
        """Get the token limit for the specified model."""
        pass
        
    @abstractmethod
    def supports_capability(self, model_name: str, capability: ModelCapability) -> bool:
        """Check if the specified model supports a capability."""
        pass
```

### Phase 2: Provider Implementations (2 weeks)
- **Timeline**: Days 8-21
- **Tasks**:
  - Create OpenAI provider implementation
  - Create Anthropic provider implementation
  - Create DeepSeek provider implementation
  - Create Ollama provider implementation
  - Implement token counting for each provider
  - Add proper error handling and retry mechanisms
  - Build model specification system
- **Code Examples**:
```python
class OpenAIProvider(ModelProvider):
    """OpenAI model provider implementation."""
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 default_model: str = "gpt-4o"):
        """Initialize the OpenAI provider."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.default_model = default_model
        self.client = OpenAI(api_key=self.api_key)
        self._init_model_specs()
        
    @property
    def provider_name(self) -> str:
        return "openai"
        
    @property
    def supported_models(self) -> List[str]:
        return list(self._model_specs.keys())
        
    @property
    def capabilities(self) -> Dict[str, List[ModelCapability]]:
        return {model: specs["capabilities"] 
                for model, specs in self._model_specs.items()}
        
    def _init_model_specs(self):
        """Initialize model specifications."""
        self._model_specs = {
            "gpt-4o": {
                "token_limit": 128000,
                "capabilities": [
                    ModelCapability.TOOL_CALLS,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING,
                    ModelCapability.JSON_MODE,
                    ModelCapability.VISION
                ]
            },
            "gpt-4o-mini": {
                "token_limit": 128000,
                "capabilities": [
                    ModelCapability.TOOL_CALLS,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING,
                    ModelCapability.JSON_MODE
                ]
            },
            # Additional models...
        }
    
    def generate(self, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None,
                 model: Optional[str] = None) -> str:
        """Generate text using OpenAI models."""
        model = model or self.default_model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise ProviderException(f"OpenAI generation failed: {str(e)}")
```

### Phase 3: Integration and Testing (1 week)
- **Timeline**: Days 22-28
- **Tasks**:
  - Update existing codebase to use new provider interface
  - Create compatibility layer for existing query_model.py
  - Write comprehensive tests for each provider
  - Implement model-specific configuration validation
  - Build provider fallback mechanism
  - Create documentation and usage examples

## Requirements
- **Dependencies**:
  - OpenAI SDK (v1.0+)
  - Anthropic SDK
  - DeepSeek SDK (if available)
  - Requests (for API calls)
  - tiktoken (for OpenAI token counting)
  - anthropic-tokenizer (for Anthropic token counting)
  - Pydantic (for configuration validation)
- **Prerequisites**:
  - None; this is a foundational integration that other integrations will build upon
- **Hardware Requirements**:
  - Standard development environment
  - CI/CD pipeline for testing

## Testing Strategy
- **Unit Tests**:
  - Test each provider implementation with mock responses
  - Verify token counting accuracy across providers
  - Test error handling and retries
  - Validate capability detection
- **Integration Tests**:
  - Test each provider with sandbox/test API keys
  - Verify proper interface implementation across providers
  - Test factory pattern and provider switching
  - Verify provider fallback mechanisms
- **Performance Metrics**:
  - Response time for each provider
  - Token counting accuracy
  - Memory usage per provider
  - Error recovery time
- **Success Criteria**:
  - All tests pass at 95%+ coverage
  - Token counting accuracy within 1% of provider-specific tokenizers
  - Seamless switching between providers
  - Proper handling of provider-specific capabilities

## Compatibility Considerations
- **Existing Codebase**: 
  - Maintains compatibility through updated query_model.py
  - Minimal changes to existing code
  - Uses factory pattern for seamless provider selection
  - Gradual migration path for existing code

- **Other Integrations**:
  - Foundational for DSPy, TextGrad, and all provider-specific integrations
  - Enables LLM inference optimization through standardized interface
  - Supports future model providers without architecture changes
  - Provides capability detection for feature-specific code paths

- **Potential Conflicts**:
  - Provider-specific features may not map cleanly to unified interface
  - Tool calling formats differ significantly between providers
  - Token counting algorithms vary between providers
  - Error handling and retry mechanisms are provider-specific
  - Model versioning differences between providers

- **Backward Compatibility**:
  - Legacy adapter for existing query_model.py users
  - Configuration-based defaults for seamless migration
  - Documentation for migration from direct API calls

## Minimal Implementation Option
A minimal version would focus on:
1. Basic abstract interface with core methods (generate, count_tokens)
2. Implementations for OpenAI and one other provider (Anthropic)
3. Simple token counting with provider libraries
4. Basic error handling
5. Direct instantiation without factory pattern
6. Limited capability detection

This would reduce implementation complexity to ~400 LOC while still providing the key unified interface benefit.

## Rollback Plan
1. Maintain the existing query_model.py implementation alongside new interface
2. Implement feature flags to control interface usage
3. Create monitoring for interface usage and errors
4. Document procedure for reverting to legacy implementation

## Documentation Updates
1. Update API documentation with new provider interface
2. Create migration guide for existing code
3. Provide examples for each provider implementation
4. Document capability detection and provider-specific features
5. Create troubleshooting guide for common issues