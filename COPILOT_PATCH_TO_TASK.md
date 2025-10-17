# Copilot Coding Agent Task: Refactor @patch_to to Direct Class Methods

## Task Overview
Systematically refactor the entire codebase to eliminate `@patch_to` decorators and move all patched methods directly into their respective class definitions. This is a large-scale refactoring affecting 38 files and 221 methods across 45 classes.

## Critical Instructions
**READ `PATCH_TO_REFACTOR_INSTRUCTIONS.md` AND `patch-to-refactoring-guide.md` BEFORE STARTING**

These files contain:
- Detailed refactoring patterns and examples
- Complete implementation requirements  
- Quality assurance guidelines
- File-by-file implementation plan

## Scope
- **Files to refactor:** 38 files
- **Methods to relocate:** 221 @patch_to methods
- **Classes affected:** 45 classes
- **Zero tolerance for breaking changes**

## Implementation Priority Order
1. **`src/client/`** (2 files) - Core client classes, fewest dependencies
2. **`src/classes/`** (35 files) - Main entity classes
3. **`src/utils/`** (1 file) - Utility classes

## Refactoring Requirements

### **Core Transformation Pattern**
```python
# BEFORE - External patched method
@patch_to(DomoUser)
async def get_role(
    self: DomoUser,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
) -> Optional[Any]:
    # implementation
    pass

# AFTER - Direct class method
@dataclass
class DomoUser:
    # ... existing fields ...
    
    async def get_role(
        self,
        debug_api: bool = False,  
        session: Optional[httpx.AsyncClient] = None,
    ) -> Optional[Any]:
        # implementation (unchanged)
        pass
```

### **Class Method Pattern**
```python
# BEFORE
@patch_to(DomoUser, cls_method=True)
async def get_by_id(cls: DomoUser, user_id: str, auth: dmda.DomoAuth):
    pass

# AFTER  
@dataclass
class DomoUser:
    # ... fields ...
    
    @classmethod
    async def get_by_id(cls, user_id: str, auth: dmda.DomoAuth) -> Optional["DomoUser"]:
        pass
```

## Strict Requirements

### **MUST PRESERVE (Zero Tolerance):**
- ✅ All existing functionality and behavior
- ✅ All method signatures, parameters, and defaults
- ✅ All async/await patterns
- ✅ All dataclass fields and decorators
- ✅ All docstrings and comments
- ✅ All import aliases (`DomoAuth as dmda`, etc.)
- ✅ All error handling patterns

### **MUST REMOVE:**
- ❌ All `@patch_to` decorators (221 total)
- ❌ `from nbdev.showdoc import patch_to` imports (where no longer needed)
- ❌ Explicit `self: ClassName` type hints in method signatures

### **MUST ADD:**
- ✅ `@classmethod` decorators for methods that had `cls_method=True`
- ✅ Proper indentation inside class definitions
- ✅ Forward reference quotes for return types: `-> "DomoUser"`
- ✅ Complete type hints following project patterns

## Implementation Process

### **For Each File:**

1. **Identify Structure**
   - Find main dataclass(es) 
   - List all `@patch_to` methods for each class
   - Note which are instance vs class methods

2. **Move Methods Into Classes**
   - Cut each `@patch_to` method
   - Paste inside the appropriate class definition
   - Remove `@patch_to` decorator
   - Add `@classmethod` if it was `cls_method=True`
   - Remove explicit `self:` or `cls:` type hints
   - Add forward reference quotes to return types

3. **Clean Up Imports**
   - Remove `patch_to` import if no longer used in file
   - Add any missing typing imports

4. **Validate Each File**
   - Syntax check: `python -m py_compile filename.py`
   - Import test: `python -c "from src.module import ClassName"`

## Key Files to Process

### **Start Here - Client Directory:**
1. `src/client/Logger.py` - 5 methods to move into `Logger` class
2. `src/client/ResponseGetData.py` - 3 methods to move into `ResponseGetData` class

### **Major Classes (High Priority):**
- `DomoUser.py` - 32 methods
- `DomoAccount.py` - 13 methods  
- `DomoDataset.py` - 25 methods
- `DomoAuth.py` - Multiple auth classes
- `DomoApplication.py` - 14 methods

## Quality Assurance

### **After Each File:**
```bash
# Test syntax
python -m py_compile src/path/to/file.py

# Test imports
python -c "from src.classes.DomoUser import DomoUser; print('Success')"
```

### **After Complete Refactor:**
```bash
# Test all imports
python -c "import src; print('All imports successful')"

# Run linting
.\scripts\lint.ps1

# Verify zero @patch_to remaining
findstr /s /n "@patch_to" src\*.py

# Run tests
.\scripts\test.ps1
```

## Common Gotchas to Avoid

1. **Don't change method implementations** - only move them
2. **Don't alter parameter names or defaults**
3. **Don't forget @classmethod decorators** for class methods
4. **Don't break circular imports** - use quoted forward references
5. **Don't remove necessary imports** - only remove unused `patch_to`

## Expected Outcomes

### **Before Refactor:**
- 221 `@patch_to` decorators scattered across files
- Methods defined outside their classes
- nbdev dependency for `patch_to`

### **After Refactor:**
- Zero `@patch_to` decorators
- All methods properly encapsulated in classes
- Better IDE support and type checking
- Cleaner, more maintainable code structure

## Success Criteria
- ✅ Zero `@patch_to` decorators in codebase
- ✅ All 221 methods successfully moved into classes
- ✅ All imports work without errors
- ✅ All existing functionality preserved
- ✅ Code passes linting and type checking
- ✅ No breaking changes to public API

## Implementation Support
- Use `patch-to-refactoring-guide.md` for file-by-file detailed instructions
- Each file has specific examples and method lists
- Process files in the specified priority order
- Test frequently to catch issues early

This refactoring will significantly improve the codebase maintainability and eliminate the nbdev dependency for method patching.

#github-pull-request_copilot-coding-agent