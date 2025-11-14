# Account Access Sharing - Return Type Update

## Summary

The `add_share()` method on `DomoAccount.Access` now returns an `Account_AccessRelationship` instance instead of a list of all relationships.

## What Changed

### Before (Old Behavior)
```python
# Returned a list of ALL access relationships
relationships = await account.Access.add_share(user_id=123)
# relationships = [<Relationship1>, <Relationship2>, ...]
# Had to find the new one manually
```

### After (New Behavior)
```python
# Returns the specific relationship that was created
relationship = await account.Access.add_share(user_id=123)
# relationship = <Account_AccessRelationship>
print(relationship.entity_id)  # 123
print(relationship.entity_type)  # "USER"
print(relationship.relationship_type)  # "CAN_VIEW"
```

## Usage Examples

### Share with User by ID
```python
from domolibrary2.routes.account import ShareAccount_AccessLevel

# Share account with a user
new_relationship = await account.Access.add_share(
    user_id=456,
    access_level=ShareAccount_AccessLevel.CAN_EDIT
)

print(f"Shared with user {new_relationship.entity_id}")
print(f"Access level: {new_relationship.relationship_type}")
print(f"Entity name: {new_relationship.entity_name}")
```

### Share with User Entity
```python
import domolibrary2.classes.DomoUser as dmu

# Get user object
user = await dmu.DomoUser.get_by_id(auth=auth, user_id=456)

# Share with the user entity
new_relationship = await account.Access.add_share(
    entity=user,
    access_level=ShareAccount_AccessLevel.CAN_VIEW
)

print(f"Shared with {new_relationship.entity_name}")
# Access the user object via relationship
print(f"User email: {new_relationship.entity.email_address}")
```

### Share with Group
```python
# Share account with a group
new_relationship = await account.Access.add_share(
    group_id=789,
    access_level=ShareAccount_AccessLevel.CAN_EDIT
)

print(f"Shared with group {new_relationship.entity_id}")
print(f"Group name: {new_relationship.entity_name}")
```

## Account_AccessRelationship Properties

The returned relationship object has these useful properties:

| Property           | Description                                    |
|--------------------|------------------------------------------------|
| `entity`           | The DomoUser or DomoGroup object               |
| `entity_id`        | ID of the user or group                        |
| `entity_type`      | "USER" or "GROUP"                              |
| `entity_name`      | Email (user) or name (group)                   |
| `relationship_type`| Access level (e.g., "CAN_VIEW", "CAN_EDIT")    |
| `parent_entity`    | The DomoAccount being shared                   |

## Converting to Dictionary

```python
relationship = await account.Access.add_share(user_id=123)

# Get simple dict representation
relationship_dict = relationship.to_dict()
print(relationship_dict)
# {'id': '123', 'type': 'USER'}
```

## Full Example

```python
import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoAccount as dmacc
from domolibrary2.routes.account import ShareAccount_AccessLevel

load_dotenv()

# Authentication
auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"]
)

# Get account
account = await dmacc.DomoAccount.get_by_id(
    auth=auth,
    account_id="12345"
)

# Add new share and get the relationship
new_owner_relationship = await account.Access.add_share(
    user_id=456,
    access_level=ShareAccount_AccessLevel.CAN_EDIT
)

# Use the relationship
print(f"Created relationship:")
print(f"  User ID: {new_owner_relationship.entity_id}")
print(f"  User Email: {new_owner_relationship.entity_name}")
print(f"  Access Level: {new_owner_relationship.relationship_type}")
print(f"  Account: {new_owner_relationship.parent_entity.display_name}")

# The access list has also been refreshed automatically
all_relationships = account.Access.relationships
print(f"\nTotal users/groups with access: {len(all_relationships)}")
```

## OAuth Accounts

The same pattern applies to OAuth accounts:

```python
from domolibrary2.classes.DomoAccount import DomoAccount_OAuth

oauth_account = await DomoAccount_OAuth.get_by_id(
    auth=auth,
    account_id="oauth-123"
)

# Returns Account_AccessRelationship
relationship = await oauth_account.Access.add_share(
    user_id=456,
    access_level=ShareAccount_AccessLevel.CAN_VIEW
)

print(f"Shared OAuth account with {relationship.entity_name}")
```

## Return Raw Response

If you need the raw API response instead:

```python
# Get raw ResponseGetData instead of relationship
raw_response = await account.Access.add_share(
    user_id=456,
    access_level=ShareAccount_AccessLevel.CAN_VIEW,
    return_raw=True
)

print(raw_response.status)  # 200
print(raw_response.response)  # API response dict
```

## Benefits

1. **Direct Access**: Get the relationship you just created immediately
2. **Type Safety**: Know exactly what type you're getting back
3. **Convenience**: No need to search through all relationships
4. **Property Access**: Use convenient properties like `entity_name`, `entity_type`
5. **Auto Refresh**: The full access list is still refreshed in the background

## Migration Guide

### Old Code
```python
# Had to refresh and find the new relationship
await account.Access.add_share(user_id=123)
relationships = await account.Access.get()
new_rel = next(r for r in relationships if r.entity_id == "123")
```

### New Code
```python
# Get it directly
new_rel = await account.Access.add_share(user_id=123)
```

---

**Breaking Change**: No
**Backward Compatible**: The access list is still refreshed, so existing code that accesses `account.Access.relationships` after calling `add_share()` will continue to work.

**Status**: ✅ Live
**Applies To**: Both `DomoAccess_Account` and `DomoAccess_OAuth`
