# Route Splitting Strategy

## Executive Summary

This document provides a standardized methodology for consistently splitting large route files into well-organized, modular structures. Based on successful implementations in `account/`, `appdb/`, `page/`, and `user/` modules, this strategy ensures maintainability, discoverability, and backward compatibility while following established patterns.

## Core Principles

### 1. **Functional Separation of Concerns**
Split routes by logical function rather than arbitrary size limits:
- **Core Operations**: Basic retrieval, search, and fundamental operations
- **CRUD Operations**: Create, update, delete operations  
- **Access & Permissions**: Sharing, access control, and permission management
- **Configuration**: Settings, configuration, and administrative functions
- **Specialized Features**: Domain-specific or advanced functionality

### 2. **Maintain Backward Compatibility**
- All existing imports must continue to work unchanged
- Consolidated `__init__.py` re-exports all functions and classes
- No breaking changes to existing API contracts

### 3. **Standardized Module Structure**
- Consistent naming conventions across all route modules
- Uniform file organization and import patterns
- Standardized documentation and exception handling

## Standard Modular Structure

### Required Files

```
routes/{entity}/
├── __init__.py          # Consolidated exports and main documentation
├── exceptions.py        # All exception classes for the entity
├── core.py             # Basic retrieval and search operations
└── {additional_modules} # Specialized functional modules
```

### Optional Specialized Modules

Based on entity complexity and functionality:

- **`crud.py`** - Create, update, delete operations
- **`access.py`** or **`sharing.py`** - Access control and permissions
- **`config.py`** or **`properties.py`** - Configuration and settings
- **`oauth.py`** - OAuth-specific operations
- **`attributes.py`** - Attribute management
- **`collections.py`**, **`documents.py`**, etc. - Domain-specific modules

## Module Classification Framework

### Core Module (`core.py`)
**Always Required** - Basic entity operations

**Typical Functions:**
```python
# Retrieval operations
async def get_{entities}()           # List all entities
async def get_{entity}_by_id()       # Retrieve by ID
async def search_{entities}()        # Search operations

# Basic queries
async def get_{entity}_summary()     # Summary information
async def get_{entity}_definition()  # Detailed definitions
```

**Example from account/core.py:**
- ✅ `get_accounts()` - List all accounts
- ✅ `get_account_by_id()` - Retrieve specific account
- ✅ `get_available_data_providers()` - Available providers

### Exception Module (`exceptions.py`)
**Always Required** - Centralized error handling

**Standard Exception Classes:**
```python
class {Entity}_GET_Error(RouteError):      # Retrieval failures
class Search{Entity}_NotFound(RouteError): # Search returns no results  
class {Entity}_CRUD_Error(RouteError):     # Create/update/delete failures
class {Entity}Sharing_Error(RouteError):   # Sharing/access failures
class {Entity}_Config_Error(RouteError):   # Configuration failures
```

### CRUD Module (`crud.py`)
**When Needed:** Entity supports create/update/delete operations

**Typical Functions:**
```python
async def create_{entity}()          # Create new entity
async def update_{entity}()          # Update existing entity  
async def delete_{entity}()          # Delete entity
async def generate_create_{entity}_body()  # Helper functions
```

**Example from account/crud.py:**
- ✅ `create_account()`, `create_oauth_account()`
- ✅ `update_account_name()`, `update_oauth_account_name()`  
- ✅ `delete_account()`, `delete_oauth_account()`

### Access/Sharing Module (`access.py` or `sharing.py`)
**When Needed:** Entity supports sharing and permission management

**Typical Functions:**
```python
async def get_{entity}_access_list()     # Retrieve access permissions
async def share_{entity}()               # Share with users/groups
async def unshare_{entity}()             # Remove sharing
async def modify_{entity}_permissions()   # Update permissions
```

**Example from page/access.py:**
- ✅ `get_page_access_test()` - Test access permissions
- ✅ `get_page_access_list()` - Retrieve access list

### Configuration Module (`config.py` or `properties.py`)
**When Needed:** Entity has configuration/property management

**Typical Functions:**
```python
async def get_{entity}_config()      # Retrieve configuration
async def update_{entity}_config()   # Update configuration
async def get_{entity}_properties()  # Property management
async def update_{entity}_layout()   # Layout updates
```

**Example from page/properties.py:**
- ✅ `update_page_layout()` - Layout configuration
- ✅ `put_writelock()`, `delete_writelock()` - Lock management
- ✅ `add_page_owner()` - Ownership management

### Specialized Modules
**When Needed:** Domain-specific functionality

**Examples:**
- **`oauth.py`** (account) - OAuth-specific account operations
- **`attributes.py`** (user) - User attribute management
- **`collections.py`, `documents.py`** (appdb) - AppDb-specific functionality

## Implementation Guidelines

### Step 1: Analyze Current Route File

**Categorize existing functions by purpose:**

1. **Inventory Functions**: List all async functions and their purposes
2. **Group by Functionality**: Categorize into core/crud/access/config/specialized
3. **Identify Dependencies**: Note function interdependencies
4. **Plan Module Structure**: Design optimal module organization

**Example Analysis Template:**
```python
# Current functions in large_route.py:
functions = {
    "core": [
        "get_entities()", "get_entity_by_id()", "search_entities()"
    ],
    "crud": [
        "create_entity()", "update_entity()", "delete_entity()"
    ],
    "access": [
        "get_entity_access_list()", "share_entity()"
    ],
    "config": [
        "get_entity_config()", "update_entity_config()"
    ]
}
```

### Step 2: Create Module Structure

**Create directory and files:**
```bash
mkdir src/domolibrary2/routes/{entity}
touch src/domolibrary2/routes/{entity}/__init__.py
touch src/domolibrary2/routes/{entity}/exceptions.py
touch src/domolibrary2/routes/{entity}/core.py
# Add specialized modules as needed
```

### Step 3: Implement Standard Templates

#### Exception Module Template (`exceptions.py`)
```python
"""
{Entity} Exception Classes

This module contains all exception classes for {entity} operations.
"""

__all__ = [
    "{Entity}_GET_Error",
    "Search{Entity}_NotFound", 
    "{Entity}_CRUD_Error",
    "{Entity}Sharing_Error",
    "{Entity}_Config_Error",
]

from typing import Optional
from ...client.exceptions import RouteError

class {Entity}_GET_Error(RouteError):
    """Raised when {entity} retrieval operations fail."""
    def __init__(self, {entity}_id: Optional[str] = None, message: Optional[str] = None, res=None, **kwargs):
        super().__init__(
            message=message or "{Entity} retrieval failed",
            entity_id={entity}_id, res=res, **kwargs
        )

# Additional exception classes...
```

#### Core Module Template (`core.py`)
```python
"""
{Entity} Core Functions

This module provides core {entity} retrieval and search functions.
"""

__all__ = [
    "get_{entities}",
    "get_{entity}_by_id",
    "search_{entities}",
]

from typing import Optional, Union
import httpx

from ...client.auth import DomoAuth
from ...client import get_data as gd
from ...client import response as rgd
from .exceptions import {Entity}_GET_Error, Search{Entity}_NotFound

@gd.route_function
async def get_{entity}_by_id(
    auth: DomoAuth,
    {entity}_id: str,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 1,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> rgd.ResponseGetData:
    """Retrieve a specific {entity} by ID."""
    # Implementation...
```

#### Main Module Template (`__init__.py`)
```python
"""
{Entity} Route Functions

This module provides functions for managing Domo {entities}.

The module is organized into functional areas:
- core: Basic {entity} retrieval and search functions
- crud: Create, update, delete operations (if applicable)
- access: Access control and sharing functions (if applicable) 
- config: Configuration and property management (if applicable)
- exceptions: All {entity}-related exception classes

Functions:
    [List all exported functions with brief descriptions]

Exception Classes:
    [List all exported exception classes with brief descriptions]
"""

# Import all exception classes
from .exceptions import (
    {Entity}_GET_Error,
    Search{Entity}_NotFound,
    # Additional exceptions...
)

# Import core functions  
from .core import (
    get_{entities},
    get_{entity}_by_id,
    # Additional core functions...
)

# Import specialized module functions
# from .crud import (...)
# from .access import (...)
# from .config import (...)

__all__ = [
    # Exception classes
    "{Entity}_GET_Error",
    "Search{Entity}_NotFound",
    
    # Core functions
    "get_{entities}",
    "get_{entity}_by_id",
    
    # Specialized functions
    # (list all exported functions)
]
```

### Step 4: Migration Process

1. **Create New Structure**: Set up directory and template files
2. **Move Exception Classes**: Migrate all exception classes to `exceptions.py`
3. **Distribute Functions**: Move functions to appropriate modules
4. **Update Imports**: Adjust relative import paths (e.g., `...client.auth`)
5. **Create Consolidated Exports**: Set up `__init__.py` with all re-exports
6. **Test Compatibility**: Verify all existing imports still work
7. **Backup Original**: Save original file as `{route}.py.backup`
8. **Remove Original**: Delete original monolithic file

### Step 5: Quality Assurance

**Required Validation Steps:**

1. **Import Testing**:
   ```python
   # Test backward compatibility
   from domolibrary2.routes.{entity} import function_name, Exception_Class
   
   # Test modular imports
   from domolibrary2.routes.{entity}.core import function_name
   ```

2. **Function Signature Verification**: Ensure all functions maintain:
   - `@gd.route_function` decorator
   - `return_raw: bool = False` parameter
   - Complete type hints
   - Proper error handling

3. **Documentation Standards**: Verify:
   - Comprehensive module docstrings
   - Complete function docstrings with Args/Returns/Raises
   - Updated `__all__` exports

## Existing Implementations Analysis

### Account Module - Complex Multi-Domain Split

**Structure:**
```
account/
├── __init__.py          # Consolidated exports (103 lines)
├── exceptions.py        # 7 exception classes
├── core.py             # Basic retrieval (3 functions)
├── oauth.py            # OAuth-specific operations (2 functions)  
├── crud.py             # Create/update/delete operations (8 functions)
├── config.py           # Configuration management (4 functions)
└── sharing.py          # Advanced sharing with enums and classes
```

**Key Patterns:**
- ✅ **Functional Separation**: Clear domain boundaries (oauth vs regular accounts)
- ✅ **Comprehensive CRUD**: Full lifecycle management
- ✅ **Advanced Sharing**: Complex permission models with enums
- ✅ **Configuration Management**: Separate config operations

### AppDb Module - Resource-Hierarchy Split

**Structure:**
```
appdb/
├── __init__.py          # Consolidated exports (68 lines)
├── exceptions.py        # 3 core exception classes
├── datastores.py        # Top-level datastore operations
├── collections.py       # Collection management within datastores
└── documents.py         # Document operations within collections
```

**Key Patterns:**
- ✅ **Hierarchical Organization**: Follows AppDb resource hierarchy
- ✅ **Resource-Specific Modules**: Each AppDb resource type has dedicated module
- ✅ **Clean Separation**: Clear boundaries between datastores/collections/documents

### Page Module - Feature-Based Split

**Structure:**
```
page/
├── __init__.py          # Consolidated exports (81 lines)
├── exceptions.py        # 4 exception classes
├── core.py             # Basic page operations (3 functions)
├── access.py           # Access control and permissions (2 functions)
└── properties.py       # Layout, locks, ownership (4 functions)
```

**Key Patterns:**
- ✅ **Feature-Based Organization**: Functions grouped by purpose
- ✅ **Balanced Distribution**: Reasonable function count per module
- ✅ **Clear Responsibilities**: Each module has distinct purpose

### User Module - Attribute-Driven Split

**Structure:**
```
user/
├── __init__.py          # Consolidated exports (101 lines)
├── core.py             # Core user operations
├── attributes.py        # User attribute management
└── properties.py       # User property management
```

**Key Patterns:**
- ✅ **Attribute-Centric**: Special focus on user attribute management
- ✅ **Property Management**: Separate property operations
- ✅ **Core Foundation**: Comprehensive basic user operations

## Decision Matrix for Module Organization

### When to Create Specialized Modules

| Criteria | Create Separate Module | Keep in Core |
|----------|------------------------|---------------|
| **Function Count** | 3+ related functions | 1-2 functions |
| **Domain Complexity** | Complex business logic | Simple operations |
| **Dependencies** | Unique dependencies | Shared dependencies |
| **Access Patterns** | Often used together | Rarely used together |
| **Future Growth** | Likely to expand | Stable functionality |

### Module Size Guidelines

- **`exceptions.py`**: 3-10 exception classes (typically 3-7)
- **`core.py`**: 3-8 basic functions (get, search, list operations)
- **Specialized modules**: 2-6 functions each (focused functionality)
- **`__init__.py`**: 50-150 lines (comprehensive exports and documentation)

### Naming Conventions

**Module Names:**
- `core.py` - Always for basic operations
- `exceptions.py` - Always for exception classes
- `crud.py` - For create/update/delete operations
- `access.py` or `sharing.py` - For permission management
- `config.py` or `properties.py` - For configuration/settings
- Domain-specific names for specialized functionality

**Function Naming:**
- Follow existing patterns: `get_{entity}_by_id`, `create_{entity}`, etc.
- Maintain consistency with similar operations across modules
- Use descriptive names that clearly indicate functionality

## Migration Prioritization Strategy

### Phase 1: High-Impact Routes (Week 1)
**Criteria**: Large files (500+ lines) with high usage

**Candidates:**
- `dataset.py` (900+ lines) - **HIGHEST PRIORITY**
- `user.py` (if not modularized) - Core user management
- `dataflow.py` - Data processing operations
- `card.py` - Dashboard functionality

### Phase 2: Medium Complexity Routes (Week 2) 
**Criteria**: Medium files (300-500 lines) with clear functional boundaries

**Candidates:**
- `application.py` (462 lines)
- `role.py` (435 lines) 
- `group.py` (646 lines)
- `instance_config.py` (684 lines)

### Phase 3: Specialized Routes (Week 3-4)
**Criteria**: Smaller files with specialized functionality

**Candidates:**
- Instance config modules (SSO, MFA, API client, etc.)
- Enterprise apps and specialized features
- Integration modules (Jupyter, AI, etc.)

## Success Metrics

### Code Organization Metrics
- **Reduced File Sizes**: Target <200 lines per module
- **Improved Discoverability**: Clear functional groupings
- **Enhanced Maintainability**: Isolated concerns
- **Better Testing**: Focused unit test coverage

### Developer Experience Metrics  
- **Backward Compatibility**: 100% existing import compatibility
- **Documentation Quality**: Comprehensive module and function docs
- **Import Flexibility**: Support both unified and modular imports
- **Code Navigation**: Faster location of relevant functionality

### Quality Assurance Metrics
- **Zero Breaking Changes**: All existing code continues working
- **Complete Type Coverage**: 100% type hints across all functions
- **Standardized Patterns**: Consistent decorator and parameter usage
- **Error Handling**: Comprehensive exception coverage

## Best Practices Summary

### ✅ Do's
1. **Start with functional analysis** before creating modules
2. **Maintain backward compatibility** at all costs
3. **Use consistent naming conventions** across all modules
4. **Provide comprehensive documentation** for each module
5. **Test both unified and modular imports** thoroughly
6. **Follow the standard template structure** for consistency
7. **Create logical functional boundaries** between modules
8. **Plan for future growth** in module organization

### ❌ Don'ts
1. **Don't split arbitrarily by size** - follow functional boundaries
2. **Don't create single-function modules** unless highly specialized
3. **Don't break existing imports** - always maintain compatibility
4. **Don't mix unrelated functionality** in the same module
5. **Don't skip exception class organization** - centralize all exceptions
6. **Don't ignore interdependencies** - plan import relationships carefully
7. **Don't forget to update `__all__` exports** in all modules
8. **Don't skip backup creation** before removing original files

## Conclusion

This standardized route splitting strategy provides a systematic approach to transforming large, monolithic route files into well-organized, maintainable modular structures. By following these established patterns and guidelines, we can ensure consistency across all route modules while maintaining full backward compatibility and improving the overall developer experience.

The strategy has been successfully validated through implementations in `account/`, `appdb/`, `page/`, and `user/` modules, demonstrating its effectiveness across different types of functionality and complexity levels.