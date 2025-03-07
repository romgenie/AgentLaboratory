# Inference System Refactoring Plan

## Overview
- **Name**: Inference Provider Abstraction
- **Target Component**: Model inference system (`inference/`)
- **Implementation Complexity**: Medium (downgraded from High) - Focused changes to provider handling
- **Timeline**: 2 weeks (reduced from 3 weeks)
- **Business Value**: High - Enables model flexibility and performance improvements

## Details
- **Total Estimated LOC**: ~250 LOC (reduced from 350)
  - New code: ~200 LOC (reduced from 280)
  - Modified code: ~50 LOC (reduced from 70)
  - Removed code: ~0 LOC (preserving backward compatibility)

- **New Files to Create**:
  - `inference/providers/base.py`: Minimal provider interface (~60 LOC)
  - `inference/providers/openai_provider.py`: OpenAI implementation (~60 LOC)
  - `inference/providers/anthropic_provider.py`: Anthropic implementation (~60 LOC)
  - `inference/providers/__init__.py`: Package initialization (~20 LOC)

- **Files to Modify**:
  - `inference/query_model.py`: Update to use provider interface (~30 LOC changes)
  - `inference/cost_estimation.py`: Update cost calculations (~20 LOC changes)

## Current Issues Addressed
1. Tight coupling to specific LLM providers
2. Difficulty adding new model providers
3. Inconsistent error handling across providers
4. Limited token counting accuracy for different providers

## Implementation Phases
### Phase 1: Provider Interface (3 days)
- **Tasks**:
  - Design minimal provider interface
  - Define core methods (generate, count_tokens)
  - Create simple error handling patterns
- **LOC Impact**: ~80 LOC (reduced from 140)
- **Code Example** (simplified):
```python
from abc import ABC, abstractmethod
from typing import Optional

class ModelProvider(ABC):
    """Minimal interface for model providers."""
    
    @abstractmethod
    def generate(self, 
                 prompt: str, 
                 system_prompt: Optional[str] = None,
                 temperature: float = 0.7,
                 max_tokens: Optional[int] = None) -> str:
        """Generate text from the model."""
        pass
        
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in the given text."""
        pass
```

### Phase 2: Implement Core Providers (1 week)
- **Tasks**:
  - Create OpenAI provider implementation
  - Create Anthropic provider implementation
  - Build basic token counting for each provider
  - Implement simple error handling
- **LOC Impact**: ~120 LOC (reduced from 140)

### Phase 3: Integrate with Existing Code (3 days)
- **Tasks**:
  - Update query_model.py to use provider interface
  - Create backward compatibility adapter
  - Update cost estimation for basic provider awareness
- **LOC Impact**: ~50 LOC (reduced from 70)

## Dependencies
- **Prerequisites**: Init Files Refactor
- **Dependents**: MLSolver Refactor
- **Required By**: Week 3 of refactoring effort

## Backward Compatibility
- **Breaking Changes**: None (backward compatibility preserved)
- **Migration Path**: Not needed for existing code
- **Compatibility Layer**: Maintain current query_model.py signature and behavior

## Risks and Mitigation
- **Risk 1**: Performance overhead from abstraction - Keep interface minimal
- **Risk 2**: Token counting inconsistency - Use provider's own tokenizers when available

## Minimal Implementation Option
Focus only on:
1. Simplest possible provider interface (generate method only)
2. OpenAI implementation only
3. Adapter in query_model.py that preserves existing behavior

This would enable future improvements while making absolute minimal changes.

## Rollback Plan
1. Keep original query_model.py implementation
2. Add simple conditional to toggle between implementations
3. Revert if any issues arise