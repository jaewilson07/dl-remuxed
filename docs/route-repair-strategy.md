# Route Functions Repair and Standardization Strategy

## Executive Summary

This document outlines a comprehensive strategy for repairing and standardizing all route functions in the Domo Library. Based on analysis of existing route files, I've identified critical inconsistencies in error handling, import patterns, function signatures, and exception hierarchies that need systematic repair.

## Current State Analysis

### Import Pattern Issues

**Problem**: Inconsistent import aliases for DomoError across routes
```python
# Multiple different patterns found:
from ..client import DomoError as dmde    # Most common
from ..client import DomoError as de      # Also common  
from ..client import DomoError            # Some files
```

**Impact**: Makes error handling inconsistent and creates maintenance confusion.

### Exception Class Issues

**Problem**: Inconsistent exception hierarchies and naming
```python
# Found patterns:
class Dataset_GetError(de.DomoError):      # Wrong base class
class Dataset_CRUDError(de.DomoError):     # Wrong base class  
class Account_GET_Error(dmde.RouteError):  # Correct base class
class User_CrudError(de.RouteError):       # Inconsistent naming
```

**Impact**: Violates the error design strategy and creates confusion about error types.

### Function Signature Issues

**Problem**: Inconsistent parameter ordering and naming
```python
# Multiple patterns found:
async def func(auth: dmda.DomoAuth, entity_id: str, debug_api: bool = False, ...)
async def func(entity_id: str, auth: dmda.DomoAuth, debug_api: bool = False, ...)
async def func(auth, entity_id, debug_api=False, ...)  # Missing type hints
```

**Impact**: Creates inconsistent developer experience and makes the API harder to learn.

### Route Function Decorator Issues

**Problem**: Inconsistent use of `@gd.route_function` decorator
- Some functions have it, others don't
- No clear pattern for when it should be used
- Some files mix decorated and non-decorated functions

## Standardization Strategy

### 1. Import Standardization

**Standard Pattern**:
```python
from typing import Any, List, Optional, Union

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError, AuthError  # Use specific imports
from ..client import get_data as gd
from ..client import response as rgd
```

**Action Items**:
- Remove all `DomoError as dmde/de` imports
- Use specific exception imports from `..client.exceptions`
- Standardize auth import to `from ..client.auth import DomoAuth`
- Ensure consistent typing imports

### 2. Exception Class Standardization

**Standard Patterns** (following error design strategy):
```python
# GET errors - for retrieval failures
class {Module}_GET_Error(RouteError):
    def __init__(self, entity_id: Optional[str] = None, response_data=None, **kwargs):
        super().__init__(
            message=f"{Module} retrieval failed",
            entity_id=entity_id,
            response_data=response_data,
            **kwargs
        )

# Search not found - for empty search results  
class Search{Module}_NotFound(RouteError):
    def __init__(self, search_criteria: str, response_data=None, **kwargs):
        message = f"No {module}s found matching: {search_criteria}"
        super().__init__(
            message=message,
            response_data=response_data,
            additional_context={"search_criteria": search_criteria},
            **kwargs
        )

# CRUD errors - for create/update/delete failures
class {Module}_CRUD_Error(RouteError):
    def __init__(self, operation: str, entity_id: Optional[str] = None, response_data=None, **kwargs):
        message = f"{Module} {operation} operation failed"
        super().__init__(
            message=message,
            entity_id=entity_id,
            response_data=response_data,
            **kwargs
        )

# Sharing errors - for permission/sharing failures  
class {Module}Sharing_Error(RouteError):
    def __init__(self, operation: str, entity_id: Optional[str] = None, response_data=None, **kwargs):
        message = f"{Module} sharing {operation} failed"
        super().__init__(
            message=message,
            entity_id=entity_id,
            response_data=response_data,
            **kwargs
        )
```

### 3. Function Signature Standardization

**Standard Pattern**:
```python
@gd.route_function  # Always use decorator for route functions
async def function_name(
    # 1. Required auth parameter (always first)
    auth: DomoAuth,
    
    # 2. Primary entity parameters
    entity_id: str,
    
    # 3. Operation-specific parameters
    operation_param: str,
    operation_list: List[str],
    
    # 4. Optional operation parameters
    optional_param: Optional[str] = None,
    
    # 5. Standard control parameters (always in this order)
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
```

**Parameter Guidelines**:
- **auth**: Always first parameter, always typed as `DomoAuth`
- **entity_id**: Primary entity identifier, second if required
- **operation params**: Specific to the function's purpose
- **Standard params**: Always in the same order at the end
- **Type hints**: Always include complete type hints
- **Return type**: Always specify return type

### 4. Error Handling Standardization

**Standard Pattern**:
```python
@gd.route_function
async def get_entity_by_id(
    auth: DomoAuth,
    entity_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve a specific entity by ID.
    
    Args:
        auth: Authentication object
        entity_id: Unique identifier for the entity
        session: HTTP client session (optional)
        debug_api: Enable API debugging
        debug_num_stacks_to_drop: Stack frames to drop for debugging
        parent_class: Name of calling class for debugging
        return_raw: Return raw response without processing
        
    Returns:
        ResponseGetData object containing entity data
        
    Raises:
        Entity_GET_Error: If entity retrieval fails
        SearchEntity_NotFound: If entity doesn't exist
    """
    url = f"https://{auth.domo_instance}.domo.com/api/entity/v1/{entity_id}"
    
    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        session=session,
        debug_api=debug_api,
        num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )
    
    if return_raw:
        return res
        
    # Handle specific error cases
    if not res.is_success:
        if res.status == 404:
            raise SearchEntity_NotFound(
                search_criteria=f"ID: {entity_id}",
                response_data=res
            )
        else:
            raise Entity_GET_Error(
                entity_id=entity_id,
                response_data=res
            )
    
    return res
```

## Route-by-Route Repair Plan

### Phase 1: Critical Infrastructure Routes (Week 1)

**Priority Order**:
1. **auth.py** ✅ (Already completed)
2. **user.py** - Critical for user management
3. **dataset.py** - Core data functionality  
4. **account.py** - Authentication dependencies
5. **role.py** - Permission system

### Phase 2: Core Entity Routes (Week 2)

6. **card.py** - Dashboard functionality
7. **page.py** - Page management
8. **dataflow.py** - Data processing
9. **group.py** - User groups
10. **grant.py** - Permissions

### Phase 3: Configuration Routes (Week 3)

11. **instance_config.py** - Instance settings
12. **instance_config_sso.py** - SSO configuration
13. **instance_config_api_client.py** - API management
14. **instance_config_mfa.py** - Multi-factor auth
15. **instance_config_scheduler_policies.py** - Scheduling

### Phase 4: Specialized Routes (Week 4)

16. **application.py** - App management
17. **appstudio.py** - App development
18. **codeengine.py** - Code execution
19. **jupyter.py** - Jupyter integration
20. **ai.py** - AI features

### Phase 5: Supporting Routes (Week 5)

21. **activity_log.py** - Audit logging
22. **bootstrap.py** - System initialization
23. **datacenter.py** - Data center management
24. **enterprise_apps.py** - Enterprise features
25. **stream.py** - Data streaming

## Repair Process for Each Route

### Step 1: Import Standardization
```python
# Replace inconsistent imports with standard pattern
from typing import Any, List, Optional, Union

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError, AuthError, ClassError
from ..client import get_data as gd 
from ..client import response as rgd
from ..client.entities import DomoEnum  # If needed
```

### Step 2: Exception Class Repair
- Rename classes to follow naming convention
- Update base classes to use correct hierarchy
- Add proper constructors with standard parameters
- Include comprehensive docstrings

### Step 3: Function Signature Repair
- Reorder parameters to follow standard pattern
- Add missing type hints
- Ensure consistent parameter naming
- Add `@gd.route_function` decorator where missing

### Step 4: Error Handling Repair
- Replace generic exceptions with specific route errors
- Add proper error context and messages
- Include entity IDs in error reporting
- Follow error handling patterns from design strategy

### Step 5: Documentation Enhancement
- Add comprehensive docstrings to all functions
- Include parameter descriptions
- Document expected exceptions
- Add usage examples

## Quality Assurance Standards

### Automated Checks
1. **Lint Validation**: All functions must pass type checking
2. **Import Consistency**: Verify standard import patterns
3. **Exception Testing**: Test all error scenarios
4. **Documentation Coverage**: Ensure all functions have docstrings

### Manual Review Checklist
- [ ] Follows standard import pattern
- [ ] Uses correct exception hierarchy
- [ ] Has proper function signature
- [ ] Includes comprehensive error handling
- [ ] Has complete docstrings
- [ ] Follows naming conventions
- [ ] Includes type hints
- [ ] Uses `@gd.route_function` decorator

## Implementation Timeline

### Week 1: Foundation (Auth, User, Dataset, Account, Role)
- Highest priority routes that other modules depend on
- Establish patterns for other routes to follow
- Critical for basic library functionality

### Week 2: Core Entities (Card, Page, Dataflow, Group, Grant)  
- Core business logic routes
- High usage functionality
- Dashboard and data management

### Week 3: Configuration (Instance Config Routes)
- System configuration and settings
- SSO and authentication configuration
- Less urgent but important for admin functionality

### Week 4: Specialized (Application, AppStudio, CodeEngine, Jupyter, AI)
- Advanced features and integrations
- Lower priority but important for complete functionality
- Specialized use cases

### Week 5: Supporting (Activity Log, Bootstrap, etc.)
- Supporting and utility routes
- Lower priority maintenance functions
- Can be done in parallel with other work

## Success Metrics

1. **Code Quality**: 100% type hint coverage, zero lint errors
2. **Consistency**: All routes follow identical patterns
3. **Error Handling**: Comprehensive error coverage with specific exceptions
4. **Documentation**: Complete docstring coverage
5. **Testing**: All error scenarios tested
6. **Developer Experience**: Consistent API patterns across all routes

## Benefits

1. **Maintainability**: Consistent patterns make code easier to maintain
2. **Debugging**: Better error messages and context
3. **Developer Experience**: Predictable API patterns
4. **Testing**: Easier to write comprehensive tests
5. **Error Recovery**: Specific exceptions enable targeted error handling
6. **Documentation**: Better API documentation through consistency

This strategy provides a systematic approach to bringing all route functions up to modern standards while maintaining backward compatibility and improving the overall developer experience.