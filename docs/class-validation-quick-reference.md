# Class Validation Quick Reference

## 🚀 Quick Start

1. **Create Issue**: Use "Class Validation and Testing" template
2. **Replace Placeholders**: Fill in `[ClassName]`, file paths, route modules
3. **Work Through Phases**: Complete tasks in order (1→2→3→4→5)
4. **Verify Criteria**: Check all acceptance criteria before closing

---

## 📊 Entity Hierarchy Quick Reference

```
DomoBase (abstract)
└── DomoEntity
    ├── DomoEntity_w_Lineage
    │   ├── DomoFederatedEntity
    │   │   └── DomoPublishedEntity
    │   └── [Custom entities]
    └── DomoManager

DomoSubEntity (composition)
```

**Decision Tree:**
- Tracks relationships? → `DomoEntity_w_Lineage`
- Collection manager? → `DomoManager`
- Belongs to parent? → `DomoSubEntity`
- Otherwise → `DomoEntity`

---

## ✅ Required Class Components

### All DomoEntity Classes Must Have:

```python
@dataclass
class DomoExample(DomoEntity):
    # ✅ Required attributes
    id: str
    auth: DomoAuth = field(repr=False)
    raw: dict = field(default_factory=dict, repr=False)
    
    # ✅ Required property
    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/path/{self.id}"
    
    # ✅ Required methods
    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict):
        """Convert API response to class instance."""
        return cls(auth=auth, id=str(obj.get("id")), raw=obj)
    
    @classmethod
    async def get_by_id(cls, auth: DomoAuth, entity_id: str, ...):
        """Retrieve entity from API."""
        res = await entity_routes.get_by_id(auth=auth, entity_id=entity_id)
        return cls.from_dict(auth=auth, obj=res.response)
```

---

## 🧩 Common Subentities

| Subentity | Use Case | Applicable To |
|-----------|----------|---------------|
| `DomoTags` | Tagging | Datasets, cards, pages |
| `DomoLineage` | Relationships | Datasets, cards, pages |
| `DomoCertification` | Certification | Datasets, cards |
| `DomoAccess` | Permissions | Users, groups, content |
| `DomoMembership` | Group membership | Users, groups |

### Subentity Pattern:

```python
from ..subentity import DomoTag as dmtg

@dataclass
class DomoEntity(DomoEntity_w_Lineage):
    Tags: dmtg.DomoTags = field(default=None)
    
    def __post_init__(self):
        self.Tags = dmtg.DomoTags.from_parent(parent=self)
```

---

## 📝 Method Signature Standards

### ✅ Correct Signature:

```python
async def method_name(
    self,
    auth: DomoAuth,              # Auth first
    required_param: str,          # Required params (typed)
    optional_param: int = 100,    # Optional params with defaults
    debug_api: bool = False,      # Debug flag
    session: httpx.AsyncClient = None,  # Session param
) -> ReturnType:
    """Docstring describing method."""
    # Delegate to route function
```

### ❌ Incorrect Signature:

```python
def method_name(required_param, auth, optional_param=100):
    # No type hints, auth not first, no docstring, not async
```

---

## 🧪 Test File Template

```python
"""Test file for DomoEntity"""
import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.routes.entity as entity_routes
import domolibrary2.classes.DomoEntity as dme

load_dotenv()

token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

TEST_ENTITY_ID_1 = os.environ.get("ENTITY_ID_1")


async def test_cell_0(token_auth=token_auth) -> str:
    """Setup helper."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1(token_auth=token_auth):
    """Test get_by_id."""
    entity = await dme.DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID_1,
    )
    assert entity is not None
    return entity


async def test_cell_2(token_auth=token_auth):
    """Test from_dict."""
    raw = await dme.DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID_1,
        return_raw=True,
    )
    entity = dme.DomoEntity.from_dict(auth=token_auth, obj=raw.response)
    assert entity.id == TEST_ENTITY_ID_1
    return entity
```

---

## 🎯 Acceptance Criteria Checklist

Quick checklist before closing issue:

- [ ] ✅ Inherits from correct base class
- [ ] ✅ `@dataclass` decorator applied
- [ ] ✅ Required attributes: `id`, `auth`, `raw`
- [ ] ✅ Required methods: `display_url`, `from_dict`, `get_by_id`
- [ ] ✅ Methods delegate to route functions
- [ ] ✅ Exceptions imported from `routes.[entity].exceptions`
- [ ] ✅ Subentities identified and implemented
- [ ] ✅ Type hints on all parameters
- [ ] ✅ Docstrings on all public methods
- [ ] ✅ Test file created/updated
- [ ] ✅ All tests pass
- [ ] ✅ `.env` constants documented
- [ ] ✅ No linting errors

---

## 🔧 Common Issues & Quick Fixes

### Circular Import
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Parent import ParentClass

@dataclass
class Child:
    parent: "ParentClass" = field(repr=False)
```

### Wrong Import Location
```python
# ❌ Wrong
from ...client.auth import InvalidAuthTypeError

# ✅ Correct
from ...routes.auth import InvalidAuthTypeError
```

### Missing Route Exception
```python
# Add to routes/[entity]/exceptions.py
class SearchEntity_NotFound(DomoError):
    def __init__(self, domo_instance, search_term):
        super().__init__(
            domo_instance=domo_instance,
            message=f"No entity found matching '{search_term}'",
        )

# Export in routes/[entity]/__init__.py
from .exceptions import SearchEntity_NotFound
__all__ = [..., "SearchEntity_NotFound"]

# Import in class file
from ...routes.entity import SearchEntity_NotFound
```

### Missing Test Constants
```bash
# Document in issue Environment Variables section:
ENTITY_ID_1="obtain-from-url"
ENTITY_ID_2="obtain-from-url"

# Add to .env_sample
# Update testing documentation
```

---

## 📋 Phase Completion Checklist

### Phase 1: Structure
- [ ] Inheritance verified
- [ ] Required attributes present
- [ ] Required methods implemented
- [ ] Method signatures reviewed

### Phase 2: Composition
- [ ] Subentities identified
- [ ] Subentities implemented
- [ ] `__post_init__` updated

### Phase 3: Routes
- [ ] Route imports verified
- [ ] Methods delegate to routes
- [ ] Exceptions imported correctly

### Phase 4: Manager (if applicable)
- [ ] Inherits from `DomoManager`
- [ ] Standard methods present
- [ ] Follows manager pattern

### Phase 5: Testing
- [ ] Test file created/updated
- [ ] Core methods tested
- [ ] Environment variables documented
- [ ] All tests pass

---

## 🔗 Quick Links

- [Full Guide](./class-validation-guide.md)
- [Issue Template](../.github/ISSUE_TEMPLATE/class-validation.md)
- [DomoUser Reference](../src/domolibrary2/classes/DomoUser.py)
- [DomoUser Tests](../tests/classes/DomoUser.py)
- [Entity Base Classes](../src/domolibrary2/client/entities.py)
- [Testing Guide](./testing-guide.md)

---

## 💡 Pro Tips

1. **Start with DomoUser**: It's the reference implementation
2. **One phase at a time**: Don't skip ahead
3. **Document as you go**: Update `.env` requirements immediately
4. **Test frequently**: Run tests after each change
5. **Use type hints**: They catch errors before runtime
6. **Copy patterns**: DomoUser, DomoDataset show best practices
7. **Ask questions**: Create discussion issues for clarification

---

## 📊 Class Priority Matrix

### Start Here (High Priority):
- DomoUser ⭐️ (reference implementation)
- DomoDataset
- DomoCard
- DomoPage
- DomoGroup

### Next (Medium Priority):
- DomoRole
- DomoAccount
- DomoActivityLog
- DomoApplication

### Later (Lower Priority):
- Specialized features
- Legacy integrations
- Utility classes

---

## 🎓 Example Issue Title Format

```
Validate and Test: DomoDataset
Validate and Test: DomoCard
Validate and Test: DomoPage
```

---

## ⚡ Speed Run (For Experienced Contributors)

1. Create issue from template
2. Phase 1: Check `@dataclass`, inheritance, required methods
3. Phase 2: Add missing subentities (`Tags`, `Lineage`, `Certification`)
4. Phase 3: Verify route imports, fix delegation
5. Phase 4: Validate manager pattern (if exists)
6. Phase 5: Create test file, run tests, document `.env`
7. Verify all acceptance criteria
8. Close issue

**Average time per class**: 1-3 hours depending on complexity

---

**Need help?** Check the [full guide](./class-validation-guide.md) or create a discussion issue!
