# Refactor @patch_to to Direct Class Methods - Copilot Instructions

## Project Context
This is `domolibrary2`, a Python library that currently uses nbdev's `@patch_to` decorator pattern to add methods to dataclasses. We need to refactor this to use direct class method definitions for better maintainability and type checking.

## Current Architecture
- **221 `@patch_to` decorators** across the codebase
- Methods are defined outside the class and patched in using `@patch_to(ClassName)`
- Class methods use `@patch_to(ClassName, cls_method=True)`
- Base classes are `@dataclass` decorated

## Target Architecture
- All methods should be defined directly within their respective classes
- Maintain all existing functionality and method signatures
- Preserve async/await patterns
- Keep dataclass structure but extend with methods

## Refactoring Patterns

### **Pattern 1: Instance Methods**

**BEFORE:**
```python
@dataclass
class DomoUser:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    # ... other fields

@patch_to(DomoUser)
async def get_role(
    self: DomoUser,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
) -> Optional[Any]:
    # method implementation
    pass
```

**AFTER:**
```python
@dataclass
class DomoUser:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    # ... other fields
    
    async def get_role(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
    ) -> Optional[Any]:
        # method implementation
        pass
```

### **Pattern 2: Class Methods**

**BEFORE:**
```python
@patch_to(DomoUser, cls_method=True)
async def get_by_id(
    cls: DomoUser,
    user_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoUser]:
    # method implementation
    pass
```

**AFTER:**
```python
@dataclass
class DomoUser:
    # ... fields
    
    @classmethod
    async def get_by_id(
        cls,
        user_id: str,
        auth: dmda.DomoAuth,
    ) -> Optional["DomoUser"]:
        # method implementation
        pass
```

### **Pattern 3: Static Methods**
If any methods don't use `self` or `cls`, convert to `@staticmethod`.

## Implementation Requirements

### **1. File Processing Order**
Process files in this priority order:
1. `src/client/` - Core client classes
2. `src/classes/` - Main entity classes  
3. `src/utils/` - Utility classes
4. `src/integrations/` - Integration classes

### **2. For Each File:**

#### **Step 1: Analyze Current Structure**
- Identify the main dataclass(es)
- Find all `@patch_to` methods for each class
- Note method types (instance, class, static)

#### **Step 2: Refactor Class Definition**
- Keep the `@dataclass` decorator
- Keep all existing fields unchanged
- Move all patched methods inside the class definition
- Remove `@patch_to` decorators
- Add `@classmethod` for class methods

#### **Step 3: Update Method Signatures**
- Remove explicit type hints for `self` (keep for `cls` in classmethods)
- Use quotes for forward references: `-> "DomoUser"`
- Keep all existing parameter names and defaults
- Maintain async/await patterns

#### **Step 4: Update Imports**
- Remove `from nbdev.showdoc import patch_to` if no longer needed
- Add typing imports if needed for return types

### **3. Type Hints Requirements**
- All parameters must have type hints
- All return types must be annotated
- Use `Optional["ClassName"]` for nullable class returns
- Use `List["ClassName"]` for list returns
- Use quotes for forward references to avoid circular imports

### **4. Common Method Signatures to Preserve**

```python
# Standard async instance method
async def method_name(
    self,
    param: str,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
    return_raw: bool = False,
) -> Union["DomoUser", ResponseGetData, None]:
    pass

# Standard async class method  
@classmethod
async def get_by_id(
    cls,
    auth: dmda.DomoAuth,
    entity_id: str,
    debug_api: bool = False,
    session: Optional[httpx.AsyncClient] = None,
) -> Optional["DomoUser"]:
    pass
```

## Critical Preservation Requirements

### **Must Preserve:**
- ✅ All existing functionality
- ✅ All method signatures and parameters
- ✅ All async/await patterns
- ✅ All dataclass fields and their types
- ✅ All import aliases (`DomoAuth as dmda`, etc.)
- ✅ All docstrings
- ✅ All error handling patterns

### **Must Remove:**
- ❌ All `@patch_to` decorators
- ❌ `from nbdev.showdoc import patch_to` (if no longer used)
- ❌ Explicit `self: ClassName` type hints in method signatures

### **Must Add:**
- ✅ `@classmethod` decorators for class methods
- ✅ Proper indentation inside class definitions
- ✅ Forward reference quotes for return types
- ✅ Missing type hints following project patterns

## Example Complete Refactor

**BEFORE (DomoUser.py):**
```python
from nbdev.showdoc import patch_to

@dataclass
class DomoUser:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    display_name: Optional[str] = None

@patch_to(DomoUser)
async def get_role(self: DomoUser, debug_api: bool = False):
    # implementation
    pass

@patch_to(DomoUser, cls_method=True)
async def get_by_id(cls: DomoUser, user_id: str, auth: dmda.DomoAuth):
    # implementation
    pass
```

**AFTER (DomoUser.py):**
```python
# Remove patch_to import if not needed elsewhere

@dataclass
class DomoUser:
    auth: dmda.DomoAuth = field(repr=False)
    id: str
    display_name: Optional[str] = None
    
    async def get_role(
        self,
        debug_api: bool = False,
    ) -> Optional[Any]:
        # implementation
        pass
    
    @classmethod
    async def get_by_id(
        cls,
        user_id: str,
        auth: dmda.DomoAuth,
    ) -> Optional["DomoUser"]:
        # implementation
        pass
```

## Quality Assurance

### **Testing Requirements:**
- All imports must work: `python -c "import src; print('Success!')"`
- All existing tests must pass
- No breaking changes to public API
- Type checking should improve (no mypy errors)

### **File Validation:**
After refactoring each file:
1. Check syntax: `python -m py_compile filename.py`
2. Test imports: `python -c "from src.module import ClassName"`
3. Run linting: `ruff check filename.py`

### **Progress Tracking:**
- Keep count of files processed
- Note any patterns that don't fit the standard refactor
- Document any methods that require special handling

## Success Criteria
- ✅ Zero `@patch_to` decorators remaining
- ✅ All functionality preserved
- ✅ All type hints properly applied
- ✅ All imports working
- ✅ Code passes linting
- ✅ Improved IDE support and type checking