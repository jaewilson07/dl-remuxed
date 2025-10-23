# Class Validation Guide

## Purpose

This guide provides instructions for using the class validation issue template to systematically review, refactor, and test all classes in the domolibrary2 project.

## Quick Start

### 1. Create an Issue

1. Navigate to GitHub Issues
2. Click "New Issue"
3. Select "Class Validation and Testing" template
4. Replace `[ClassName]` with the actual class name (e.g., "DomoDataset", "DomoCard")
5. Fill in the class location details

### 2. Work Through Phases

Follow the phases in order:
- **Phase 1**: Structure validation (inheritance, required methods)
- **Phase 2**: Composition analysis (subentities)
- **Phase 3**: Route integration (proper imports, delegation)
- **Phase 4**: Manager class validation (if applicable)
- **Phase 5**: Testing (create/update tests)

### 3. Check Acceptance Criteria

Before closing the issue, verify all acceptance criteria are met.

---

## Detailed Phase Breakdown

### Phase 1: Structure Validation

**Goal**: Ensure the class follows the entity hierarchy and has all required components.

#### Task 1.1: Verify Proper Inheritance

**Check the class definition:**

```python
# ✅ Good - inherits from DomoEntity
@dataclass
class DomoUser(DomoEntity):
    id: str
    auth: DomoAuth = field(repr=False)
    # ...

# ❌ Bad - doesn't inherit from base class
class DomoUser:
    def __init__(self, id, auth):
        # ...
```

**Decision Tree for Inheritance:**
- Does the entity track relationships? → Use `DomoEntity_w_Lineage`
- Can it be federated? → Use `DomoFederatedEntity`
- Can it be published/subscribed? → Use `DomoPublishedEntity`
- Is it a collection manager? → Use `DomoManager`
- Does it belong to a parent? → Use `DomoSubEntity`
- Otherwise → Use `DomoEntity`

#### Task 1.2: Validate Required Attributes and Methods

**All DomoEntity subclasses must have:**

```python
@dataclass
class DomoExample(DomoEntity):
    # Required attributes
    id: str
    auth: DomoAuth = field(repr=False)
    raw: dict = field(default_factory=dict, repr=False)
    
    # Optional but common
    display_name: Optional[str] = None
    created_dt: Optional[dt.datetime] = None
    
    @property
    def display_url(self):
        """Return the Domo web URL for this entity."""
        return f"https://{self.auth.domo_instance}.domo.com/[path]/{self.id}"
    
    @classmethod
    def from_dict(cls, auth: DomoAuth, obj: dict):
        """Convert API response dictionary to class instance."""
        return cls(
            auth=auth,
            id=str(obj.get("id")),
            display_name=obj.get("displayName"),
            raw=obj,
        )
    
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

#### Task 1.3: Review Method Signatures

**Standard method signature pattern:**

```python
# ✅ Good - auth first, optional params properly typed
@classmethod
async def search(
    cls,
    auth: DomoAuth,
    search_term: str,
    limit: int = 50,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
) -> List["DomoEntity"]:
    """Search for entities matching term."""
    # Delegate to route function
    res = await entity_routes.search(
        auth=auth,
        search_term=search_term,
        limit=limit,
        debug_api=debug_api,
        session=session,
    )
    return [cls.from_dict(auth=auth, obj=obj) for obj in res.response]

# ❌ Bad - auth not first, no type hints, no docstring
def search(search_term, auth, limit=50):
    # ...
```

---

### Phase 2: Composition Analysis

**Goal**: Identify opportunities to use subentities instead of implementing everything in the main class.

#### Common Subentities

| Subentity | Purpose | Applicable To |
|-----------|---------|---------------|
| `DomoTags` | Entity tagging | Most entities (datasets, cards, pages) |
| `DomoLineage` | Upstream/downstream relationships | Datasets, cards, pages |
| `DomoCertification` | Certification status | Datasets, cards |
| `DomoAccess` | Sharing/permissions | Users, groups, content |
| `DomoMembership` | Group membership | Users, groups |

#### Subentity Pattern

```python
from ..subentity import DomoTag as dmtg, DomoLineage as dmdl

@dataclass
class DomoDataset(DomoEntity_w_Lineage):
    id: str
    auth: DomoAuth = field(repr=False)
    
    # Subentity attributes
    Tags: dmtg.DomoTags = field(default=None)
    # Lineage: dmdl.DomoLineage = field(default=None, repr=False)  # Inherited
    
    def __post_init__(self):
        # Initialize subentities
        self.Tags = dmtg.DomoTags.from_parent(parent=self)
        
        # For entities with lineage
        self.Lineage = dmdl.DomoLineage.from_parent(auth=self.auth, parent=self)
```

#### Entity-Specific Subentities

Some entities need custom subentities:

```python
# DomoDataset has Schema and PDP policies
from . import Schema as dmdsc, PDP as dmpdp

@dataclass
class DomoDataset(DomoEntity_w_Lineage):
    Schema: dmdsc.DomoDataset_Schema = field(default=None)
    PDP: dmpdp.Dataset_PDP_Policies = field(default=None)
    
    def __post_init__(self):
        self.Schema = dmdsc.DomoDataset_Schema.from_parent(parent=self)
        self.PDP = dmpdp.Dataset_PDP_Policies(dataset=self)
```

---

### Phase 3: Route Integration

**Goal**: Ensure class methods properly delegate to route functions.

#### Correct Import Pattern

```python
# ✅ Good - import from routes module
from ...routes import user as user_routes
from ...routes.user.exceptions import (
    User_GET_Error,
    User_CRUD_Error,
    SearchUser_NotFound,
)

# ❌ Bad - importing from client or implementing API logic in class
from ...client.api import make_request
```

#### Delegation Pattern

```python
# ✅ Good - method delegates to route function
@classmethod
async def get_by_id(cls, auth: DomoAuth, user_id: str):
    """Get user by ID."""
    res = await user_routes.get_by_id(
        auth=auth,
        user_id=user_id,
    )
    return cls.from_dict(auth=auth, obj=res.response)

# ❌ Bad - class implements API logic
@classmethod
async def get_by_id(cls, auth: DomoAuth, user_id: str):
    """Get user by ID."""
    url = f"https://{auth.domo_instance}.domo.com/api/data/v1/users/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers={"X-DOMO-Developer-Token": auth.token})
        # ... manual response handling
```

---

### Phase 4: Manager Class Validation

**Goal**: Ensure manager classes follow the standard pattern for entity collections.

#### Manager Pattern

```python
@dataclass
class DomoUsers(DomoManager):
    """Manager class for DomoUser entities."""
    
    auth: DomoAuth = field(repr=False)
    
    async def get(
        self,
        limit: int = 500,
        offset: int = 0,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ) -> List[DomoUser]:
        """Get all users."""
        res = await user_routes.get_users(
            auth=self.auth,
            limit=limit,
            offset=offset,
            debug_api=debug_api,
            session=session,
        )
        return [DomoUser.from_dict(auth=self.auth, obj=obj) for obj in res.response]
    
    async def search(
        self,
        search_term: str,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ) -> List[DomoUser]:
        """Search for users by term."""
        res = await user_routes.search_users(
            auth=self.auth,
            search_term=search_term,
            debug_api=debug_api,
            session=session,
        )
        
        if not res.response:
            raise SearchUser_NotFound(
                domo_instance=self.auth.domo_instance,
                search_term=search_term,
            )
        
        return [DomoUser.from_dict(auth=self.auth, obj=obj) for obj in res.response]
    
    async def create(
        self,
        email_address: str,
        role_id: int,
        display_name: Optional[str] = None,
        # ... other params
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ) -> DomoUser:
        """Create a new user."""
        res = await user_routes.create_user(
            auth=self.auth,
            email_address=email_address,
            role_id=role_id,
            display_name=display_name,
            debug_api=debug_api,
            session=session,
        )
        return DomoUser.from_dict(auth=self.auth, obj=res.response)
```

---

### Phase 5: Testing

**Goal**: Create comprehensive tests following the established pattern.

#### Test File Structure

```python
"""
Test file for DomoEntity class
Tests entity methods and validates API integration
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.routes.entity as entity_routes
import domolibrary2.classes.DomoEntity as dme

load_dotenv()

# Setup authentication
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test constants from .env
TEST_ENTITY_ID_1 = os.environ.get("ENTITY_ID_1")
TEST_ENTITY_ID_2 = os.environ.get("ENTITY_ID_2")


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to get authenticated user ID."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1(token_auth=token_auth):
    """Test get_by_id method."""
    entity = await dme.DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID_1,
        return_raw=False,
    )
    
    assert entity is not None
    assert entity.id == TEST_ENTITY_ID_1
    assert entity.display_url is not None
    return entity


async def test_cell_2(token_auth=token_auth):
    """Test from_dict method."""
    # Get raw response
    raw_entity = await dme.DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID_1,
        return_raw=True,
    )
    
    # Convert to class instance
    entity = dme.DomoEntity.from_dict(
        auth=token_auth,
        obj=raw_entity.response,
    )
    
    assert entity.id == TEST_ENTITY_ID_1
    return entity


async def test_cell_3(token_auth=token_auth):
    """Test search method."""
    manager = dme.DomoEntities(auth=token_auth)
    results = await manager.search(search_term="test")
    
    assert isinstance(results, list)
    assert len(results) > 0
    return results


async def test_cell_4(token_auth=token_auth):
    """Test exception handling - not found."""
    try:
        entity = await dme.DomoEntity.get_by_id(
            auth=token_auth,
            entity_id="invalid-id-999999",
        )
        assert False, "Should have raised exception"
    except entity_routes.Entity_GET_Error as e:
        assert "not found" in str(e).lower()
        return True
```

#### Environment Variables Documentation

**In the issue, document all required constants:**

```bash
# Required for DomoEntity tests
DOMO_INSTANCE="your-instance"
DOMO_ACCESS_TOKEN="your-developer-token"
ENTITY_ID_1="valid-entity-id-1"
ENTITY_ID_2="valid-entity-id-2"

# Optional - for specific test scenarios
ENTITY_NAME_SEARCH="test entity name"
```

**Provide instructions to obtain values:**

1. **DOMO_INSTANCE**: Your Domo instance subdomain (e.g., "mycompany")
2. **DOMO_ACCESS_TOKEN**: Create a developer token at Admin > Security > Access Tokens
3. **ENTITY_ID_1**: Navigate to a test entity in Domo, copy ID from URL
4. **ENTITY_ID_2**: Repeat for a second test entity

---

## Common Issues and Solutions

### Issue: Circular Import

**Problem**: Class imports subentity, subentity imports class

**Solution**: Use TYPE_CHECKING and string annotations

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .DomoDataset import DomoDataset

@dataclass
class DomoDataset_Schema(DomoSubEntity):
    parent: "DomoDataset" = field(repr=False)
```

### Issue: Missing Route Function

**Problem**: Class method needs functionality not in routes

**Solution**: 
1. Create the route function first
2. Add proper exception handling
3. Update route module `__init__.py` to export it
4. Then implement class method using the route function

### Issue: Tests Fail Due to Missing Constants

**Problem**: Test tries to use `TEST_ENTITY_ID_1` but it's not in `.env`

**Solution**:
1. Document the required constant in the issue
2. Add instructions for obtaining the value
3. Update `.env_sample` with the new constant
4. Commit the issue with the requirements

### Issue: Method Signature Doesn't Match Route

**Problem**: Class method parameters don't align with route function

**Solution**: Update class method to match route signature:

```python
# Route function signature (correct)
async def get_entity(
    auth: DomoAuth,
    entity_id: str,
    include_details: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    # ...

# Class method should match
@classmethod
async def get_by_id(
    cls,
    auth: DomoAuth,
    entity_id: str,
    include_details: bool = False,  # ← Match route param
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    res = await entity_routes.get_entity(
        auth=auth,
        entity_id=entity_id,
        include_details=include_details,  # ← Pass through
        debug_api=debug_api,
        session=session,
    )
    return cls.from_dict(auth=auth, obj=res.response)
```

---

## Checklist for Issue Completion

Before closing the issue, verify:

- [ ] All phase tasks completed
- [ ] All acceptance criteria met
- [ ] Tests run successfully
- [ ] No linting errors
- [ ] Documentation updated
- [ ] `.env_sample` updated with new constants
- [ ] Code reviewed (if team workflow requires)
- [ ] Branch merged to main

---

## Prioritization Strategy

### High Priority Classes
Start with these commonly-used classes:
1. `DomoUser` (reference implementation)
2. `DomoDataset`
3. `DomoCard`
4. `DomoPage`
5. `DomoGroup`

### Medium Priority
Core infrastructure classes:
- `DomoRole`
- `DomoAccount`
- `DomoActivityLog`
- `DomoApplication`

### Lower Priority
Specialized or less commonly used classes:
- Enterprise-specific features
- Legacy integrations
- Utility classes

---

## Related Documentation

- [Class Instructions](../.github/instructions/classes.instructions.md) - Copilot class standards
- [Route Instructions](../.github/instructions/routes.instructions.md) - Route function requirements
- [General Instructions](../.github/instructions/general.instructions.md) - Project conventions

---

## Questions?

If you encounter issues or have questions while working through class validation:

1. Check this guide for common solutions
2. Review the reference implementation (`DomoUser.py`)
3. Check existing test patterns (`tests/classes/DomoUser.py`)
4. Create a discussion issue for clarification
