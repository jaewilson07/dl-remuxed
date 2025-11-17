# Converter Module Migration (2025-11-06)

## Overview
The converter module has been reorganized to move core functionality out of the `legacy/` folder into the main module structure.

## Changes Made

### Files Moved
- `legacy/converter.py` → `core.py`
- `legacy/models.py` → `models.py`
- `legacy/utils.py` → `utils.py`

### Updated Imports

#### Before:
```python
from postman.converter.legacy.converter import PostmanRequestConverter
from postman.converter.legacy.models import PostmanCollection
```

#### After:
```python
from postman.converter import PostmanRequestConverter, PostmanCollection
# or
from postman.converter.core import PostmanRequestConverter
from postman.converter.models import PostmanCollection
```

### Backward Compatibility
The `legacy/` folder now contains only `__init__.py` which re-exports from the new locations with a deprecation warning. Old imports will continue to work but will emit:

```
DeprecationWarning: Importing from postman.converter.legacy is deprecated.
Use 'from postman.converter import ...' instead.
```

## New Features Added

### Collection Auth Parsing
The converter now properly reads and uses authentication configuration from Postman collections:

- **API Key auth**: Correctly generates `X-DOMO-Developer-Token` header
- **Bearer auth**: Generates `Authorization: Bearer {token}` header
- Dynamic auth detection based on collection configuration

### Enhanced Test Code Generation
Generated files now include:

```python
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Setup auth from environment variables
    domo_instance = os.getenv("DOMO_INSTANCE")
    domo_token = os.getenv("DOMO_ACCESS_TOKEN")

    auth = {
        "base_url": f"https://{domo_instance}.domo.com/",
        "headers": {
            "X-DOMO-Developer-Token": f"{domo_token}",  # Parsed from collection!
            "Content-Type": "application/json"
        }
    }

    try:
        response = test_function(auth=auth, debug_api=True)
        print(f"Success! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
```

### Export to EXPORTS Folder
Test script now saves generated files to `EXPORTS/` folder for easy access and testing.

## Structure

```
converter/
├── __init__.py                 # Main exports
├── core.py                     # PostmanRequestConverter, PostmanCollectionConverter
├── models.py                   # PostmanCollection, PostmanRequest, etc.
├── utils.py                    # Helper functions
├── agent_*.py                  # Multi-agent framework
├── legacy/
│   └── __init__.py            # Backward compatibility (deprecated)
└── tests/
    ├── test_simple_conversion.py
    └── test_models.py
```

## Migration Guide

### For Users
No changes needed immediately. Old imports will work with a deprecation warning.

### For Developers
Update imports to use the new paths:

```python
# ✅ Recommended
from postman.converter import (
    PostmanCollection,
    PostmanRequestConverter,
    PostmanCollectionConverter,
)

# ⚠️ Deprecated (but still works)
from postman.converter.legacy import PostmanCollection
```

## Testing

All tests pass with the new structure:
- ✅ Import tests (new and legacy paths)
- ✅ Conversion tests
- ✅ Generated code execution tests
- ✅ Auth header detection tests

## Benefits

1. **Cleaner structure**: Core files at module level, not buried in `legacy/`
2. **Better discoverability**: Easier to find and import converter classes
3. **Proper auth handling**: Collection auth configuration is now respected
4. **Standalone test files**: Generated code can be run directly
5. **Maintained compatibility**: Existing code continues to work

## Next Steps

1. Update any internal tools to use new import paths
2. Consider deprecating `legacy/` folder entirely in future release
3. Add more collection auth types (OAuth, etc.) as needed
