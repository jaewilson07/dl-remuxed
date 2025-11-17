---
name: Class Validation and Testing
about: Template for validating and fixing class implementations to follow domolibrary2 standards
title: 'Validate and Test: [ClassName]'
labels: ['class-validation', 'testing', 'refactor']
assignees: ''
---

> Last updated: 2025-10-30

# Validate and Test: [ClassName]

## 📋 Background

This issue tracks the validation and testing of the `[ClassName]` class to ensure it follows domolibrary2 design patterns and standards.

### Entity Hierarchy
All Domo entities should inherit from the appropriate base class:

```
DomoBase (abstract)
└── DomoEntity (id, auth, raw, display_url, from_dict, get_by_id)
    ├── DomoEntity_w_Lineage (adds Lineage tracking)
    │   ├── DomoFederatedEntity (adds federation support)
    │   │   └── DomoPublishedEntity (adds publish/subscribe)
    │   └── [Other lineage-aware entities]
    └── DomoManager (for entity collections)

DomoSubEntity (for composition - entities that belong to parents)
```

### Key Design Patterns

1. **Dataclass Pattern**: All entities use `@dataclass` decorator
2. **Composition over Inheritance**: Use `DomoSubEntity` for related entities (e.g., `DomoTags`, `DomoLineage`, `DomoCertification`)
3. **Route Function Delegation**: Class methods should call route functions, not implement API logic
4. **Standardized Signatures**:
   - `auth` parameter always comes first
   - Optional parameters properly typed with defaults
   - All methods include docstrings
5. **Exception Handling**: Use route-specific exceptions imported from `routes.[entity].exceptions`

---

## 📍 Class Location

**File**: `src/domolibrary2/classes/[path]/[ClassName].py`
**Route Module**: `src/domolibrary2/routes/[route_name]/`
**Test File**: `tests/classes/test_50_[ClassName].py`

---

## ✅ Tasks

### Phase 1: Structure Validation

- [ ] **Task 1.1**: Verify proper inheritance
  - Check that class inherits from appropriate base (`DomoEntity`, `DomoEntity_w_Lineage`, `DomoManager`, or `DomoSubEntity`)
  - Verify `@dataclass` decorator is present
  - Confirm `__all__` exports are complete

- [ ] **Task 1.2**: Validate required attributes and methods
  - [ ] `id` attribute present with correct type
  - [ ] `auth: DomoAuth` attribute present (with `field(repr=False)`)
  - [ ] `raw: dict` attribute present (with `field(default_factory=dict, repr=False)`)
  - [ ] `display_url()` property/method implemented
  - [ ] `from_dict()` classmethod implemented
  - [ ] `get_by_id()` classmethod implemented (for DomoEntity subclasses)
  - [ ] `__post_init__()` method if initialization logic needed

- [ ] **Task 1.3**: Review method signatures
  - [ ] All methods have `auth` as first parameter (after `cls` or `self`)
  - [ ] Optional parameters properly typed with defaults
  - [ ] Methods delegate to route functions (not implementing API logic)
  - [ ] All public methods have docstrings

### Phase 2: Composition Analysis

- [ ] **Task 2.1**: Identify composition opportunities
  - [ ] Check if entity should have `DomoTags` (most entities support tagging)
  - [ ] Check if entity should have `DomoLineage` (datasets, cards, pages)
  - [ ] Check if entity should have `DomoCertification` (datasets, cards)
  - [ ] Check if entity should have `DomoAccess` (sharing/permissions)
  - [ ] Check if entity should have `DomoMembership` (groups, user groups)
  - [ ] list any entity-specific subentities needed (e.g., `DomoDataset_Schema`, `PDP_Policies`)

- [ ] **Task 2.2**: Implement subentity composition
  - [ ] Add subentity attributes as `field(default=None)`
  - [ ] Initialize subentities in `__post_init__()` using `from_parent()`
  - [ ] Verify subentities inherit from `DomoSubEntity`

### Phase 3: Route Integration

- [ ] **Task 3.1**: Verify route function imports
  - [ ] Route functions imported from correct module (`routes.[entity]`)
  - [ ] Exception classes imported from `routes.[entity].exceptions`
  - [ ] Check for any incorrect imports from `client.*` (should be from `routes.*`)

- [ ] **Task 3.2**: Validate route function usage
  - [ ] Methods call route functions correctly (auth first, then params)
  - [ ] Route function exceptions properly imported and re-raised
  - [ ] No API implementation logic in class methods (should be in routes)

### Phase 4: Manager Class Validation (if applicable)

- [ ] **Task 4.1**: Verify manager pattern
  - [ ] Manager class inherits from `DomoManager`
  - [ ] Manager has reference to entity class
  - [ ] Common manager methods present:
    - [ ] `get()` - retrieve all entities
    - [ ] `get_by_name()` or `search()` - find specific entities
    - [ ] `create()` - create new entity
    - [ ] `update()` - update existing entity
    - [ ] `delete()` - remove entity

### Phase 5: Testing

- [ ] **Task 5.1**: Create/update test file
  - [ ] Test file exists: `tests/classes/test_50_[ClassName].py`
  - [ ] Test file imports class and required modules
  - [ ] Test file loads `.env` for configuration
  - [ ] Test authentication setup (token_auth)

- [ ] **Task 5.2**: Implement test functions (following `DomoUser.py` pattern)
  - [ ] `test_cell_0()` - Setup/authentication helper
  - [ ] `test_cell_1()` - Test `get_by_id()` method
  - [ ] `test_cell_2()` - Test `from_dict()` method
  - [ ] Additional tests for entity-specific methods
  - [ ] Test exception handling (not found, invalid auth, etc.)

- [ ] **Task 5.3**: Document required environment variables
  - [ ] list all `.env` constants needed for tests
  - [ ] Example values provided (sanitized)
  - [ ] Document how to obtain test values

- [ ] **Task 5.4**: Run and validate tests
  - [ ] All tests pass successfully
  - [ ] Tests use async/await properly
  - [ ] Tests clean up resources if needed

---

## 🎯 Acceptance Criteria

### Structure
- ✅ Class inherits from appropriate entity base class
- ✅ All required attributes and methods implemented
- ✅ `@dataclass` decorator applied correctly
- ✅ `__all__` exports include all public classes and exceptions

### Implementation
- ✅ Methods delegate to route functions (no API logic in class)
- ✅ Method signatures follow standards (auth first, typed params)
- ✅ All public methods have docstrings
- ✅ Exception classes imported from route modules
- ✅ No circular import issues

### Composition
- ✅ Appropriate subentities identified and implemented
- ✅ Subentities initialized in `__post_init__()`
- ✅ Subentities use `from_parent()` pattern

### Testing
- ✅ Test file created following `DomoUser.py` pattern
- ✅ All core methods covered by tests
- ✅ Tests run successfully without errors
- ✅ Required `.env` constants documented

### Code Quality
- ✅ Type hints present on all parameters and return values
- ✅ Code follows PEP 8 style guidelines
- ✅ No linting errors from pre-commit hooks
- ✅ Documentation complete and accurate

---

## 🔧 Environment Variables

Document any `.env` constants required for testing:

```bash
# Example constants for [ClassName] tests
DOMO_INSTANCE="your-instance"
DOMO_ACCESS_TOKEN="your-token"
[ENTITY]_ID_1="example-id-1"
[ENTITY]_ID_2="example-id-2"
# Add more as needed
```

### How to Obtain Test Values
<!-- Provide instructions for finding valid test values -->
1. Navigate to your Domo instance
2. [Specific steps to find test entity]
3. Copy the ID from the URL or API response

---

## 📝 Notes

<!-- Add any class-specific notes, quirks, or special considerations -->

### Known Issues
- [ ] list any known bugs or limitations

### Related Issues
- Related to #[issue-number]

### References
- [Entities Documentation](../src/domolibrary2/client/entities.py)
- [Testing Guide](../docs/testing-guide.md)
- [Route Standards](../.github/instructions/routes.instructions.md)
- [DomoUser Example](../src/domolibrary2/classes/DomoUser.py)
- [DomoUser Test Example](../tests/classes/DomoUser.py)

---

## 🚀 Implementation Checklist

Use this checklist to track progress:

- [ ] Phase 1: Structure Validation - Complete
- [ ] Phase 2: Composition Analysis - Complete
- [ ] Phase 3: Route Integration - Complete
- [ ] Phase 4: Manager Class Validation - Complete (if applicable)
- [ ] Phase 5: Testing - Complete
- [ ] All acceptance criteria met
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Ready for merge
