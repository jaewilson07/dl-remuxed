---
applyTo: 'src/domolibrary2/classes/**/*'
---
# Class Validation and Structure Standards

## Entity Hierarchy

All Domo entities must inherit from the appropriate base class:

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

### Choosing the Right Base Class

- **DomoEntity**: Basic entity with id, auth, raw
- **DomoEntity_w_Lineage**: Entity that tracks relationships (datasets, cards, pages)
- **DomoFederatedEntity**: Entity that can be federated across instances
- **DomoPublishedEntity**: Entity that supports publish/subscribe
- **DomoManager**: Collection manager (e.g., DomoUsers, DomoDatasets)
- **DomoSubEntity**: Entity that belongs to a parent (e.g., Schema, Tags)

## Required Class Structure

### All DomoEntity Subclasses Must Have:

```python
from dataclasses import dataclass, field
from ..client.auth import DomoAuth
from ..client.entities import DomoEntity

@dataclass
class DomoExample(DomoEntity):
    # REQUIRED attributes
    id: str
    auth: DomoAuth = field(repr=False)
    raw: dict = field(default_factory=dict, repr=False)
    
    # Optional attributes
    display_name: Optional[str] = None
    created_dt: Optional[dt.datetime] = None
    
    # REQUIRED: display_url property or method
    @property
    def display_url(self):
        """Return the Domo web URL for this entity."""
        return f"https://{self.auth.domo_instance}.domo.com/path/{self.id}"
    
    # REQUIRED: from_dict classmethod
    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict):
        """Convert API response dictionary to class instance."""
        return cls(
            auth=auth,
            id=str(obj.get("id")),
            display_name=obj.get("displayName"),
            raw=obj,
        )
    
    # REQUIRED: get_by_id classmethod
    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        entity_id: str,
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        """Retrieve entity by ID from Domo API."""
        # MUST delegate to route function
        res = await entity_routes.get_by_id(
            auth=auth,
            entity_id=entity_id,
            debug_api=debug_api,
            session=session,
        )
        
        if return_raw:
            return res
        
        return cls.from_dict(auth=auth, obj=res.response)
```

## Composition Over Inheritance

Use DomoSubEntity for related functionality instead of adding everything to the main class.

### Common Subentities:

```python
from ..subentity import (
    DomoTag as dmtg,
    DomoLineage as dmdl,
    DomoCertification as dmdc,
    DomoAccess as dmac,
)

@dataclass
class DomoDataset(DomoEntity_w_Lineage):
    # Subentity attributes
    Tags: dmtg.DomoTags = field(default=None)
    Certification: dmdc.DomoCertification = field(default=None)
    Schema: dmdsc.DomoDataset_Schema = field(default=None)
    
    def __post_init__(self):
        # Initialize subentities
        self.Tags = dmtg.DomoTags.from_parent(parent=self)
        self.Lineage = dmdl.DomoLineage.from_parent(auth=self.auth, parent=self)
        self.Schema = dmdsc.DomoDataset_Schema.from_parent(parent=self)
        
        if self.raw.get("certification"):
            self.Certification = dmdc.DomoCertification.from_parent(parent=self)
```

### Which Entities Need Which Subentities:

- **DomoTags**: Most entities (datasets, cards, pages)
- **DomoLineage**: Datasets, cards, pages
- **DomoCertification**: Datasets, cards
- **DomoAccess**: Entities with sharing/permissions
- **DomoMembership**: Users, groups

## Method Standards

### Signature Pattern:

```python
async def method_name(
    self,
    auth: DomoAuth,              # Auth always first (after self/cls)
    required_param: str,          # Required params (typed)
    optional_param: int = 100,    # Optional params with defaults
    debug_api: bool = False,      # Debug flag
    session: httpx.AsyncClient = None,
    return_raw: bool = False,     # return_raw on methods that call routes
) -> ReturnType:
    """Docstring describing method.
    
    Args:
        auth: Authentication object
        required_param: Description
        optional_param: Description
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionName: When error occurs
    """
    # MUST delegate to route function - no API logic in class
    res = await entity_routes.method_name(
        auth=auth,
        param=required_param,
        debug_api=debug_api,
        session=session,
    )
    
    if return_raw:
        return res
    
    # Process and return
    return self.from_dict(auth=auth, obj=res.response)
```

### Critical Rules:

1. **Delegation**: Class methods MUST call route functions, never implement API logic
2. **Auth First**: `auth` parameter always comes first (after `self`/`cls`)
3. **Type Hints**: All parameters and returns must have type hints
4. **Docstrings**: All public methods must have docstrings
5. **return_raw**: Include on methods that call route functions

## Import Standards

### Correct Imports:

```python
# ✅ Import route functions from routes module
from ...routes import user as user_routes
from ...routes.user import UserProperty_Type, UserProperty
from ...routes.user.exceptions import (
    User_GET_Error,
    User_CRUD_Error,
    SearchUser_NotFound,
)

# ✅ Import subentities
from ..subentity import DomoTag as dmtg, DomoLineage as dmdl

# ✅ Import client entities
from ...client.entities import DomoEntity, DomoManager
from ...client.auth import DomoAuth
```

### Incorrect Imports:

```python
# ❌ DO NOT import exceptions from client
from ...client.auth import InvalidAuthTypeError  # Wrong!
# Should be: from ...routes.auth import InvalidAuthTypeError

# ❌ DO NOT implement API logic in class
import httpx  # Only if absolutely necessary
# Prefer delegating to route functions
```

## Exception Handling

Always use route-specific exceptions:

```python
from ...routes.entity.exceptions import (
    Entity_GET_Error,
    Entity_CRUD_Error,
    SearchEntity_NotFound,
)

# In methods, let route exceptions propagate or catch and re-raise
try:
    res = await entity_routes.get_by_id(auth=auth, entity_id=entity_id)
except Entity_GET_Error as e:
    # Handle or re-raise
    raise
```

## Manager Pattern

For entity collections (DomoUsers, DomoDatasets, etc.):

```python
@dataclass
class DomoEntities(DomoManager):
    """Manager class for DomoEntity collection."""
    
    auth: DomoAuth = field(repr=False)
    
    async def get(
        self,
        limit: int = 500,
        offset: int = 0,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ) -> List[DomoEntity]:
        """Get all entities."""
        res = await entity_routes.get_entities(
            auth=self.auth,
            limit=limit,
            offset=offset,
            debug_api=debug_api,
            session=session,
        )
        return [DomoEntity.from_dict(auth=self.auth, obj=obj) for obj in res.response]
    
    async def search(
        self,
        search_term: str,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ) -> List[DomoEntity]:
        """Search for entities."""
        res = await entity_routes.search_entities(
            auth=self.auth,
            search_term=search_term,
            debug_api=debug_api,
            session=session,
        )
        
        if not res.response:
            raise SearchEntity_NotFound(
                domo_instance=self.auth.domo_instance,
                search_term=search_term,
            )
        
        return [DomoEntity.from_dict(auth=self.auth, obj=obj) for obj in res.response]
```

## Testing Requirements

Every class must have a corresponding test file in `tests/classes/`:

```python
# tests/classes/test_50_DomoEntity.py
import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoEntity as dme

load_dotenv()

token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

TEST_ENTITY_ID_1 = os.environ.get("ENTITY_ID_1")

async def test_cell_1(token_auth=token_auth):
    """Test get_by_id method."""
    entity = await dme.DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID_1,
    )
    assert entity is not None
    assert entity.id == TEST_ENTITY_ID_1
    return entity
```

## Common Patterns

### __post_init__ for ID Conversion:

```python
def __post_init__(self):
    self.id = str(self.id)  # Ensure ID is string
    # Initialize subentities
    self.Tags = dmtg.DomoTags.from_parent(parent=self)
```

### __eq__ for Comparison:

```python
def __eq__(self, other) -> bool:
    if self.__class__.__name__ != other.__class__.__name__:
        return False
    return self.id == other.id
```

## Reference Implementation

See `src/domolibrary2/classes/DomoUser.py` as the reference implementation that follows all these patterns correctly.

## Documentation

For detailed guidance, see:
- [Class Validation Guide](../../docs/class-validation-guide.md)
- [Quick Reference](../../docs/class-validation-quick-reference.md)
- [Testing Guide](../../docs/testing-guide.md)
