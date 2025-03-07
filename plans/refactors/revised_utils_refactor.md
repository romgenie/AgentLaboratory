# Utils Refactoring Plan

## Overview
- **Name**: Core Utilities Standardization
- **Target Component**: Utility modules (`utils/`)
- **Implementation Complexity**: Low - Focused on minimal organization improvements
- **Timeline**: 3 days (reduced from 1 week)
- **Business Value**: Medium - Improves code reusability and maintenance

## Details
- **Total Estimated LOC**: ~100 LOC (reduced from 200)
  - New code: ~80 LOC (reduced from 150)
  - Modified code: ~20 LOC (reduced from 50)
  - Removed code: ~0 LOC (preserving compatibility)

- **New Files to Create**:
  - `utils/validation.py`: Essential validation utilities (~50 LOC)
  - `utils/constants.py`: System-wide constants (~30 LOC)

- **Files to Modify**:
  - `utils/__init__.py`: Update exports (~10 LOC changes)
  - `utils/file_utils.py`: Add cross-references (~5 LOC changes)
  - `utils/text_utils.py`: Add cross-references (~5 LOC changes)

## Current Issues Addressed
1. Duplicated validation logic across modules
2. Scattered constants and configuration values
3. Missing documentation for common operations

## Implementation Phases
### Phase 1: Core Validation Utilities (2 days)
- **Tasks**:
  - Create essential validation functions
  - Add comprehensive docstrings
  - Ensure type hints for IDE support
- **LOC Impact**: ~50 LOC
- **Code Example** (simplified):
```python
"""Core validation utilities for the system."""
from typing import Any, Dict, Optional
import os

def validate_file_path(path: str, must_exist: bool = True) -> str:
    """Validate a file path and return its absolute path.
    
    Args:
        path: The file path to validate
        must_exist: Whether the file must already exist
        
    Returns:
        The absolute path to the file
        
    Raises:
        ValueError: If the path is invalid or the file doesn't exist
    """
    if not path:
        raise ValueError("File path cannot be empty")
        
    abs_path = os.path.abspath(os.path.expanduser(path))
    
    if must_exist and not os.path.exists(abs_path):
        raise ValueError(f"File does not exist: {abs_path}")
        
    return abs_path
```

### Phase 2: Constants and Cross-References (1 day)
- **Tasks**:
  - Consolidate common constants
  - Add import forwarding in __init__.py
  - Add cross-references between utility files
- **LOC Impact**: ~50 LOC

## Dependencies
- **Prerequisites**: Init Files Refactor
- **Dependents**: Most other refactors use utilities
- **Required By**: Week 1 of refactoring effort

## Backward Compatibility
- **Breaking Changes**: None (all changes preserve existing functionality)
- **Migration Path**: Not needed for existing code
- **Compatibility Layer**: Use import forwarding in __init__.py

## Risks and Mitigation
- **Risk 1**: Breaking imports in dependent code - Use import forwarding
- **Risk 2**: Inconsistent function signatures - Document with type hints

## Minimal Implementation Option
Focus only on:
1. Create validation.py with the most commonly used validations
2. Skip constants file entirely

This addresses the most critical reuse needs with minimal change.

## Rollback Plan
1. All changes preserve original functionality
2. Can revert individual files without affecting others