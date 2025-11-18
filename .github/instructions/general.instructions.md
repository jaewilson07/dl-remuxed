---
applyTo: '**/*'
name: general_instructions
description: Project-wide conventions, imports, testing, and workflow guidance for domolibrary2.
---

> Last updated: 2025-11-17

# Domolibrary2 General Instructions
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
├── auth/              # Authentication classes (DomoAuth, DomoFullAuth, etc.)
│   ├── __init__.py    # Re-exports all auth classes
│   ├── base.py        # DomoAuth base class
│   ├── full.py        # Username/password auth
│   ├── token.py       # Access token auth
│   ├── developer.py   # OAuth2 client credentials
│   ├── jupyter.py     # Jupyter-specific auth
│   └── utils.py       # Auth utilities
├── base/              # Base classes and exceptions
│   ├── base.py        # DomoEnumMixin and base utilities
│   ├── entities.py    # DomoEntity, DomoManager base classes
│   ├── exceptions.py  # DomoError, RouteError, ClassError, AuthError
│   └── relationships.py # Relationship utilities
├── classes/           # Domo entity classes (DomoUser, DomoDataset, etc.)
├── routes/            # API route handlers grouped by domain
│   ├── Single-file modules (simple routes)
│   └── Folder modules (complex routes with submodules)
├── client/            # HTTP client utilities
│   ├── get_data.py    # Core HTTP request handler
│   └── response.py    # Response classes
├── utils/             # Utility functions and helpers
└── integrations/      # Higher-level integration patterns

tests/
├── classes/           # Class tests (test_50_*.py)
├── routes/            # Route tests
└── client/            # Client tests
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
   - Exceptions in `routes/[domain]/exceptions.py` (folder modules) or at top of file (single-file modules)
   - All exceptions inherit from base classes in `base/exceptions.py`:
     - **DomoError**: Base for all Domo-related errors
     - **RouteError**: API route/endpoint errors
     - **ClassError**: Class instance errors
     - **AuthError**: Authentication-specific errors

6. **Authentication Architecture**:
   - All auth classes in `auth/` module
   - **DomoAuth**: Base authentication class (abstract)
   - **DomoFullAuth**: Username/password authentication
   - **DomoTokenAuth**: Access token authentication
   - **DomoDeveloperAuth**: OAuth2 client credentials
   - **DomoJupyterAuth**: Jupyter-specific authentication variants

## Import Conventions

### Standard Aliases:
```python
import domolibrary2.auth as dmda
import domolibrary2.base.entities as dmde
import domolibrary2.base.exceptions as dmex
import domolibrary2.utils.DictDot as util_dd
```

### Import Order:
1. Standard library imports
2. Third-party imports (httpx, pandas, etc.)
3. Local imports (relative imports within package)

### Relative Import Pattern:
```python
# From routes to auth
from ..auth import DomoAuth  # Single-file module
from ...auth import DomoAuth  # Folder module

# From routes to client
from ..client import get_data as gd
from ..client import response as rgd

# From routes to base exceptions
from ..base.exceptions import RouteError  # Single-file module
from ...base.exceptions import RouteError  # Folder module

# From classes to routes
from ...routes import user as user_routes
from ...routes.dataset import get_dataset_by_id  # Folder module
from ...routes.user.exceptions import User_GET_Error

# From classes to subentities
from ..subentity import DomoTags as dmtg  # Note: class name is plural
```

### User attributes imports (high-level)
User attributes are implemented in `routes/instance_config/user_attributes.py` and re-exported via `routes/user/__init__.py`.

- **Preferred**: import via `routes.user` re-exports.
- **Details**: see `.github/instructions/classes.instructions.md` for the full class-level import pattern.

## Code Style

### Formatting:
- **Ruff-format** for code formatting (Black-compatible, line length: 88)
- **isort** for import sorting
- **Ruff** for linting with auto-fix
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

### Entity URLs
- In classes, `display_url` MUST be a `@property` that returns the entity's Domo web URL. See `.github/instructions/classes.instructions.md` for the full entity pattern.

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
- **ruff**: Linting with auto-fix
- **ruff-format**: Code formatting (Black-compatible)
- **isort**: Import sorting
- **bandit**: Security scanning
- **trailing-whitespace**, **end-of-file-fixer**: File cleanup
- **check-yaml**, **check-toml**: Configuration validation

Note: mypy type checking is available via `scripts/lint.ps1` but not in pre-commit hooks.

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
    session: httpx.AsyncClient | None = None,
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

### What belongs in `docs/`

The top-level `docs/` folder is for **user-facing documentation** only:

- How to install and use domolibrary2
- How to configure auth and environment variables
- How to interpret logs and control log levels (for example
    `docs/log-level-quick-ref.md`)
- How to use specific features and behaviors in notebooks and scripts
- Stable conceptual guides (for example circular import explanations)

These docs are expected to be maintained over time as part of the
public-facing surface area of the library.

### What does *not* belong in `docs/`

Docs that are primarily for **code development, feature implementation,
or internal refactors** should live outside `docs/` (for example under
`local_work/` or a dedicated `dev_docs/` folder) and are generally
expected to be:

- Temporary design notes
- Migration checklists (for example, adopting a new logger implementation)
- One-off PR planning docs

Those documents should be merged into PR descriptions or inline comments
as appropriate and then deleted once the feature is complete. They should
not be treated as long-lived project documentation.

### Finding user-facing docs

See the `docs/` directory for additional reference material. Key documents include:
- `docs/version-management.md` (release/versioning strategy)
- Logging and circular import guides in `docs/` for advanced topics

API documentation is generated from docstrings using Sphinx or a similar tool.

## Development Workflow

1. **Create Branch**: `git checkout -b feature/feature-name`
2. **Make Changes**: Edit files, add tests
3. **Format Code**: `.\scripts\format-code.ps1`
4. **Run Tests**: `pytest tests/`
5. **Commit**: `git commit -m "Description"`
6. **Push**: `git push origin feature/feature-name`
7. **Create PR**: Via GitHub interface

## Reference Implementations

- **Class patterns**: See `.github/instructions/classes.instructions.md` (reference: `src/domolibrary2/classes/DomoUser.py`).
- **Route patterns**: See `.github/instructions/routes.instructions.md`.
- **Test patterns**: See `.github/instructions/tests.instructions.md`.

## Getting Help

- **Documentation**: Check `docs/` directory
- **Examples**: See test files for usage examples
- **Issues**: Create GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
