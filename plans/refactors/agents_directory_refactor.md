# Agents Directory Refactoring Plan

## Overview
- **Name**: Agent Interface Standardization
- **Target Component**: Agent Classes (`agents/`)
- **Implementation Complexity**: Low (downgraded from Medium) - Minimal changes to interface
- **Timeline**: 1 week (reduced from 2 weeks)
- **Business Value**: Medium - Improves extensibility for new agent types

## Details
- **Total Estimated LOC**: ~120 LOC (reduced from 250)
  - New code: ~80 LOC (reduced from 150)
  - Modified code: ~40 LOC (reduced from 100)
  - Removed code: ~0 LOC (preserving compatibility)

- **New Files to Create**:
  - `agents/interfaces.py`: Minimal agent interfaces (~80 LOC)

- **Files to Modify**:
  - `agents/base_agent.py`: Implement interfaces (~20 LOC changes)
  - `agents/ml_engineer_agent.py`: Update imports (~5 LOC changes)
  - `agents/phd_student_agent.py`: Update imports (~5 LOC changes)
  - `agents/professor_agent.py`: Update imports (~5 LOC changes)
  - `agents/reviewers_agent.py`: Update imports (~5 LOC changes)

## Current Issues Addressed
1. Inconsistent agent interfaces
2. Difficulty creating new agent types
3. Lack of clear agent capabilities

## Implementation Phases
### Phase 1: Interface Design (2 days)
- **Tasks**:
  - Design minimal agent interface
  - Define basic capability system
  - Document extension patterns
- **LOC Impact**: ~80 LOC (reduced from 150)
- **Code Example** (simplified):
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class AgentInterface(ABC):
    """Minimal interface all agents must implement."""
    
    @property
    @abstractmethod
    def agent_type(self) -> str:
        """Get the type identifier for this agent."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """Get the capabilities this agent provides."""
        pass
    
    @abstractmethod
    def process_message(self, message: str) -> str:
        """Process a message and generate a response."""
        pass
```

### Phase 2: BaseAgent Implementation (3 days)
- **Tasks**:
  - Update BaseAgent to implement interfaces
  - Ensure backward compatibility
  - Add minimal documentation
- **LOC Impact**: ~40 LOC (reduced from 50)

## Dependencies
- **Prerequisites**: Init Files Refactor
- **Dependents**: Agents Phases Refactor
- **Required By**: Week 2 of refactoring effort

## Backward Compatibility
- **Breaking Changes**: None (all interfaces additive)
- **Migration Path**: Not needed for existing code
- **Compatibility Layer**: Not required (implementation preserves existing methods)

## Risks and Mitigation
- **Risk 1**: Interface too restrictive - Keep requirements minimal
- **Risk 2**: Performance impact - Keep abstraction lightweight

## Minimal Implementation Option
Focus only on:
1. Core agent interface in separate file
2. Update BaseAgent implementation
3. Skip specialized agent updates initially

This provides a foundation for future improvements with minimal immediate changes.

## Rollback Plan
1. Interfaces are additive and non-breaking
2. Can remove the interface file without affecting functionality