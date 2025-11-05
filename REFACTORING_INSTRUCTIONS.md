# Python Refactoring Instructions for Domolibrary2

## Overview

This document provides detailed instructions for refactoring large Python files in the domolibrary2 project. The goal is to improve code organization, maintainability, and follow established patterns while maintaining 100% backward compatibility.

## Completed Refactorings

### ✅ client/auth.py (COMPLETED)
- **Before**: 922 lines, 12 classes in single file
- **After**: Split into 7 focused modules (max 256 lines each)
- **Result**: 100% backward compatible, all 118 import locations still work
- **Pattern**: Original file now re-exports from `client/auth/` submodules

### ✅ tests/routes/test.py (COMPLETED)
- **Issue**: 96% duplicate of `tests/test_routes.py`
- **Action**: Deleted duplicate, saved 875 lines
- **Result**: Single canonical test file remains

## High Priority Refactorings

### 🔴 Priority 1: routes/dataset.py

**Current State:**
- 890 lines
- 26 functions
- 7 exception classes
- Mixed responsibilities: queries, schema, uploads, CRUD, sharing, permissions

**Why Refactor:**
- Largest core file in library
- routes/account/ and routes/user/ already follow package structure
- Multiple distinct responsibilities in one file
- Would establish consistent pattern across ALL route modules

**Target Structure:**

```
src/domolibrary2/routes/dataset/
├── __init__.py          # Public API exports (all functions/classes)
├── query.py             # Query operations (2 functions)
├── schema.py            # Schema management (3 functions)
├── upload.py            # Data upload pipeline (4 functions)
├── crud.py              # Create, delete, list operations (6 functions)
├── sharing.py           # Permissions and sharing (2 functions)
└── exceptions.py        # All exception classes (ALREADY EXISTS - move here)
```

**Function Distribution:**

**query.py:**
```python
- query_dataset_public()
- query_dataset_private()
- QueryRequestError (exception)
```

**schema.py:**
```python
- get_schema()
- alter_schema()
- alter_schema_descriptions()
```

**upload.py:**
```python
- UploadDataError (exception)
- upload_dataset_stage_1()
- upload_dataset_stage_2_file()
- upload_dataset_stage_2_df()
- upload_dataset_stage_3()
- index_dataset()
- index_status()
- generate_list_partitions_body()
- list_partitions()
```

**crud.py:**
```python
- DatasetNotFoundError (exception)
- Dataset_GetError (exception)
- Dataset_CRUDError (exception)
- get_dataset_by_id()
- create()
- generate_create_dataset_body()
- generate_enterprise_toolkit_body()
- generate_remote_domostats_body()
- create_dataset_enterprise_toolkit()
- delete_partition_stage_1()
- delete_partition_stage_2()
- delete()
```

**sharing.py:**
```python
- ShareDataset_Error (exception)
- ShareDataset_AccessLevelEnum (enum)
- generate_share_dataset_payload()
- share_dataset()
- get_permissions()
```

**Migration Steps:**

1. **Create the dataset/ directory structure**
   ```bash
   mkdir src/domolibrary2/routes/dataset
   ```

2. **Create __init__.py with all exports**
   ```python
   """Dataset route functions for Domo API operations."""
   
   __all__ = [
       # Query operations
       "query_dataset_public",
       "query_dataset_private",
       "QueryRequestError",
       
       # Schema operations
       "get_schema",
       "alter_schema",
       "alter_schema_descriptions",
       
       # Upload operations
       "UploadDataError",
       "upload_dataset_stage_1",
       "upload_dataset_stage_2_file",
       "upload_dataset_stage_2_df",
       "upload_dataset_stage_3",
       "index_dataset",
       "index_status",
       "list_partitions",
       
       # CRUD operations
       "DatasetNotFoundError",
       "Dataset_GetError",
       "Dataset_CRUDError",
       "get_dataset_by_id",
       "create",
       "delete",
       
       # Sharing operations
       "ShareDataset_Error",
       "ShareDataset_AccessLevelEnum",
       "share_dataset",
       "get_permissions",
   ]
   
   from .query import query_dataset_public, query_dataset_private, QueryRequestError
   from .schema import get_schema, alter_schema, alter_schema_descriptions
   from .upload import (
       UploadDataError,
       upload_dataset_stage_1,
       upload_dataset_stage_2_file,
       upload_dataset_stage_2_df,
       upload_dataset_stage_3,
       index_dataset,
       index_status,
       list_partitions,
   )
   from .crud import (
       DatasetNotFoundError,
       Dataset_GetError,
       Dataset_CRUDError,
       get_dataset_by_id,
       create,
       delete,
   )
   from .sharing import (
       ShareDataset_Error,
       ShareDataset_AccessLevelEnum,
       share_dataset,
       get_permissions,
   )
   ```

3. **Create each submodule file**
   - Copy functions from original dataset.py
   - Keep all imports needed by those functions
   - Keep all decorators (@gd.route_function, @log_call)
   - Maintain all docstrings

4. **Replace original dataset.py with re-exports**
   ```python
   """Dataset route functions - refactored into package structure.
   
   This file maintains backward compatibility by re-exporting from submodules.
   
   New code can import from submodules:
   - from domolibrary2.routes.dataset.query import query_dataset_public
   - from domolibrary2.routes.dataset.schema import get_schema
   - from domolibrary2.routes.dataset.upload import upload_dataset_stage_1
   - from domolibrary2.routes.dataset.crud import create, delete
   - from domolibrary2.routes.dataset.sharing import share_dataset
   """
   
   __all__ = [...]  # Same as dataset/__init__.py
   
   from .dataset import *  # Re-export everything
   ```

5. **Test thoroughly**
   ```bash
   # Test imports work both ways
   python -c "from domolibrary2.routes.dataset import query_dataset_public"
   python -c "from domolibrary2.routes.dataset.query import query_dataset_public"
   
   # Run relevant tests
   pytest tests/routes/test_dataset*.py -v
   pytest tests/classes/test_*Dataset*.py -v
   ```

6. **Git commit**
   ```bash
   git add src/domolibrary2/routes/dataset/
   git commit -m "refactor: split routes/dataset.py into package structure

   - Split 890-line file into 6 focused modules
   - Organized by responsibility: query, schema, upload, crud, sharing
   - Maintained 100% backward compatibility via re-exports
   - Follows pattern established in routes/account/ and routes/user/
   - No breaking changes to external code"
   ```

**Impact:**
- Largest core file reduced from 890 to ~200 lines per module
- All route modules follow consistent package structure
- Easier to locate specific dataset operations
- Estimated effort: 2-3 hours

---

## Medium Priority Refactorings

### 🟡 Priority 2: utils/logging/processors.py

**Current State:**
- 694 lines
- 6 processor classes
- Mixed entity extractors and result processors

**Why Refactor:**
- Extractors and processors are different concerns
- Multiple entity types mixed together
- Would improve logging subsystem organization

**Target Structure:**

```
src/domolibrary2/utils/logging/
├── __init__.py          # Public API exports
├── extractors.py        # Entity extractors
└── processors.py        # Result processors
```

**Class Distribution:**

**extractors.py:**
```python
- NoOpEntityExtractor
- DomoEntityExtractor
- _extract_dataset_entity()
- _extract_card_entity()
- _extract_user_entity()
- _extract_page_entity()
- _extract_auth_entity()
```

**processors.py:**
```python
- ResponseGetDataProcessor
- DomoEntityResultProcessor
```

**Migration Steps:**

1. Create `extractors.py` with entity extractor classes
2. Create `processors.py` with result processor classes
3. Update `__init__.py` to re-export all classes
4. Replace original `processors.py` with re-exports if needed for compatibility
5. Test imports: `from domolibrary2.utils.logging import DomoEntityExtractor`

**Impact:**
- Clearer separation of logging concerns
- Easier to extend with new entity types or processors
- Estimated effort: 1 hour

---

### 🟡 Priority 3: classes/DomoAccount/config.py

**Current State:**
- 608 lines
- 22 configuration classes
- Each class is small (~20-30 lines) but hard to find

**Why Refactor:**
- Many small classes in one file
- Hard to navigate and find specific config
- Natural grouping by config type

**Target Structure:**

```
src/domolibrary2/classes/DomoAccount/config/
├── __init__.py          # Re-export all config classes
├── settings.py          # General settings (5-6 classes)
├── notifications.py     # Notification configs (4-5 classes)
└── security.py          # Security settings (4-5 classes)
```

**Class Grouping Strategy:**

Analyze the 22 classes and group by:
- Settings: General account configuration
- Notifications: Email, alert, notification configs
- Security: Authentication, access, security configs

**Migration Steps:**

1. Analyze all 22 `DomoAccount_Config_*` classes
2. Group by logical categories (settings/notifications/security)
3. Create submodules with grouped classes
4. Create `__init__.py` that re-exports ALL classes
5. Replace original `config.py` with re-exports
6. Test: `from domolibrary2.classes.DomoAccount.config import DomoAccount_Config_*`

**Impact:**
- Easier to find specific config class
- Better organization by config type
- Estimated effort: 1-2 hours

---

### 🟡 Priority 4: classes/subentity/schedule.py

**Current State:**
- 648 lines
- 6 classes
- Mix of schedule types and configuration

**Why Refactor:**
- Schedule types and configs are different concerns
- Complex schedule logic could be isolated
- Used by multiple classes

**Target Structure:**

```
src/domolibrary2/classes/subentity/schedule/
├── __init__.py          # Public API exports
├── types.py             # Schedule type classes
└── config.py            # Schedule configuration classes
```

**Migration Steps:**

1. Identify schedule type classes vs config classes
2. Split into `types.py` and `config.py`
3. Create `__init__.py` with all exports
4. Update `subentity/__init__.py` to import from schedule package
5. Test schedule functionality in relevant classes

**Impact:**
- Clearer schedule type organization
- Easier to extend with new schedule types
- Estimated effort: 2 hours

---

### 🟡 Priority 5: classes/DomoInstanceConfig/publish.py

**Current State:**
- 615 lines
- 8 classes
- Publishing configuration classes

**Why Refactor:**
- Multiple publish-related entities
- Could be split by entity type if patterns emerge

**Target Structure:**

Analyze the 8 classes first, then determine if splitting makes sense:
```
src/domolibrary2/classes/DomoInstanceConfig/publish/
├── __init__.py          # Public API exports
├── registry.py          # Registry-related classes
└── policies.py          # Policy-related classes
```

**Migration Steps:**

1. Review all 8 classes in publish.py
2. Determine if natural groupings exist
3. Only split if clear benefits (may keep as-is if classes are tightly coupled)
4. Test publish functionality

**Impact:**
- Depends on analysis of class relationships
- May decide to keep as-is if no clear benefits
- Estimated effort: 1-2 hours

---

## Files Already Well-Structured (No Action)

### ✅ classes/DomoUser.py (736 lines)
- **Status**: Reference implementation
- **Reason**: Well-structured with proper subentity usage
- **Action**: Keep as-is, use as pattern example

### ✅ routes/user/core.py (699 lines)
- **Status**: Already part of routes/user/ package
- **Reason**: 11 route functions is manageable, already split from main user routes
- **Action**: None needed

### ✅ postman/converter/models.py (648 lines)
- **Status**: External utility
- **Reason**: Postman conversion models, separate concern from core library
- **Action**: Out of scope for core refactoring

---

## General Refactoring Principles

### 1. Always Maintain Backward Compatibility

**Pattern**: Original file becomes re-export layer
```python
# Original: src/module.py becomes re-export
"""Module description - refactored into package structure.

Backward compatible re-exports for existing code.
"""

__all__ = [...]

from .module import *  # Import from new package
```

### 2. Follow Established Patterns

**Routes Pattern** (see routes/account/, routes/user/):
```
module/
├── __init__.py          # Public API exports
├── core.py              # Main CRUD operations
├── [feature].py         # Specific features
└── exceptions.py        # Module-specific errors
```

**Classes Pattern** (see client/auth/):
```
module/
├── __init__.py          # Public API exports
├── base.py              # Base classes if needed
├── [type].py            # Specific implementations
└── utils.py             # Helper functions
```

### 3. Required Standards

- ✅ Keep all `@gd.route_function` decorators
- ✅ Keep all `@log_call` decorators on CRUD operations
- ✅ Maintain all docstrings
- ✅ Preserve all type hints
- ✅ Keep all imports needed by functions
- ✅ Test both old and new import paths

### 4. Testing Checklist

For each refactoring:

```bash
# 1. Test imports work both ways
python -c "from original.path import function"
python -c "from new.module.path import function"

# 2. Verify class identity (if applicable)
python -c "
from original.path import Class1
from new.path import Class1 as Class2
assert Class1 is Class2
"

# 3. Run relevant test suite
pytest tests/relevant_tests*.py -v

# 4. Run import tests
pytest tests/test_routes.py -v

# 5. Check for import errors across project
python -c "import domolibrary2"
```

### 5. Git Commit Message Template

```
refactor: split [module] into package structure

- Split [X]-line file into [N] focused modules
- Organized by [responsibility/feature/type]
- Maintained 100% backward compatibility via re-exports
- Follows pattern established in [similar module]
- No breaking changes to external code

Modules:
- [module1.py]: [description]
- [module2.py]: [description]
- [module3.py]: [description]
```

---

## Expected Outcomes

### After Priority 1 (dataset refactoring):
- ✅ All route modules follow consistent package structure
- ✅ Largest core file reduced from 890 to ~200 lines per module
- ✅ Easier to locate specific dataset operations
- ✅ Consistent with routes/account/ and routes/user/ patterns

### After Priority 1-2 (dataset + logging):
- ✅ Largest file ~650 lines (excluding tests)
- ✅ 60% reduction from original 922-line auth.py
- ✅ Clearer separation of concerns throughout library
- ✅ Better logging subsystem organization

### After All Priorities:
- ✅ Consistent module structure across entire library
- ✅ No files over 500 lines (excluding tests and external utilities)
- ✅ Clear patterns for future development
- ✅ Improved code navigation and discovery
- ✅ Reduced cognitive load for contributors

---

## Troubleshooting

### Issue: Circular Import Errors

**Solution**: Move shared dependencies to separate module
```python
# Create shared.py or constants.py for shared imports
# Import from shared module in both places
```

### Issue: Import Path Too Long

**Solution**: Re-export at parent level
```python
# In parent __init__.py
from .submodule.deep.path import Class
```

### Issue: Tests Failing After Refactoring

**Checklist**:
1. Verify all functions/classes exported in `__all__`
2. Check that original file re-exports correctly
3. Ensure all decorators preserved
4. Verify imports work both ways
5. Check for missed imports in new modules

### Issue: Type Hints Not Working

**Solution**: Make sure imports include type hint dependencies
```python
from typing import Optional, Union
from ..client.auth import DomoAuth  # For type hints
```

---

## Priority Order Summary

1. **🔴 HIGH**: routes/dataset.py (2-3 hours, HIGH impact)
2. **🟡 MEDIUM**: utils/logging/processors.py (1 hour, MEDIUM impact)
3. **🟡 MEDIUM**: classes/DomoAccount/config.py (1-2 hours, LOW-MEDIUM impact)
4. **🟡 MEDIUM**: classes/subentity/schedule.py (2 hours, MEDIUM impact)
5. **🟡 MEDIUM**: classes/DomoInstanceConfig/publish.py (1-2 hours, MEDIUM impact)

**Recommendation**: Complete one refactoring at a time, test thoroughly, and commit before moving to the next.

---

## Success Criteria

Each refactoring is successful when:

✅ All existing imports continue to work  
✅ All tests pass without modification  
✅ New import paths also work  
✅ Code is better organized and easier to navigate  
✅ File sizes reduced to manageable levels (<300 lines ideal)  
✅ Patterns are consistent with similar modules  
✅ No breaking changes introduced  
✅ Documentation updated if needed  

---

## Reference Files

**Good Examples to Follow**:
- `src/domolibrary2/client/auth/` - Class refactoring pattern
- `src/domolibrary2/routes/account/` - Route refactoring pattern
- `src/domolibrary2/routes/user/` - Route refactoring pattern
- `src/domolibrary2/classes/DomoUser.py` - Well-structured class

**Completed Refactoring**:
- Original: `src/domolibrary2/client/auth.py` (kept as re-export)
- New: `src/domolibrary2/client/auth/` (7 focused modules)

---

*Last Updated: 2025-01-04*  
*Completed Refactorings: 2 (auth module, duplicate test removal)*  
*Remaining Priorities: 5*
