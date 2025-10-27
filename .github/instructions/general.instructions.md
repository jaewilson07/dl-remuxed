---
applyTo: '**/*'
---
# Domolibrary2 General Instructions

## Project Overview

Domolibrary2 is a Python library for interacting with Domo APIs. The project uses:
- **Async/await patterns** throughout
- **Dataclasses** for data models
- **httpx** for HTTP requests
- **Modern Python packaging** with hatchling and src/ layout
- **Type hints** on all functions and methods

## Directory Structure

```
src/domolibrary2/
├── classes/          # Domo entity classes (DomoUser, DomoDataset, etc.)
├── routes/           # API route handlers grouped by domain
├── client/           # Core client classes (DomoAuth, entities, exceptions)
├── utils/            # Utility functions and helpers
└── integrations/     # Higher-level integration patterns

tests/
├── classes/          # Class tests (test_50_*.py)
├── routes/           # Route tests
└── client/           # Client tests
```

## Key Design Principles

1. **Separation of Concerns**:
   - **Routes**: Handle API calls and HTTP logic
   - **Classes**: Provide user-friendly interface, delegate to routes
   - **Client**: Core authentication and error handling

2. **Composition Over Inheritance**:
   - Use subentities (DomoTags, DomoLineage, etc.) for related functionality
   - Avoid deep inheritance hierarchies

3. **Type Safety**:
   - All parameters must have type hints
   - Use Optional[] for nullable values
   - Return types explicitly declared

4. **Async First**:
   - All API-calling functions are async
   - Use `asyncio` patterns
   - Support session reuse with httpx.AsyncClient

5. **Error Design**:
   - Route-specific exceptions (User_GET_Error, Dataset_CRUD_Error)
   - Exceptions in `routes/[domain]/exceptions.py`
   - Inherit from DomoError base class

## Import Conventions

### Standard Aliases:
```python
import domolibrary2.client.auth as dmda
import domolibrary2.client.entities as dmde
import domolibrary2.client.exceptions as dmex
import domolibrary2.utils.DictDot as util_dd
```

### Import Order:
1. Standard library imports
2. Third-party imports (httpx, pandas, etc.)
3. Local imports (relative imports within package)

### Relative Import Pattern:
```python
# From routes to client
from ..client.auth import DomoAuth
from ..client import get_data as gd

# From classes to routes
from ...routes import user as user_routes
from ...routes.user.exceptions import User_GET_Error

# From classes to subentities
from ..subentity import DomoTag as dmtg
```

## Code Style

### Formatting:
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- Run via pre-commit hooks or `scripts/format-code.ps1`

### Naming:
- **Classes**: PascalCase (DomoUser, DomoDataset)
- **Functions/Methods**: snake_case (get_by_id, create_user)
- **Constants**: UPPER_SNAKE_CASE (TEST_USER_ID_1)
- **Private**: Prefix with underscore (_internal_method)

### Docstrings:
```python
def function_name(param1: str, param2: int = 10) -> ReturnType:
    """Brief description of function.

    Longer description if needed. Explain what the function does,
    not how it does it.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)

    Returns:
        Description of return value

    Raises:
        ExceptionName: When this error occurs
    """
```

## Testing Standards

### Test File Naming:
- Class tests: `tests/classes/test_50_ClassName.py`
- Route tests: `tests/routes/test_route_name.py`
- Client tests: `tests/client/test_component.py`

### Test Structure:
```python
import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda

load_dotenv()

token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

async def test_cell_1(token_auth=token_auth):
    """Test description."""
    # Test implementation
    result = await some_async_function()
    assert result is not None
    return result
```

### Test Requirements:
- All tests must be async
- Use environment variables from .env
- Clean up resources when needed
- Test both success and error cases

## Environment Variables

Store in `.env` file (not committed):
```bash
DOMO_INSTANCE="your-instance"
DOMO_ACCESS_TOKEN="your-developer-token"
USER_ID_1="test-user-id"
DATASET_ID_1="test-dataset-id"
# Add more as needed
```

Update `.env_sample` with new variables (without actual values).

## Pre-commit Hooks

Run before every commit:
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Bypass if needed (not recommended):
```powershell
git commit --no-verify
```

## Common Patterns

### Async Context Manager:
```python
async with httpx.AsyncClient() as session:
    result = await some_function(session=session)
```

### Optional Session Parameter:
```python
async def function_name(
    auth: DomoAuth,
    session: Optional[httpx.AsyncClient] = None,
):
    # Function handles both with and without session
    res = await route_function(auth=auth, session=session)
```

### Return Raw Pattern:
```python
async def get_something(
    auth: DomoAuth,
    return_raw: bool = False,
):
    res = await route_function(auth=auth)

    if return_raw:
        return res  # Return ResponseGetData object

    return SomeClass.from_dict(auth=auth, obj=res.response)
```

## Error Handling

### Try-Except Pattern:
```python
try:
    result = await some_function()
except SpecificError as e:
    # Handle specific error
    logger.error(f"Error occurred: {e}")
    raise
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    raise
```

### Custom Exceptions:
```python
class CustomError(DomoError):
    def __init__(self, entity_id: str, domo_instance: str):
        super().__init__(
            domo_instance=domo_instance,
            message=f"Custom error for entity {entity_id}",
        )
```

## Documentation

### Project Documentation:
- [Class Validation System](../../docs/CLASS-VALIDATION-START-HERE.md)
- [Testing Guide](../../docs/testing-guide.md)
- [Type Hints Guide](../../docs/type-hints-implementation-guide.md)
- [Error Design Strategy](../../docs/error-design-strategy.md)

### API Documentation:
Generated from docstrings using Sphinx or similar tool.

## Development Workflow

1. **Create Branch**: `git checkout -b feature/feature-name`
2. **Make Changes**: Edit files, add tests
3. **Format Code**: `.\scripts\format-code.ps1`
4. **Run Tests**: `pytest tests/`
5. **Commit**: `git commit -m "Description"`
6. **Push**: `git push origin feature/feature-name`
7. **Create PR**: Via GitHub interface

## Reference Implementations

- **Class**: `src/domolibrary2/classes/DomoUser.py`
- **Route**: `src/domolibrary2/routes/user/`
- **Test**: `tests/classes/DomoUser.py`
- **Manager**: `src/domolibrary2/classes/DomoUser.py` (DomoUsers class)

## Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: See test files for usage examples
- **Issues**: Create GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
