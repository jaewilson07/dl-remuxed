# Route Refactoring Guide

## Overview
This guide provides instructions for refactoring route files to align with the error design strategy.

## Completed Routes (8/38)
The following routes have been successfully refactored:
1. ✅ `access_token.py` - Already complete (pre-existing)
2. ✅ `account.py` and `account/` - Already complete (pre-existing)
3. ✅ `activity_log.py` - Refactored with ActivityLog_GET_Error
4. ✅ `ai.py` - Refactored with AI_GET_Error, AI_CRUD_Error
5. ✅ `bootstrap.py` - Refactored with Bootstrap_GET_Error
6. ✅ `filesets.py` - Refactored with Fileset_GET_Error, Fileset_CRUD_Error
7. ✅ `grant.py` - Refactored with Grant_GET_Error
8. ✅ `sandbox.py` - Refactored with Sandbox_GET_Error, Sandbox_CRUD_Error
9. ✅ `stream.py` - Refactored with Stream_GET_Error, Stream_CRUD_Error
10. ✅ `workflows.py` - Refactored with Workflow_GET_Error, Workflow_CRUD_Error

## Routes Requiring Refactoring (28 remaining)

### Simple Routes (Small files, straightforward refactoring)
These routes need standard GET/CRUD error classes:

1. **beastmode.py** (272 lines)
   - Current: `BeastModes_API_Error`
   - Needed: `BeastMode_GET_Error`, `BeastMode_CRUD_Error`

2. **codeengine.py** (243 lines)
   - Current: `CodeEngine_API_Error`
   - Needed: `CodeEngine_GET_Error`, `CodeEngine_CRUD_Error`

3. **codeengine_crud.py** (223 lines)
   - Review needed - appears to be utilities, may not need error classes

4. **enterprise_apps.py** (263 lines)
   - Current: `App_API_Exception`
   - Needed: `EnterpriseApp_GET_Error`, `EnterpriseApp_CRUD_Error`

5. **instance_config_api_client.py** (229 lines)
   - Current: `ApiClient_GET_Error`
   - Action: Verify naming, may already be correct

6. **instance_config_instance_switcher.py** (112 lines)
   - Current: `InstanceSwitcherMapping_GET_Error`, `InstanceSwitcherMapping_CRUD_Error`
   - Action: Verify naming, may already be correct

7. **instance_config_mfa.py** (261 lines)
   - Current: `MFA_UPDATE_Error`, `MFA_UPDATE_Value_Error`
   - Needed: `MFA_GET_Error`, `MFA_CRUD_Error`

8. **instance_config_scheduler_policies.py** (229 lines)
   - Current: `Scheduler_Policies_Error`
   - Needed: `SchedulerPolicy_GET_Error`, `SchedulerPolicy_CRUD_Error`

9. **pdp.py** (307 lines)
   - Current: `PDP_NotRetrieved`
   - Needed: `PDP_GET_Error`, `PDP_CRUD_Error`

### Medium Complexity Routes
These routes may need additional specialized error classes:

10. **application.py** (462 lines)
    - Current: `Application_GET_Error`, `ApplicationError_NoneRetrieved`
    - Needed: Add `Application_CRUD_Error`, `SearchApplication_NotFound`

11. **appdb.py** (422 lines)
    - Current: `AppDb_GET_Exception`, `AppDb_CRUD_Exception`
    - Needed: Rename to `AppDb_GET_Error`, `AppDb_CRUD_Error`

12. **appstudio.py** (324 lines)
    - Current: `AppStudio_API_Error`, `AppStudio_CRUD_Error`, `AppStudioSharing_Error`
    - Action: Rename `AppStudio_API_Error` to `AppStudio_GET_Error`

13. **card.py** (266 lines)
    - Current: `Cards_API_Exception`, `CardSearch_NotFoundError`
    - Needed: `Card_GET_Error`, `Card_CRUD_Error`, `SearchCard_NotFound`

14. **dataflow.py** (387 lines)
    - Current: `GET_Dataflow_Error`, `CRUD_Dataflow_Error`
    - Needed: Rename to `Dataflow_GET_Error`, `Dataflow_CRUD_Error`

15. **group.py** (646 lines)
    - Current: `Group_GET_Error`, `SearchGroups_Error`
    - Needed: Add `Group_CRUD_Error`, `SearchGroup_NotFound`, `GroupSharing_Error`

16. **instance_config.py** (684 lines)
    - Current: `ToggleSocialUsers_Error`
    - Needed: `InstanceConfig_GET_Error`, `InstanceConfig_CRUD_Error`

17. **instance_config_sso.py** (539 lines)
    - Current: `SSO_AddUserDirectSignonError`
    - Needed: `SSO_GET_Error`, `SSO_CRUD_Error`

18. **jupyter.py** (561 lines)
    - Current: `JupyterAPI_Error`, `JupyterAPI_WorkspaceStarted`
    - Needed: `Jupyter_GET_Error`, `Jupyter_CRUD_Error`

19. **page.py** (370 lines)
    - Current: `Page_GET_Error`, `PageRetrieval_byId_Error`
    - Needed: Add `Page_CRUD_Error`, `SearchPage_NotFound`, `PageSharing_Error`

20. **publish.py** (409 lines)
    - Current: `GET_Publish_Error`, `CRUD_Publish_Error`
    - Needed: Rename to `Publish_GET_Error`, `Publish_CRUD_Error`

21. **role.py** (435 lines)
    - Current: `Role_NotRetrieved`, `Role_CRUD_Error`
    - Needed: Rename `Role_NotRetrieved` to `Role_GET_Error`

22. **user_attributes.py** (301 lines)
    - Current: `UserAttributes_GET_Error`
    - Needed: Add `UserAttributes_CRUD_Error`

### Complex Routes (May need splitting into submodules)

23. **dataset.py** (900 lines) - **PRIORITY**
    - Current: `DatasetNotFoundError`, `Dataset_GetError`, `Dataset_CRUDError`, `QueryRequestError`, `UploadDataError`, `ShareDataset_Error`
    - Needed: Complete restructure similar to `account/` structure:
      - `dataset/__init__.py` - Main exports
      - `dataset/core.py` - GET operations
      - `dataset/crud.py` - Create/Update/Delete operations
      - `dataset/query.py` - Query operations
      - `dataset/upload.py` - Upload operations
      - `dataset/sharing.py` - Sharing operations
      - `dataset/exceptions.py` - All error classes

24. **datacenter.py** (394 lines)
    - Mostly enums and utilities, review if error classes needed

25. **cloud_amplifier.py** (499 lines)
    - Review needed for error class requirements

## Refactoring Pattern

For each route file, follow this pattern:

### 1. Update Imports
```python
from typing import Optional

import httpx

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
```

### 2. Define Standard Error Classes

```python
class {Module}_GET_Error(RouteError):
    """Raised when {module} retrieval operations fail."""

    def __init__(
        self,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or "{Module} retrieval failed",
            entity_id={module}_id,
            response_data=response_data,
            **kwargs,
        )


class {Module}_CRUD_Error(RouteError):
    """Raised when {module} create, update, or delete operations fail."""

    def __init__(
        self,
        operation: str,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"{Module} {operation} operation failed",
            entity_id={module}_id,
            response_data=response_data,
            **kwargs,
        )


class Search{Module}_NotFound(RouteError):
    """Raised when {module} search operations return no results."""

    def __init__(
        self,
        search_criteria: str,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"No {module}s found matching: {search_criteria}",
            response_data=response_data,
            additional_context={"search_criteria": search_criteria},
            **kwargs,
        )


class {Module}Sharing_Error(RouteError):
    """Raised when {module} sharing operations fail."""

    def __init__(
        self,
        operation: str,
        {module}_id: Optional[str] = None,
        message: Optional[str] = None,
        response_data=None,
        **kwargs,
    ):
        super().__init__(
            message=message or f"{Module} sharing {operation} failed",
            entity_id={module}_id,
            response_data=response_data,
            **kwargs,
        )
```

### 3. Update Function Signatures
Add proper type hints to all parameters:

```python
@gd.route_function
async def get_{module}_by_id(
    auth: DomoAuth,
    {module}_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    session: Optional[httpx.AsyncClient] = None,
) -> rgd.ResponseGetData:
```

### 4. Update Error Raises
Replace old error patterns with new ones:

```python
# OLD
if not res.is_success:
    raise OldError(res=res)

# NEW
if not res.is_success:
    raise {Module}_GET_Error({module}_id={module}_id, response_data=res)
```

### 5. Update __all__ Exports
Ensure all error classes are exported:

```python
__all__ = [
    "{Module}_GET_Error",
    "Search{Module}_NotFound",
    "{Module}_CRUD_Error",
    "{Module}Sharing_Error",
    # ... function names
]
```

## Breaking Down Large Files

For files over 500 lines (like dataset.py), follow the account/ pattern:

### Create Directory Structure
```
dataset/
├── __init__.py          # Main exports
├── core.py              # GET operations
├── crud.py              # Create/Update/Delete
├── exceptions.py        # All error classes
├── query.py             # Query operations (if applicable)
├── upload.py            # Upload operations (if applicable)
└── sharing.py           # Sharing operations (if applicable)
```

### Maintain Import Compatibility
In `dataset/__init__.py`:
```python
from .core import *
from .crud import *
from .exceptions import *
from .query import *
from .upload import *
from .sharing import *

__all__ = [
    # List all exported items
]
```

This ensures existing imports like `from routes.dataset import get_dataset_by_id` continue to work.

## Testing Strategy

After refactoring each route:
1. Verify imports work correctly
2. Check that error classes follow the naming convention
3. Ensure type hints are complete
4. Verify backward compatibility (if applicable)

## Priority Order

1. Complete simple routes first (beastmode, codeengine, enterprise_apps, etc.)
2. Refactor medium complexity routes
3. Break down dataset.py into submodules (highest priority for splitting)
4. Review datacenter.py and cloud_amplifier.py for specific needs

## Notes

- The `auth.py` route already uses the new `AuthError` base class correctly
- The `user.py` route appears to already follow the correct patterns
- Keep minimal changes - only update error classes and type hints
- Retain all existing functionality
- Follow the import strategy used in completed routes
