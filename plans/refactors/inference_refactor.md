# Inference Module Refactoring Plan

## Overview
- **Name**: Unified Inference Framework
- **Target Component**: Inference Directory
- **Implementation Complexity**: High - Requires extensive rework of core model interaction components
- **Timeline**: 4 weeks
- **Business Value**: Very High - Enables model flexibility, improves performance, and reduces costs

## Details
- **Total Estimated LOC**: ~1,200 LOC
  - New code: ~900 LOC
  - Modified code: ~250 LOC
  - Removed code: ~50 LOC

- **New Files to Create**:
  - `inference/providers/__init__.py`: Provider package initialization - ~20 LOC
  - `inference/providers/base.py`: Abstract provider interface - ~150 LOC
  - `inference/providers/openai_provider.py`: OpenAI implementation - ~120 LOC
  - `inference/providers/anthropic_provider.py`: Anthropic implementation - ~120 LOC
  - `inference/providers/deepseek_provider.py`: DeepSeek implementation - ~100 LOC
  - `inference/providers/ollama_provider.py`: Ollama implementation - ~100 LOC
  - `inference/providers/factory.py`: Provider factory for dynamic instantiation - ~50 LOC
  - `inference/providers/exceptions.py`: Provider-specific exceptions - ~50 LOC
  - `inference/infrastructure/cache.py`: Caching infrastructure - ~100 LOC
  - `inference/infrastructure/batching.py`: Request batching system - ~80 LOC
  - `inference/infrastructure/retry.py`: Retry mechanisms - ~60 LOC
  - `inference/infrastructure/telemetry.py`: Performance monitoring - ~50 LOC

- **Files to Modify**:
  - `inference/query_model.py`: Update to use provider interface - ~100 LOC changes
  - `inference/cost_estimation.py`: Update for provider-specific cost models - ~100 LOC changes
  - `inference/__init__.py`: Update exports and convenience methods - ~50 LOC changes

- **Files to Remove/Deprecate**:
  - None (maintaining backward compatibility through adapters)

## Current Issues Addressed
1. **Limited Provider Support**: Currently only supports OpenAI and DeepSeek - adding abstraction for multiple providers
2. **Poor Error Handling**: Current error propagation is inconsistent - implementing standardized exceptions
3. **No Caching**: Redundant API calls waste tokens - adding multi-level caching
4. **Limited Concurrency**: Sequential processing slows performance - adding async capabilities
5. **Tight Coupling**: Direct provider dependencies make switching difficult - implementing provider abstraction
6. **Inconsistent Cost Tracking**: Tracking varies by provider - standardizing cost estimation

## Implementation Phases
### Phase 1: Provider Interface (Week 1)
- **Timeline**: 5 days
- **Tasks**:
  - Design abstract provider interface
  - Define capability detection system
  - Create standard request/response formats
  - Design exception hierarchy
  - Implement core interface and base classes
- **LOC Impact**: ~350 LOC
- **Code Examples**:
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
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
        
    @abstractmethod
    def generate(self, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None) -> str:
        """Generate text from the model."""
        pass
```

### Phase 2: Provider Implementations (Week 2)
- **Timeline**: 5 days
- **Tasks**:
  - Implement OpenAI provider
  - Implement Anthropic provider
  - Implement DeepSeek provider
  - Implement Ollama provider
  - Create provider factory system
  - Add token counting for all providers
- **LOC Impact**: ~500 LOC

### Phase 3: Infrastructure Layer (Week 3)
- **Timeline**: 5 days
- **Tasks**:
  - Implement caching system (memory and disk)
  - Create request batching for similar prompts
  - Build retry mechanism with exponential backoff
  - Develop telemetry for performance monitoring
  - Update cost estimation for all providers
- **LOC Impact**: ~350 LOC

### Phase 4: Integration and Migration (Week 4)
- **Timeline**: 5 days
- **Tasks**:
  - Update query_model.py with adapter pattern
  - Add backward compatibility layer
  - Create comprehensive tests for all providers
  - Add documentation and usage examples
  - Implement feature flags for gradual rollout
- **LOC Impact**: ~200 LOC

## Dependencies
- **Prerequisites**: 
  - Init Files Refactor (for proper imports)
- **Dependents**: 
  - MLSolver Refactor
  - Agents Directory Refactor
  - DSPy Integration
  - TextGrad Integration
- **Required By**: Week 7 of overall refactoring plan

## Testing Strategy
- **Unit Tests**: 
  - Test provider interfaces individually
  - Test caching and infrastructure components
  - Mock API responses for each provider
  - New tests needed: ~60 test cases
  - Tests to update: ~15 test cases
- **Integration Tests**: 
  - End-to-end tests with actual API calls (using small models)
  - Performance benchmarks for caching and batching
  - Error recovery scenarios
  - New tests needed: ~20 test cases
  - Tests to update: ~10 test cases
- **Expected Test Coverage**: 95%+ for inference framework

## Backward Compatibility
- **Breaking Changes**: 
  - New parameter format for advanced features
  - Provider-specific capabilities access
  - Different error handling patterns
- **Migration Path**: 
  - Legacy adapter in query_model.py maintains current signatures
  - Feature detection for provider capabilities
  - Gradual migration documentation
- **Deprecation Strategy**: 
  - Support current query_model.py interface for 6 months
  - Add deprecation warnings for direct provider access
  - Version-specific imports for transition period
- **Compatibility Layer**: 
  - Adapter pattern in query_model.py to translate between old and new interfaces
  - Provider-specific fallbacks for missing capabilities

## Risks and Mitigation
- **Risk 1**: API changes in provider SDKs - Create abstraction layers and adapter patterns
- **Risk 2**: Performance overhead from abstraction - Benchmark and optimize critical paths
- **Risk 3**: Backward compatibility issues - Comprehensive testing and adapter pattern
- **Risk 4**: Cost estimation accuracy - Provider-specific calibration and validation

## Minimal Implementation Option
If resources are constrained, focus on:
1. Create basic provider interface
2. Implement OpenAI and one other provider
3. Add simple in-memory caching
4. Update query_model.py with minimal changes
5. Skip advanced features like batching and telemetry

## Rollback Plan
1. Maintain old implementation of query_model.py
2. Create feature flag to control which implementation is used
3. Use environment variables to select implementation
4. Keep comprehensive test suite to validate behavior equivalence