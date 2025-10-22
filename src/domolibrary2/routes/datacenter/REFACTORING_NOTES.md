# Datacenter Module Refactoring

## Overview
The datacenter module has been refactored from a single file into a package structure following the established pattern used by the account module.

## Changes Made

### Structure
```
Before:
routes/datacenter.py (461 lines)

After:
routes/datacenter/
  ├── __init__.py      (exports all public APIs)
  ├── exceptions.py    (error classes)
  └── core.py          (enums, utilities, and route functions)
```

### Files Created

#### 1. `exceptions.py`
Contains all exception classes following the error design strategy:
- `SearchDatacenter_NoResultsFound` - Raised when datacenter search returns no results
- `Datacenter_GET_Error` - Renamed from `SearchDatacenter_GET_Error` for consistency
- `ShareResource_Error` - Now extends `RouteError` instead of `DomoError`

#### 2. `core.py`
Contains all functionality:
- **Enums**: Datacenter_Enum, Dataflow_Type_Filter_Enum, etc.
- **Utility functions**: generate_search_datacenter_filter, etc.
- **Route functions**: search_datacenter, get_connectors, get_lineage_upstream, share_resource
- **TypedDict**: LineageNode

#### 3. `__init__.py`
Exports all public APIs maintaining backward compatibility.

## Improvements

### Error Class Standardization
1. **ShareResource_Error** now extends `RouteError` instead of `DomoError`
2. All error classes follow the standard RouteError pattern with proper `res` parameter handling
3. Consistent error messages and entity_id handling

### Code Quality
1. Removed duplicate definition of `generate_search_datacenter_filter` (was defined twice)
2. Added proper type hints for all functions
3. Added comprehensive docstrings
4. Added `return_raw` parameter to all route functions following the standard pattern

### Documentation
1. Each module has clear docstring explaining its purpose
2. All functions have comprehensive docstrings with Args/Returns/Raises sections
3. Examples included where appropriate

## Backward Compatibility

All existing imports continue to work:
```python
# These all work as before
from domolibrary2.routes import datacenter
from domolibrary2.routes.datacenter import Datacenter_Enum
from domolibrary2.routes.datacenter import search_datacenter
from domolibrary2.routes.datacenter import generate_search_datacenter_filter
```

## Testing

The refactoring maintains the same public API, so existing code using the datacenter module should continue to work without changes.

## Next Steps

Following the completion of this refactoring, the datacenter module:
- ✅ Has standardized error classes following RouteError patterns
- ✅ Has proper separation of concerns (exceptions vs core functionality)
- ✅ Follows the established pattern from account module
- ✅ Maintains backward compatibility
- ✅ Has comprehensive type hints and documentation
