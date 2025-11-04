# DomoStream Account Composition

## Overview

`DomoStream` now includes an `Account` attribute that provides access to the connector account associated with the stream. This follows the same composition pattern used for other relationships in the library (e.g., `DomoDataset.Stream`, `DomoDataset.Schema`).

## Features

### Account Attribute

The `Account` attribute is:
- **Optional**: Only populated when account information is available
- **Lazy-loaded**: Can be retrieved on-demand using `get_account()` method
- **Auto-loaded**: Automatically retrieved by `get_by_id()` when `is_retrieve_account=True` (default)
- **Excluded from serialization**: Marked with `repr=False` so it doesn't appear in `to_dict()` output

### Related Fields

In addition to the `Account` object, DomoStream maintains account metadata fields:
- `account_id`: Account identifier (string)
- `account_display_name`: Human-readable account name
- `account_userid`: User ID associated with the account

These fields are always populated from the stream's raw data and **are included** in `to_dict()` output.

## Usage Examples

### Basic Stream Retrieval with Account

```python
from domolibrary2.classes.DomoDataset.stream import DomoStream
from domolibrary2.client.auth import DomoTokenAuth

auth = DomoTokenAuth(
    domo_instance="your-instance",
    domo_access_token="your-token"
)

# Get stream by ID (automatically retrieves Account if account_id is present)
stream = await DomoStream.get_by_id(
    auth=auth,
    stream_id="stream-123"
)

# Access account information
if stream.Account:
    print(f"Account Name: {stream.Account.name}")
    print(f"Account Type: {stream.Account.data_provider_type}")
    print(f"Account ID: {stream.Account.id}")
else:
    print("No account associated with this stream")

# Access account metadata (always available if in raw data)
print(f"Account ID: {stream.account_id}")
print(f"Account Display Name: {stream.account_display_name}")
```

### Skip Account Retrieval

If you don't need the full Account object, skip retrieval for better performance:

```python
# Don't retrieve Account object
stream = await DomoStream.get_by_id(
    auth=auth,
    stream_id="stream-123",
    is_retrieve_account=False  # Skip Account retrieval
)

# Account metadata is still available
print(f"Account ID: {stream.account_id}")
print(f"Account Name: {stream.account_display_name}")

# Account object will be None
print(f"Account object: {stream.Account}")  # None
```

### Lazy Load Account

Retrieve the Account object later if needed:

```python
# Get stream without Account
stream = await DomoStream.get_by_id(
    auth=auth,
    stream_id="stream-123",
    is_retrieve_account=False
)

# Later, retrieve the Account when needed
account = await stream.get_account()

if account:
    print(f"Account: {account.name}")

    # Access account configuration
    if account.Config:
        print(f"Config: {account.Config.to_dict()}")
```

### Force Refresh Account

Refresh the Account object even if already loaded:

```python
stream = await DomoStream.get_by_id(
    auth=auth,
    stream_id="stream-123"
)

# Account is already loaded
print(f"Original Account: {stream.Account.name}")

# Force refresh the Account
account = await stream.get_account(force_refresh=True)
print(f"Refreshed Account: {account.name}")
```

### Working with Dataset Streams

Access stream account through a dataset:

```python
from domolibrary2.classes.DomoDataset import DomoDataset

# Get dataset
dataset = await DomoDataset.get_by_id(
    auth=auth,
    dataset_id="dataset-123"
)

# Access stream (auto-populated in __post_init__)
stream = dataset.Stream

# Manually refresh stream with Account
await stream.refresh()  # Refreshes stream data
account = await stream.get_account()

if account:
    print(f"Dataset '{dataset.name}' uses account '{account.name}'")
```

### Batch Processing with Accounts

Process multiple streams and their accounts:

```python
from domolibrary2.classes.DomoDataset import DomoDataset
from domolibrary2.classes.DomoDatacenter import DomoDatacenter

# Get all datasets
datacenter = DomoDatacenter(auth=auth)
datasets = await datacenter.search_datasets()

# Get streams with accounts
streams_with_accounts = []
for ds in datasets:
    if ds.stream_id:
        stream = await DomoStream.get_by_id(
            auth=auth,
            stream_id=ds.stream_id
        )
        if stream.Account:
            streams_with_accounts.append({
                'dataset_name': ds.name,
                'stream_id': stream.id,
                'account_name': stream.Account.name,
                'account_type': stream.Account.data_provider_type
            })

# Create DataFrame
import pandas as pd
df = pd.DataFrame(streams_with_accounts)
print(df)
```

### Account Information in Serialization

The `Account` object is excluded from `to_dict()`, but account metadata is included:

```python
stream = await DomoStream.get_by_id(auth=auth, stream_id="stream-123")

# to_dict() includes account metadata fields
stream_dict = stream.to_dict()
print(stream_dict)
# {
#     'id': 'stream-123',
#     'accountId': '456',  # ✓ Included
#     'accountDisplayName': 'My Account',  # ✓ Included
#     'accountUserid': 'user-789',  # ✓ Included
#     'dataProviderName': 'Snowflake',
#     ...
#     # Note: 'Account' object is NOT included
# }

# Access the full Account object separately
if stream.Account:
    account_dict = stream.Account.to_dict()
    print(account_dict)
```

## Error Handling

The Account retrieval is designed to be robust:

```python
stream = await DomoStream.get_by_id(
    auth=auth,
    stream_id="stream-123",
    debug_api=True  # Enable warnings
)

# If Account retrieval fails, stream retrieval continues
# A warning is printed if debug_api=True
# stream.Account will be None, but other stream data is intact
```

## API Reference

### DomoStream Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `account_id` | `str` | Account identifier |
| `account_display_name` | `str` | Human-readable account name |
| `account_userid` | `str` | User ID associated with account |
| `Account` | `DomoAccount \| None` | Full Account object (repr=False) |

### DomoStream.get_by_id()

```python
@classmethod
async def get_by_id(
    cls,
    auth: DomoAuth,
    stream_id: str,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient | None = None,
    is_retrieve_account: bool = True,  # ← New parameter
) -> DomoStream:
    """Get a stream by its ID.

    Args:
        auth: Authentication object
        stream_id: Unique stream identifier
        return_raw: Return raw response without processing
        debug_api: Enable API debugging
        session: HTTP client session
        is_retrieve_account: If True and account_id is present, retrieve full Account object

    Returns:
        DomoStream instance with Account populated (if available)
    """
```

### DomoStream.get_account()

```python
async def get_account(
    self,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    force_refresh: bool = False,
) -> DomoAccount | None:
    """Retrieve the Account associated with this stream.

    Args:
        session: HTTP client session
        debug_api: Enable API debugging
        force_refresh: If True, refresh even if Account is already set

    Returns:
        DomoAccount instance or None if no account_id
    """
```

## Benefits

1. **Consistent Pattern**: Follows the same composition pattern as other relationships
2. **Performance**: Skip Account retrieval when not needed
3. **Lazy Loading**: Retrieve Account on-demand
4. **Error Resilient**: Stream retrieval succeeds even if Account fetch fails
5. **Clean Serialization**: Account excluded from `to_dict()` but metadata included
6. **Type Safe**: Full type hints for IDE support

## Migration Guide

If you were previously accessing account information:

### Before
```python
stream = await DomoStream.get_by_id(auth=auth, stream_id="stream-123")

# Access only basic account info
print(f"Account ID: {stream.account_id}")
print(f"Account Name: {stream.account_display_name}")

# To get full account, you had to separately call:
# account = await DomoAccount.get_by_id(auth=auth, account_id=stream.account_id)
```

### After
```python
stream = await DomoStream.get_by_id(auth=auth, stream_id="stream-123")

# Basic account info still available
print(f"Account ID: {stream.account_id}")
print(f"Account Name: {stream.account_display_name}")

# Full account now automatically available
if stream.Account:
    print(f"Account Type: {stream.Account.data_provider_type}")
    print(f"Account Config: {stream.Account.Config.to_dict()}")
```

## Related Documentation

- [DomoAccount Documentation](./DomoAccount.md)
- [DomoStream Documentation](./DomoStream.md)
- [Composition Pattern Guide](./composition-pattern.md)
- [to_dict() Usage Guide](../TO_DICT_USAGE.md)
