# Class Validation System - Quick Start

## 🎯 Goal

Systematically validate and test all classes in domolibrary2 to ensure they follow proper design patterns, delegate to route functions, and have comprehensive test coverage.

## 📦 What You Get

✅ **GitHub Issue Template** - Structured validation process  
✅ **Comprehensive Guide** - Detailed instructions with examples  
✅ **Quick Reference** - Cheat sheet for fast lookup  
✅ **Issue Generator** - Script to create issues for all classes  
✅ **Generated Issues** - Ready-to-import issue files  

## ⚡ Get Started in 5 Minutes

### 1. Read the Quick Reference (2 min)
```powershell
code docs/class-validation-quick-reference.md
```

### 2. Generate Issue Files (1 min)
```powershell
python scripts/generate-class-validation-issues.py --priority high
```

### 3. Create Your First Issue (1 min)
```powershell
# Option A: GitHub UI
# Navigate to Issues → New Issue → Class Validation template

# Option B: GitHub CLI
gh issue create --body-file "EXPORTS/issues/issue_DomoUser.md"
```

### 4. Start Validating (1 min to setup)
- Open the class file
- Follow the issue tasks
- Reference the quick guide

## 📚 Full Documentation

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [Quick Reference](./class-validation-quick-reference.md) | Fast lookup | 5 min |
| [Comprehensive Guide](./class-validation-guide.md) | Detailed learning | 30 min |
| [System Overview](./class-validation-system-overview.md) | Complete system | 15 min |

## 🎯 Priority Classes

**Start with these 5 classes:**
1. DomoUser (reference implementation)
2. DomoDataset
3. DomoCard
4. DomoPage
5. DomoGroup

**Expected time**: 2-4 hours per class

## 🔑 Key Patterns

### ✅ Required Structure
```python
@dataclass
class DomoEntity(DomoEntity):
    id: str
    auth: DomoAuth = field(repr=False)
    raw: dict = field(default_factory=dict, repr=False)
    
    @property
    def display_url(self): ...
    
    @classmethod
    def from_dict(cls, auth, obj): ...
    
    @classmethod
    async def get_by_id(cls, auth, entity_id): ...
```

### ✅ Method Pattern
```python
async def method_name(
    cls,
    auth: DomoAuth,              # Auth first
    required_param: str,          # Required params
    optional_param: int = 100,    # Defaults
    debug_api: bool = False,      # Debug flag
    session: httpx.AsyncClient = None,
) -> ReturnType:
    """Docstring."""
    # Delegate to route function
    res = await entity_routes.method(auth=auth, ...)
    return cls.from_dict(auth=auth, obj=res.response)
```

## 📋 Validation Phases

1. **Structure** (30 min) - Verify inheritance, attributes, methods
2. **Composition** (30 min) - Identify subentity opportunities
3. **Routes** (30 min) - Verify proper delegation
4. **Manager** (20 min) - Validate collection pattern
5. **Testing** (1-2 hr) - Create comprehensive tests

## 🚀 Commands

```powershell
# Generate all issues
python scripts/generate-class-validation-issues.py

# Generate high priority only
python scripts/generate-class-validation-issues.py --priority high

# Import one issue
gh issue create --body-file "EXPORTS/issues/issue_DomoDataset.md"

# Import all high priority
Get-ChildItem "EXPORTS/issues/issue_*.md" | 
    Where-Object { $_.Name -match "(DomoUser|DomoDataset|DomoCard|DomoPage|DomoGroup)" } |
    ForEach-Object { gh issue create --body-file $_.FullName }
```

## ✅ Success Checklist

Before closing an issue:
- [ ] Inherits from correct base class
- [ ] All required methods present
- [ ] Methods delegate to routes
- [ ] Subentities implemented
- [ ] Tests created and passing
- [ ] .env constants documented
- [ ] No linting errors

## 💡 Pro Tips

1. **Start with DomoUser** - It's the reference
2. **One phase at a time** - Don't skip ahead
3. **Copy patterns** - Use DomoUser as template
4. **Test frequently** - Run after each change
5. **Document .env** - As you discover constants

## 🆘 Need Help?

- **Quick lookup**: Check [Quick Reference](./class-validation-quick-reference.md)
- **Detailed help**: Read [Comprehensive Guide](./class-validation-guide.md)
- **Code examples**: See `src/domolibrary2/classes/DomoUser.py`
- **Test examples**: See `tests/classes/DomoUser.py`

## 🎓 Example Workflow

```powershell
# 1. Generate issues for high priority classes
python scripts/generate-class-validation-issues.py --priority high

# 2. Create issue for DomoUser (reference implementation)
gh issue create --body-file "EXPORTS/issues/issue_DomoUser.md"

# 3. Open the class file
code src/domolibrary2/classes/DomoUser.py

# 4. Follow the issue checklist
# - Verify structure ✅
# - Check composition ✅
# - Validate routes ✅
# - Review tests ✅

# 5. Run tests
pytest tests/classes/DomoUser.py -v

# 6. Close issue when complete
```

## 📞 Questions?

Create a discussion issue or check the comprehensive documentation!

---

**Ready to start?** Pick your first class and create an issue! 🚀
