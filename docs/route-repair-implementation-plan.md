# Route Function Repair Implementation Plan

## Current Status

After analyzing the route functions, I've identified several categories of issues that need systematic repair. **Progress Update**: access_token.py has been successfully completed and now serves as a template for other route repairs.

### ✅ Completed Routes (Templates)
- **auth.py** - Clean, modern implementation (already completed)
- **access_token.py** - ✅ **NEWLY COMPLETED** - Fully standardized with:
  - Standardized imports (`from ..client.exceptions import RouteError`)
  - Proper exception classes (`AccessToken_GET_Error`, `SearchAccessToken_NotFound`, `AccessToken_CRUD_Error`)
  - All functions use `@gd.route_function` decorator
  - Consistent function signatures with `return_raw: bool = False` parameter
  - Comprehensive docstrings with Args/Returns/Raises sections
  - Zero lint errors - validated and ready for use

## Standard Template Pattern (from access_token.py)

All route repairs should follow this exact pattern:

### 1. Module Structure Template
```python
"""
{Module} Route Functions

This module provides functions for managing Domo {module}s including retrieval,
creation, and management operations.

Functions:
    get_{module}s: Retrieve all {module}s
    get_{module}_by_id: Retrieve a specific {module} by ID
    search_{module}s: Search for {module}s matching criteria
    create_{module}: Create a new {module}
    update_{module}: Update an existing {module}
    delete_{module}: Delete a {module}

Exception Classes:
    {Module}_GET_Error: Raised when {module} retrieval fails
    Search{Module}_NotFound: Raised when {module} search returns no results
    {Module}_CRUD_Error: Raised when {module} create/update/delete operations fail
    {Module}Sharing_Error: Raised when {module} sharing operations fail (if applicable)
"""

__all__ = [
    "{Module}_GET_Error",
    "Search{Module}_NotFound",
    "{Module}_CRUD_Error",
    "{Module}Sharing_Error",  # If applicable
    "get_{module}s",
    "get_{module}_by_id",
    "search_{module}s",
    "create_{module}",
    "update_{module}",
    "delete_{module}",
]

from typing import Any, List, Optional, Union

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
```

### 2. Exception Classes Template
```python
class {Module}_GET_Error(RouteError):
    """Raised when {module} retrieval operations fail."""

    def __init__(
        self,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "{Module} retrieval failed",
            entity_id={module}_id,
            res=res,
            **kwargs,
        )


class Search{Module}_NotFound(RouteError):
    """Raised when {module} search operations return no results."""

    def __init__(
        self,
        search_criteria: str,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"No {module}s found matching: {search_criteria}",
            res=res,
            additional_context={"search_criteria": search_criteria},
            **kwargs,
        )


class {Module}_CRUD_Error(RouteError):
    """Raised when {module} create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"{Module} {operation} operation failed",
            entity_id={module}_id,
            res=res,
            **kwargs,
        )


class {Module}Sharing_Error(RouteError):
    """Raised when {module} sharing operations fail."""

    def __init__(
        self,
        operation: str,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        res=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"{Module} sharing {operation} failed",
            entity_id={module}_id,
            res=res,
            **kwargs,
        )
```

### 3. Function Signature Template
```python
@gd.route_function
async def get_{module}_by_id(
    auth: DomoAuth,
    {module}_id: str,
    # Operation-specific parameters here
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve a specific {module} by ID.

    Args:
        auth: Authentication object containing credentials and instance info
        {module}_id: Unique identifier for the {module}
        session: Optional httpx client session for connection reuse
        debug_api: Enable detailed API request/response logging
        debug_num_stacks_to_drop: Number of stack frames to drop in debug output
        parent_class: Optional parent class name for debugging context
        return_raw: Return raw API response without processing

    Returns:
        ResponseGetData object containing {module} information

    Raises:
        {Module}_GET_Error: If {module} retrieval fails
        Search{Module}_NotFound: If {module} with specified ID doesn't exist
    """
    url = f"https://{auth.domo_instance}.domo.com/api/{module}/v1/{module}_id"

    res = await gd.get_data(
        auth=auth,
        url=url,
        method="GET",
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=parent_class,
    )

    if return_raw:
        return res

    if not res.is_success:
        if res.status == 404:
            raise Search{Module}_NotFound(
                search_criteria=f"{module}_id: {module}_id}",
                res=res,
            )
        raise {Module}_GET_Error({module}_id={module}_id, res=res)

    return res
```

## Route Classification and Repair Strategy

### Simple Routes (Apply template directly - 1-2 hours each)
Apply access_token.py template directly with minimal customization:

1. **beastmode.py** (272 lines)
   - Current: `BeastModes_API_Error`
   - Needed: `BeastMode_GET_Error`, `BeastMode_CRUD_Error`

2. **codeengine.py** (243 lines)
   - Current: `CodeEngine_API_Error`
   - Needed: `CodeEngine_GET_Error`, `CodeEngine_CRUD_Error`

3. **enterprise_apps.py** (263 lines)
   - Current: `App_API_Exception`
   - Needed: `EnterpriseApp_GET_Error`, `EnterpriseApp_CRUD_Error`

4. **pdp.py** (307 lines)
   - Current: `PDP_NotRetrieved`
   - Needed: `PDP_GET_Error`, `PDP_CRUD_Error`

5. **instance_config_mfa.py** (261 lines)
   - Current: `MFA_UPDATE_Error`, `MFA_UPDATE_Value_Error`
   - Needed: `MFA_GET_Error`, `MFA_CRUD_Error`

### Medium Complexity Routes (Apply template with customization - 2-4 hours each)

6. **card.py** (266 lines)
   - Current: `Cards_API_Exception`, `CardSearch_NotFoundError`
   - Needed: `Card_GET_Error`, `Card_CRUD_Error`, `SearchCard_NotFound`

7. **application.py** (462 lines)
   - Current: `Application_GET_Error`, `ApplicationError_NoneRetrieved`
   - Needed: Add `Application_CRUD_Error`, `SearchApplication_NotFound`

8. **group.py** (646 lines)
   - Current: `Group_GET_Error`, `SearchGroups_Error`
   - Needed: Add `Group_CRUD_Error`, `SearchGroup_NotFound`, `GroupSharing_Error`

9. **role.py** (435 lines) - **PRIORITY for user.py dependency**
   - Current: `Role_NotRetrieved`, `Role_CRUD_Error`
   - Needed: Rename `Role_NotRetrieved` to `Role_GET_Error`

10. **page.py** (370 lines)
    - Current: `Page_GET_Error`, `PageRetrieval_byId_Error`
    - Needed: Add `Page_CRUD_Error`, `SearchPage_NotFound`, `PageSharing_Error`

### Complex Routes (May need restructuring - 4-8 hours each)

11. **dataset.py** (900+ lines) - **HIGHEST PRIORITY**
    - **Strategy**: Split into submodules following account/ pattern:
    ```
    dataset/
    ├── __init__.py          # Main exports
    ├── core.py              # GET operations
    ├── crud.py              # Create/Update/Delete
    ├── exceptions.py        # All error classes
    ├── query.py             # Query operations
    ├── upload.py            # Upload operations
    └── sharing.py           # Sharing operations
    ```

12. **user.py** (953+ lines) - **Complex, depends on role.py**
    - Current: Multiple error patterns
    - Strategy: Apply template after role.py completion
    - Dependencies: role.py must be completed first

13. **instance_config.py** (684 lines)
    - Current: `ToggleSocialUsers_Error`
    - Needed: `InstanceConfig_GET_Error`, `InstanceConfig_CRUD_Error`

14. **instance_config_sso.py** (539 lines)
    - Current: `SSO_AddUserDirectSignonError`
    - Needed: `SSO_GET_Error`, `SSO_CRUD_Error`

## Step-by-Step Repair Process

### Phase 1: Validate Infrastructure (Before route repairs)

**Validate Core Components**:
```python
# Test basic functionality:
from src.client import get_data as gd
from src.client import response as rgd
from src.client.auth import DomoAuth

# Verify these work as expected
```

**Test Exception Integration**:
```python
# Test exception construction:
from src.client.exceptions import RouteError

error = RouteError(message="test", res=None)
print(error)  # Should work without issues
```

### Phase 2: Apply Template to Individual Routes

For each route file, follow this exact process:

#### Step 1: Import Standardization
```python
# Replace ALL imports with standard pattern
from typing import Any, List, Optional, Union

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
```

#### Step 2: Exception Class Standardization
- Replace all existing error classes with standard pattern
- Use exact naming: `{Module}_GET_Error`, `Search{Module}_NotFound`, `{Module}_CRUD_Error`
- Follow constructor pattern from access_token.py exactly

#### Step 3: Function Signature Standardization
- Add `@gd.route_function` decorator to ALL route functions
- Add `return_raw: bool = False` parameter to ALL functions
- Ensure parameter order: auth, entity_id, operation_params, session, debug_*, return_raw
- Add complete type hints following access_token.py pattern

#### Step 4: Function Body Updates
```python
@gd.route_function
async def function_name(..., return_raw: bool = False) -> rgd.ResponseGetData:
    res = await gd.get_data(...)

    # CRITICAL: Immediate return_raw check
    if return_raw:
        return res

    # Error handling only after return_raw check
    if not res.is_success:
        if res.status == 404:
            raise Search{Module}_NotFound(search_criteria="...", res=res)
        raise {Module}_GET_Error(entity_id=entity_id, res=res)

    return res
```

#### Step 5: Documentation Updates
- Add comprehensive module docstring listing all functions and exceptions
- Add complete function docstrings with Args/Returns/Raises sections
- Update `__all__` exports to include all new exception classes

#### Step 6: Validation
- Run type checking to ensure zero lint errors
- Test basic import functionality
- Verify exception handling works correctly
