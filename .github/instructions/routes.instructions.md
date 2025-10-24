---
applyTo: '/src/domolibrary2/routes/*'
---
# Route Function Standards

## Standard Route Function Pattern

```python
from typing import Optional
import httpx
from ..client.auth import DomoAuth
from ..client.exceptions import RouteError
from ..client import get_data as gd
from ..client import response as rgd

@gd.route_function  # REQUIRED on ALL route functions
async def function_name(
    auth: DomoAuth,  # Always first
    entity_id: str,  # Entity parameters next
    # ... operation-specific params
    session: Optional[httpx.AsyncClient] = None,
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
- [ ] `return_raw: bool = False` parameter on ALL route functions
- [ ] Immediate `if return_raw: return res` check after `gd.get_data()`
- [ ] Standard parameter order (auth first, control params last)
- [ ] Complete type hints on all parameters and return types
- [ ] RouteError-based exception classes with entity_id and res
- [ ] Comprehensive docstrings with Args/Returns/Raises
- [ ] Standard imports pattern
