---
applyTo: '/src/domolibrary2/routes/*'
---
# Route Function Standards

## Standard Route Function Pattern

```python
from typing import Optional
import httpx
from dc_logger.decorators import LogDecoratorConfig, log_call

from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd
from ..utils.logging import ResponseGetDataProcessor

@gd.route_function  # REQUIRED on ALL route functions
@log_call(  # REQUIRED on ALL route functions that perform CRUD operations
    level_name="route",
    config=LogDecoratorConfig(result_processor=ResponseGetDataProcessor()),
)
async def function_name(
    auth: DomoAuth,  # Always first
    entity_id: str,  # Entity parameters next
    # ... operation-specific params
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,  # REQUIRED on all route functions
) -> rgd.ResponseGetData:
    """Function description.

    Args:
        auth: Authentication object
        entity_id: Entity identifier
        return_raw: Return raw response without processing

    Returns:
        ResponseGetData object

    Raises:
        ModuleName_GET_Error: If retrieval fails
    """
    res = await gd.get_data(...)

    # IMMEDIATE return_raw check after get_data
    if return_raw:
        return res

    # Error handling only if not return_raw
    if not res.is_success:
        raise ModuleName_GET_Error(entity_id=entity_id, res=res)

    return res
```

## Logging Decorator Requirements

**When to use `@log_call` decorator:**
- ✅ **REQUIRED** for all CRUD operations (Create, Update, Delete)
- ✅ **REQUIRED** for all sharing/permissions operations
- ✅ **RECOMMENDED** for GET operations (especially by ID)
- ✅ **RECOMMENDED** for search operations
- ⚠️ **OPTIONAL** for utility/helper functions

**Benefits:**
- Automatic request/response logging with sanitized headers
- Execution timing for performance monitoring
- Full error context for debugging
- Audit trail for compliance

**What gets logged:**
- Function name and parameters
- HTTP method, URL, headers (sanitized)
- Request body/payload (sanitized)
- Response status code and body
- Execution duration
- Error details with stack traces

## Standard Exception Classes

```python
# GET errors - retrieval failures
class ModuleName_GET_Error(RouteError):
    def __init__(self, entity_id: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message="ModuleName retrieval failed",
            entity_id=entity_id, res=res, **kwargs
        )

# CRUD errors - create/update/delete failures
class ModuleName_CRUD_Error(RouteError):
    def __init__(self, operation: str, entity_id: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message=f"ModuleName {operation} operation failed",
            entity_id=entity_id, res=res, **kwargs
        )

# Search not found - empty search results
class SearchModuleName_NotFound(RouteError):
    def __init__(self, search_criteria: str, res=None, **kwargs):
        super().__init__(
            message=f"No items found matching: {search_criteria}",
            res=res, additional_context={"search_criteria": search_criteria}, **kwargs
        )
```

## Required Standards Checklist

- [ ] `@gd.route_function` decorator on ALL route functions
- [ ] `@log_call` decorator on CRUD operations (create, update, delete, share)
- [ ] `return_raw: bool = False` parameter on ALL route functions
- [ ] Immediate `if return_raw: return res` check after `gd.get_data()`
- [ ] Standard parameter order (auth first, control params last)
- [ ] Complete type hints on all parameters and return types
- [ ] RouteError-based exception classes with entity_id and res
- [ ] Comprehensive docstrings with Args/Returns/Raises
- [ ] Standard imports pattern (including dc_logger imports for logged functions)
