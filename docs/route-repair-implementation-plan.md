# Route Function Repair Implementation Plan

## Current Status

After analyzing the route functions, I've identified several categories of issues that need systematic repair. **Progress Update**: access_token.py has been successfully completed and now serves as a template for other route repairs.

### ✅ Completed Routes
- **auth.py** - Clean, modern implementation (already completed)
- **access_token.py** - ✅ **NEWLY COMPLETED** - Fully standardized with:
  - Standardized imports (`from ..client.exceptions import RouteError`)
  - Proper exception classes (`AccessToken_GET_Error`, `SearchAccessToken_NotFound`, `AccessToken_CRUD_Error`)
  - All functions use `@gd.route_function` decorator
  - Consistent function signatures with `return_raw: bool = False` parameter
  - Comprehensive docstrings with Args/Returns/Raises sections
  - Zero lint errors - validated and ready for use

### 1. Critical Import Issues (RESOLVED in completed routes)
- ✅ Inconsistent DomoError import patterns (`as de`, `as dmde`, direct imports) - **FIXED**
- ✅ Missing or incorrect type annotations - **FIXED**
- ✅ Outdated auth import patterns - **FIXED**

### 2. Exception Class Issues (RESOLVED in completed routes)
- ✅ Wrong base classes (using DomoError instead of RouteError) - **FIXED**
- ✅ Inconsistent naming conventions - **FIXED**
- ✅ Missing or poor error context - **FIXED**

### 3. Function Signature Issues (RESOLVED in completed routes)
- ✅ Inconsistent parameter ordering - **FIXED**
- ✅ Missing type hints (especially Optional types) - **FIXED**
- ✅ Incorrect default parameter patterns - **FIXED**
- ✅ Missing `@gd.route_function` decorator - **FIXED**
- ✅ Missing `return_raw: bool = False` parameter - **FIXED**

### 4. Remaining Issues in Other Routes
The remaining routes still have structural problems similar to what was fixed in access_token.py:
- Complex functions with mixed responsibilities
- Inconsistent error handling patterns
- Type annotation issues throughout
- Missing proper Optional type usage
- Missing route function decorators and return_raw patterns

## Immediate Action Plan

### Phase 1: Build on Successfully Completed Templates

We now have two excellent templates that demonstrate the standardized patterns:

#### ✅ **auth.py** (Completed)
- Clean, modern implementation
- Serves as template for authentication patterns

#### ✅ **access_token.py** (Completed) 
- **PERFECT TEMPLATE** for standard route patterns
- Demonstrates all required standardization elements:
  - Proper imports: `from ..client.exceptions import RouteError`
  - Exception classes: `AccessToken_GET_Error`, `SearchAccessToken_NotFound`, `AccessToken_CRUD_Error`
  - Function decorators: `@gd.route_function` on all route functions
  - Parameter patterns: `return_raw: bool = False` on all functions
  - Comprehensive documentation with Args/Returns/Raises
  - Zero lint errors

#### Next Priority Routes (Using access_token.py as template):

#### 1. **account.py** - Next Target (HIGH PRIORITY)
- **Status**: Needs repair - has `from ..client import exceptions as dmde` pattern
- **Complexity**: Medium - simpler structure than user.py
- **Impact**: High - core account management functionality
- **Template**: Use access_token.py patterns for exception classes and function signatures

#### 2. **card.py** - Quick Win (HIGH PRIORITY)
- **Status**: Needs repair
- **Complexity**: Low - relatively simple structure  
- **Impact**: High - dashboard functionality
- **Template**: Direct application of access_token.py patterns

#### 3. **role.py** - Foundation Dependency (HIGH PRIORITY)
- **Status**: Needs repair
- **Complexity**: Medium - needed by user.py
- **Impact**: High - critical for permission system
- **Template**: Use access_token.py exception patterns

### Phase 2: Apply access_token.py Template to Remaining Routes

Now that we have a perfect template in access_token.py, we can systematically apply the same patterns:

#### Standard Template Pattern (from access_token.py):
```python
# 1. Module docstring with functions and exceptions listed
"""
{Module} Route Functions

Functions:
    function_name: Description
    
Exception Classes:
    {Module}_GET_Error: Raised when retrieval fails
    Search{Module}_NotFound: Raised when search returns no results  
    {Module}_CRUD_Error: Raised when create/update/delete operations fail
"""

# 2. Standardized imports
from typing import Optional, Union
import httpx
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd

# 3. Exception classes
class {Module}_GET_Error(RouteError):
    def __init__(self, entity_id: Optional[str] = None, res=None, **kwargs):
        # Standard constructor pattern

# 4. Route functions
@gd.route_function
async def function_name(
    auth: DomoAuth,
    entity_id: str,
    # ... operation-specific params
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Comprehensive docstring with Args/Returns/Raises"""
    
    res = await gd.get_data(...)
    
    if return_raw:
        return res
        
    if not res.is_success:
        raise CustomError(res=res)
    
    return res
```

### Phase 3: Priority Order for Remaining Routes

With access_token.py as our proven template, here's the recommended repair order:

#### Week 1: High-Impact Core Routes
1. **account.py** - Account management (use access_token.py template)
2. **card.py** - Dashboard functionality (simple structure)
3. **role.py** - Permission system (needed by user.py)
4. **dataset.py** - Core data functionality

#### Week 2: Entity Management Routes
5. **user.py** - User management (complex, save for after role.py)
6. **group.py** - User groups (depends on user.py patterns)
7. **page.py** - Page management
8. **dataflow.py** - Data processing

#### Week 3: Configuration Routes
9. **instance_config.py** - Instance settings
10. **instance_config_sso.py** - SSO configuration
11. **instance_config_api_client.py** - API management
12. **grant.py** - Permissions (depends on role.py)

#### Week 4: Specialized Routes
13. **application.py** - App management
14. **appstudio.py** - App development
15. **jupyter.py** - Jupyter integration
16. **ai.py** - AI features

#### Week 5: Supporting Routes
17. **activity_log.py** - Audit logging
18. **bootstrap.py** - System initialization
19. **stream.py** - Data streaming
20. **enterprise_apps.py** - Enterprise features

## Recommended Next Steps

1. **Start with account.py** - Apply access_token.py template directly
   - Replace `from ..client import exceptions as dmde` with standardized imports
   - Create `Account_GET_Error`, `SearchAccount_NotFound`, `Account_CRUD_Error` classes
   - Add `@gd.route_function` decorators to all route functions
   - Add `return_raw: bool = False` parameter to all functions
   - Update function signatures following access_token.py patterns

2. **Use access_token.py as the template** - It demonstrates perfect implementation of:
   - ✅ Standardized imports and exception classes
   - ✅ Route function decorators on all functions
   - ✅ Consistent parameter patterns with return_raw
   - ✅ Comprehensive documentation
   - ✅ Zero lint errors

3. **Apply systematic repairs** using the proven template pattern

This approach will:
- ✅ **Build on proven success** - access_token.py is the perfect template
- ✅ **Maintain consistency** - all routes will follow identical patterns  
- ✅ **Ensure quality** - template has zero errors and comprehensive coverage
- ✅ **Enable rapid progress** - clear pattern to follow for each route

## Success Metrics (Based on access_token.py achievements)

✅ **Template Established**: access_token.py demonstrates all required patterns
✅ **Zero Lint Errors**: Proven error-free implementation  
✅ **Complete Documentation**: Comprehensive docstrings with Args/Returns/Raises
✅ **Standardized Exceptions**: RouteError-based hierarchy with proper context
✅ **Function Decorators**: All route functions use @gd.route_function
✅ **Return Raw Pattern**: All functions include return_raw parameter with immediate return
✅ **Type Safety**: Complete type hints throughout

## Implementation Strategy for account.py

Now that access_token.py has been completed as the perfect template, let's apply the same patterns to account.py:

### Current Issues in account.py:
1. ❌ Import pattern: `from ..client import exceptions as dmde` (needs standardization)
2. ❌ Function signatures missing Optional types and return_raw parameter
3. ❌ Exception classes need standardization to RouteError base
4. ❌ Missing @gd.route_function decorators
5. ❌ Missing comprehensive docstrings

### Target Pattern (Following access_token.py template):
```python
"""
Account Route Functions

This module provides functions for managing Domo accounts including retrieval,
creation, and management operations.

Functions:
    get_accounts: Retrieve all accounts
    get_account_by_id: Retrieve a specific account by ID
    # ... other functions

Exception Classes:
    Account_GET_Error: Raised when account retrieval fails
    SearchAccount_NotFound: Raised when account search returns no results
    Account_CRUD_Error: Raised when account create/update/delete operations fail
"""

from typing import Optional, Union
import httpx
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd

class Account_GET_Error(RouteError):
    # Follow access_token.py pattern exactly

@gd.route_function
async def get_account_by_id(
    auth: DomoAuth,
    account_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve a specific account by ID."""
    
    res = await gd.get_data(...)
    
    if return_raw:
        return res
        
    if not res.is_success:
        raise Account_GET_Error(res=res)
    
    return res
```

This approach focuses on:
- ✅ **Proven template** - access_token.py demonstrates perfect implementation
- ✅ **Direct application** - copy patterns exactly from the template  
- ✅ **Systematic approach** - apply same repairs to each route function
- ✅ **Quality assurance** - follow the zero-error template exactly