# CodeEngine Module Refactoring Summary

## Overview
The `codeengine.py` and `codeengine_crud.py` files have been refactored into a structured package following the standardized route pattern used elsewhere in the project (e.g., `account/` subdirectory).

## Changes Made

### 1. Created `routes/codeengine/` Subdirectory
Following the pattern established by `routes/account/`, the codeengine functionality has been organized into a package structure:

```
routes/codeengine/
├── __init__.py          # Package exports
├── exceptions.py        # Standardized error classes
├── core.py             # GET/retrieval operations
└── crud.py             # Create/Update/Deploy operations
```

### 2. Standardized Error Classes (`exceptions.py`)
All error classes now inherit from `RouteError` (instead of `DomoError`) following the error design strategy:

- **`CodeEngine_GET_Error`**: Raised when codeengine retrieval operations fail
  - Replaces: `CodeEngine_API_Error` (for GET operations)
  - Pattern: `RouteError` with `entity_id` and `res` parameters
  
- **`SearchCodeEngine_NotFound`**: Raised when search returns no results
  - New error class following standard pattern
  - Includes `search_criteria` in context
  
- **`CodeEngine_CRUD_Error`**: Raised when create/update/delete operations fail
  - Replaces: `CodeEngine_API_Error` (for CRUD operations)
  - Includes `operation` parameter to specify which operation failed
  
- **`CodeEngine_InvalidPackage`**: Raised when package validation fails
  - Kept from original but now inherits from `RouteError`
  - Used for business logic validation errors
  
- **`CodeEngine_FunctionCallError`**: Raised when function parameters are invalid
  - Kept from original but now inherits from `RouteError`
  - Used for parameter validation errors

### 3. Core Functions (`core.py`)
GET and retrieval operations:
- `get_packages()`: Retrieve all codeengine packages
- `get_codeengine_package_by_id()`: Retrieve specific package
- `get_package_versions()`: Retrieve all versions of a package
- `get_codeengine_package_by_id_and_version()`: Retrieve specific version
- `test_package_is_released()`: Test if package is released
- `test_package_is_identical()`: Test if package code is identical

**Improvements:**
- All functions use `@gd.route_function` decorator
- Added `return_raw: bool = False` parameter to all route functions
- Added proper type hints (`-> rgd.ResponseGetData`)
- Added comprehensive docstrings with Args/Returns/Raises
- Replaced generic error handling with specific error classes

### 4. CRUD Functions (`crud.py`)
Create, update, and deployment operations:
- `deploy_code_engine_package()`: Deploy a package version
- `create_code_engine_package()`: Create new package
- `increment_version()`: Version number helper
- `upsert_code_engine_package_version()`: Create or update version
- `upsert_package()`: Create or update package

**Improvements:**
- All functions use `@gd.route_function` decorator
- Added `return_raw: bool = False` parameter
- Added proper type hints
- Added comprehensive docstrings
- Use specific error classes (`CodeEngine_CRUD_Error` instead of `CodeEngine_API_Error`)

### 5. Backward Compatibility
The original `codeengine.py` and `codeengine_crud.py` files have been updated to:
- Import and re-export all functionality from the new package
- Maintain backward compatibility alias: `CodeEngine_API_Error = CodeEngine_GET_Error`
- Preserve all existing function signatures
- Include deprecation notices in docstrings

This ensures existing code continues to work without modification.

## Benefits

### 1. Consistency
- Follows the same pattern as `account/`, `user/`, and other structured routes
- Makes the codebase more predictable and easier to navigate
- Standardized error handling across all routes

### 2. Maintainability
- Separation of concerns (GET vs CRUD operations)
- Easier to find and modify specific functionality
- Clear organization of related functions

### 3. Error Handling
- Specific error classes for different failure modes
- Better debugging with contextual error information
- Follows RouteError pattern for automatic context extraction

### 4. Type Safety
- Complete type hints on all functions
- Proper return type annotations
- Better IDE support and static analysis

### 5. Documentation
- Comprehensive docstrings on all functions
- Clear separation of exception classes
- Better API documentation

## Migration Guide

### For New Code
Import directly from the package:
```python
from domolibrary2.routes.codeengine import (
    get_packages,
    CodeEngine_GET_Error,
    CodeEngine_CRUD_Error,
)
```

### For Existing Code
No changes required - backward compatibility is maintained:
```python
# This still works
from domolibrary2.routes.codeengine import get_packages
from domolibrary2.routes.codeengine_crud import create_code_engine_package

# CodeEngine_API_Error is aliased to CodeEngine_GET_Error
try:
    result = await get_packages(auth=auth)
except CodeEngine_API_Error as e:  # Still works
    print(e)
```

### Recommended Updates
While not required, consider updating to use specific error classes:
```python
# Old approach
try:
    result = await get_packages(auth=auth)
except CodeEngine_API_Error as e:
    print(e)

# New approach (more specific)
try:
    result = await get_packages(auth=auth)
except CodeEngine_GET_Error as e:  # For GET operations
    print(f"Failed to retrieve packages: {e}")
except CodeEngine_CRUD_Error as e:  # For CRUD operations
    print(f"Failed to modify package: {e}")
```

## Validation

All changes have been validated:
- ✅ Python syntax validation passed
- ✅ Directory structure follows account/ pattern
- ✅ All error classes inherit from RouteError
- ✅ All route functions have @gd.route_function decorator
- ✅ All route functions have return_raw parameter
- ✅ All route functions have proper type hints
- ✅ Backward compatibility maintained
- ✅ All exports properly defined in __all__

## Files Changed

### New Files
- `src/domolibrary2/routes/codeengine/__init__.py`
- `src/domolibrary2/routes/codeengine/exceptions.py`
- `src/domolibrary2/routes/codeengine/core.py`
- `src/domolibrary2/routes/codeengine/crud.py`

### Modified Files
- `src/domolibrary2/routes/codeengine.py` (now a compatibility shim)
- `src/domolibrary2/routes/codeengine_crud.py` (now a compatibility shim)

## Next Steps

This refactoring sets the foundation for:
1. Adding more specific error handling
2. Implementing additional codeengine features
3. Better testing with mocked responses
4. Enhanced documentation and examples

## References
- Error Design Strategy: `docs/error-design-strategy.md`
- Route Refactoring Guide: `docs/route-refactoring-guide.md`
- Route Standards: `.github/instructions/routes.md`
