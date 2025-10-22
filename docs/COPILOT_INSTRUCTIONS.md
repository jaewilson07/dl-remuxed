# Domo Library Project Conventions & Type Hints Instructions

## Project Overview

This is `domolibrary2`, a Python library for interacting with Domo APIs. The project uses:

-   **Async/await patterns** throughout
-   **nbdev-style architecture** with `@patch_to` decorators
-   **Dataclasses** for data models
-   **httpx** for HTTP requests
-   **Modern Python packaging** with hatchling and src/ layout

## Code Structure & Conventions

### 1. Directory Structure

```
src/
├── classes/          # Main Domo entity classes (DomoUser, DomoDataset, etc.)
├── client/           # Core client classes (DomoAuth, DomoError, etc.)
├── routes/           # API route handlers grouped by domain
├── utils/            # Utility functions and helpers
└── integrations/     # Higher-level integration patterns
```

### 2. Import Conventions

-   Use **relative imports** within the package: `from ..client import DomoAuth as dmda`
-   **Aliased imports** for commonly used modules:
    -   `DomoAuth as dmda`
    -   `DomoError as dmde`
    -   `Logger as lc`
    -   `DictDot as util_dd`
-   Group imports: stdlib → third-party → local

### 3. Class & Method Patterns

#### **Main Entity Classes** (in `classes/`)

-   Use `@dataclass` with `field(repr=False)` for auth objects
-   Include `auth: dmda.DomoAuth = field(repr=False)` as first field
-   Implement `__post_init__()` for ID string conversion: `self.id = str(self.id)`
-   Implement `__eq__()` for object comparison by ID

#### **nbdev @patch_to Pattern**

All methods are added to classes using `@patch_to` decorators:

```python
@patch_to(DomoUser)
async def method_name(self: DomoUser, ...):
    pass

@patch_to(DomoUser, cls_method=True)
async def class_method_name(cls: DomoUser, ...):
    pass
```

#### **Async Methods**

-   All API-calling methods are `async`
-   Standard parameters for async methods:
    -   `debug_api: bool = False`
    -   `debug_num_stacks_to_drop: int = 2`
    -   `session: httpx.AsyncClient = None`
    -   `return_raw: bool = False`

### 4. Type Hint Standards

#### **Required Type Hints**

-   **All function parameters** must have type hints
-   **All function return types** must be annotated
-   **Use modern typing** (Python 3.9+ style)

#### **Common Type Patterns**

```python
from typing import Any, List, Optional, Union, Dict
import datetime as dt
import httpx

# Standard async method signature
async def method_name(
    self: DomoUser,
    param1: str,
    param2: Optional[int] = None,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
) -> Union[DomoUser, ResponseGetData, None]:
    pass

# Class methods
@classmethod
async def class_method(
    cls: "DomoUser",  # Use quotes for forward references
    auth: dmda.DomoAuth,
    user_id: str,
    return_raw: bool = False,
) -> Optional["DomoUser"]:
    pass

# List returns
async def get_users(self) -> List[DomoUser]:
    pass

# Complex unions for different return types
async def search_user(
    self,
    email: str,
    return_raw: bool = False,
) -> Union[DomoUser, ResponseGetData, None]:
    pass
```

#### **Dataclass Type Hints**

```python
@dataclass
class DomoUser:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    display_name: Optional[str] = None
    email_address: Optional[str] = None
    created_dt: Optional[dt.datetime] = None
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
    role: Optional[Any] = None  # Use Any for circular imports
```

#### **Route Functions**

```python
async def api_route_function(
    auth: dmda.DomoAuth,
    entity_id: str,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    parent_class: Optional[str] = None,
    debug_num_stacks_to_drop: int = 2,
) -> rgd.ResponseGetData:
    pass
```

### 5. Error Handling Patterns

#### **Custom Exception Classes**

```python
class CustomError(dmde.DomoError):
    def __init__(self, domo_instance: str, additional_param: str):
        super().__init__(
            domo_instance=domo_instance,
            message=f"error message with {additional_param}",
        )
```

#### **Route Error Classes**

```python
class RouteError(de.RouteError):
    def __init__(
        self,
        res: rgd.ResponseGetData,
        entity_id: Optional[str] = None,
    ):
        super().__init__(
            status=res.status,
            message=res.response,
            url=res.url,
            entity_id=entity_id,
        )
```

### 6. Specific Type Requirements

#### **Common Parameter Types**

-   `domo_instance: str`
-   `email_address: str` (validate with `test_valid_email()`)
-   `session: Optional[httpx.AsyncClient] = None`
-   `debug_api: bool = False`
-   `return_raw: bool = False`
-   `debug_num_stacks_to_drop: int = 2`

#### **Return Type Patterns**

-   Single entity: `Optional[DomoUser]` or `DomoUser`
-   Multiple entities: `List[DomoUser]`
-   Raw API response: `ResponseGetData`
-   Flexible returns: `Union[DomoUser, ResponseGetData, None]`
-   Boolean success: `bool`

#### **Complex Types**

-   Use `Any` for circular import situations
-   Use `Union[str, List[str]]` for flexible string/list parameters
-   Use `Dict[str, Any]` for JSON-like data
-   Use `Optional[T]` instead of `Union[T, None]`

### 7. Documentation & Comments

#### **Docstrings**

```python
async def method_name(self, param: str) -> DomoUser:
    """Brief description of what the method does.
    More detailed explanation if needed.
    """
```

#### ****all** Declarations**

Every module should start with `__all__` listing public exports:

```python
__all__ = [
    "MainClass",
    "HelperFunction",
    "CustomError",
]
```

### 8. Async/Await Patterns

#### **Session Management**

```python
# Don't create sessions in methods, pass them in
async def method(
    self,
    session: Optional[httpx.AsyncClient] = None,
) -> ResponseGetData:
    # Use passed session or let route function handle it
    return await some_route(session=session, ...)
```

#### **Error Handling in Async**

```python
try:
    result = await async_operation()
except SomeError as e:
    if suppress_error:
        return None
    raise e from e
```

## Implementation Instructions

### For Type Hint Addition:

1. **Analyze existing patterns** in each file before adding type hints
2. **Preserve all existing functionality** - only add type annotations
3. **Follow the established import patterns** for typing modules
4. **Use the standard parameter patterns** shown above
5. **Maintain consistency** with existing method signatures
6. **Add missing imports** for typing when needed
7. **Use forward references** with quotes for circular dependencies
8. **Test that imports still work** after changes

### Priority Order:

1. Core classes in `classes/` directory
2. Client classes in `client/` directory
3. Route functions in `routes/` directory
4. Utility functions in `utils/` directory
5. Integration functions in `integrations/` directory

### Quality Checks:

-   All functions have parameter type hints (except `self`/`cls`)
-   All functions have return type annotations
-   Imports include necessary typing modules
-   No breaking changes to existing functionality
-   Consistent with project patterns
