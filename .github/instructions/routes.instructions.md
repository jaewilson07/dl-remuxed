---
applyTo: '/src/domolibrary2/routes/*'
---
# Route Function Standards

## Route Module Organization

Routes are organized into two patterns:

### 1. Single-File Modules (Simple Routes)
For routes with limited functionality (< 300 lines):
```
routes/
├── access_token.py      # Access token operations
├── activity_log.py      # Activity logging
├── ai.py                # AI/ML operations
├── application.py       # Application management
├── auth.py              # Authentication
├── beastmode.py         # Beast mode operations
├── card.py              # Card operations
├── dataflow.py          # Dataflow operations
├── grant.py             # Grant management
├── group.py             # Group operations
├── pdp.py               # PDP policies
├── role.py              # Role management
├── stream.py            # Stream operations
└── workflows.py         # Workflow operations
```

### 2. Folder Modules (Complex Routes)
For routes with extensive functionality requiring better organization:
```
routes/
├── account/             # Account operations
│   ├── __init__.py      # Re-exports
│   ├── config.py        # Configuration
│   ├── core.py          # Core CRUD operations
│   ├── crud.py          # Additional CRUD
│   ├── exceptions.py    # Account-specific errors
│   ├── oauth.py         # OAuth operations
│   └── sharing.py       # Sharing operations
│
├── dataset/             # Dataset operations (example below)
│   ├── __init__.py      # Re-exports all functions
│   ├── exceptions.py    # Dataset-specific errors
│   ├── core.py          # Get, create, delete
│   ├── query.py         # Query operations
│   ├── schema.py        # Schema management
│   ├── sharing.py       # Permissions & sharing
│   └── upload.py        # Data upload workflow
│
├── page/                # Page operations
│   ├── __init__.py      # Re-exports
│   ├── access.py        # Access control
│   ├── core.py          # Core operations
│   ├── crud.py          # CRUD operations
│   └── exceptions.py    # Page-specific errors
│
└── user/                # User operations
    ├── __init__.py      # Re-exports (includes user_attributes)
    ├── core.py          # Core user operations
    ├── exceptions.py    # User-specific errors
    └── properties.py    # User properties
```

**When to Use Folder Structure:**
- Module exceeds 500 lines
- Multiple logical groupings of functions (CRUD, query, sharing, etc.)
- Many exception classes (>4)
- Separate concerns improve maintainability

**Folder Module Requirements:**
1. **__init__.py**: Must re-export all public functions and classes
2. **exceptions.py**: All error classes in one file
3. **Logical grouping**: Separate files by functionality (core, query, schema, etc.)
4. **Backward compatibility**: All imports work via `__init__.py`

## Standard Route Function Pattern

```python
from typing import Optional
import httpx
from dc_logger.decorators import LogDecoratorConfig, log_call

from ..auth import DomoAuth  # For single-file modules
# from ...auth import DomoAuth  # For folder modules
from ..base.exceptions import RouteError
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

## Import Patterns for Route Modules

### Single-File Route Module
```python
# src/domolibrary2/routes/stream.py
import httpx
from ..auth import DomoAuth
from ..base.exceptions import RouteError
from ..client import get_data as gd, response as rgd
from ..utils.logging import DomoEntityExtractor, DomoEntityResultProcessor

class Stream_GET_Error(RouteError):
    """Stream-specific error."""
    pass

async def get_stream_by_id(auth: DomoAuth, stream_id: str, ...):
    """Get stream by ID."""
    pass
```

### Folder Route Module Structure
```python
# src/domolibrary2/routes/dataset/exceptions.py
from ...base.exceptions import RouteError, DomoError
from ...client import response as rgd

class Dataset_GET_Error(RouteError):
    """Dataset retrieval error."""
    pass

# src/domolibrary2/routes/dataset/core.py
import httpx
from ...auth import DomoAuth
from ...client import get_data as gd, response as rgd
from .exceptions import Dataset_GET_Error

async def get_dataset_by_id(auth: DomoAuth, dataset_id: str, ...):
    """Get dataset by ID."""
    pass

# src/domolibrary2/routes/dataset/__init__.py
"""Dataset route module - re-exports all functionality."""

from .core import get_dataset_by_id, create, delete
from .exceptions import Dataset_GET_Error, Dataset_CRUD_Error
from .query import query_dataset_private, query_dataset_public
from .schema import get_schema, alter_schema
from .sharing import share_dataset, get_permissions
from .upload import upload_dataset_stage_1, upload_dataset_stage_2_file

__all__ = [
    # Exceptions
    "Dataset_GET_Error",
    "Dataset_CRUD_Error",
    # Core
    "get_dataset_by_id",
    "create",
    "delete",
    # Query
    "query_dataset_private",
    "query_dataset_public",
    # Schema
    "get_schema",
    "alter_schema",
    # Sharing
    "share_dataset",
    "get_permissions",
    # Upload
    "upload_dataset_stage_1",
    "upload_dataset_stage_2_file",
]
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

### Exception Organization
- **Single-file modules**: Define exceptions at the top of the file
- **Folder modules**: Create `exceptions.py` file

### Standard Exception Types
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

### Import Pattern for Exceptions
```python
# Single-file module
from ..base.exceptions import RouteError, DomoError

# Folder module
from ...base.exceptions import RouteError, DomoError
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
