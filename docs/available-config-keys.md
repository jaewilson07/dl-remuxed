# _available_config_keys: Discover Configuration Gaps

## Overview

`_available_config_keys` helps identify configuration parameters that exist in `typed_config` but are **not yet mapped** to conformed properties. This is essential for extending conformed properties coverage as you add more schemas.

## Problem Solved

### Before
- No way to know which config keys exist but aren't mapped
- Manual inspection required to find unmapped parameters
- Easy to miss important configuration options when creating conformed properties

### After
- Automatic discovery of unmapped keys
- Easy gap identification
- Helps prioritize which properties to add next

## Usage

```python
>>> stream = await DomoStream.get_by_id(auth, stream_id)
>>> stream._available_config_keys
['role', 'authenticator', 'private_key_path', 'timeout_seconds']
# These keys exist in typed_config but aren't mapped to conformed properties yet
```

## How It Works

1. **Get all keys** from `typed_config` (excluding private/callable)
2. **Get mapped keys** from `CONFORMED_PROPERTIES` for this provider
3. **Return difference** - keys that exist but aren't mapped

```python
typed_config_keys = ['query', 'database_name', 'warehouse', 'role', 'authenticator']
mapped_keys = ['query', 'database_name', 'warehouse']  # From CONFORMED_PROPERTIES
available_config_keys = ['role', 'authenticator']  # The difference
```

## Workflow for Extending Conformed Properties

###1. Discover Unmapped Keys

```python
>>> stream = await DomoStream.get_by_id(auth, snowflake_stream_id)
>>> stream._available_config_keys
['role', 'authenticator', 'cloud_provider']
```

### 2. Check If Common Across Providers

```python
# Check multiple streams from different providers
streams_by_provider = {
    "snowflake": snowflake_stream,
    "postgresql": postgres_stream,
    "aws-athena": athena_stream,
}

for provider, stream in streams_by_provider.items():
    print(f"{provider}: {stream._available_config_keys}")

# Output:
# snowflake: ['role', 'authenticator', 'cloud_provider']
# postgresql: ['role', 'ssl_mode', 'connection_timeout']
# aws-athena: ['workgroup', 'output_location']

# 'role' appears in multiple providers → good candidate for conformed property!
```

### 3. Add to CONFORMED_PROPERTIES

```python
# In _conformed.py
CONFORMED_PROPERTIES = {
    # ... existing properties ...

    "role": ConformedProperty(
        name="role",
        description="Database role or user role",
        mappings={
            "snowflake": "role",
            "snowflakekeypairauthentication": "role",
            "postgresql": "role",
        },
        is_repr=False,  # Security - don't show in repr
    ),
}
```

### 4. Add Property to DomoStream

```python
@property
def role(self) -> str | None:
    """Get database role from stream configuration.

    Works for databases that support role-based access control.

    Returns:
        Role name or None
    """
    return self._get_conformed_value("role")
```

### 5. Verify - Key Disappears from _available_config_keys

```python
>>> stream._available_config_keys
['authenticator', 'cloud_provider']  # 'role' no longer appears!
```

## Examples

### Example 1: Snowflake Stream

```python
>>> snowflake_stream._available_config_keys
['role', 'authenticator', 'private_key_path', 'timeout_seconds']

# These are Snowflake-specific keys that could be added to conformed properties
# if they're common across multiple database providers
```

### Example 2: Google Sheets Stream

```python
>>> sheets_stream._available_config_keys
['sheet_name', 'range', 'first_row_headers']

# These are specific to spreadsheets - probably NOT good candidates
# for conformed properties (too specific to one provider type)
```

### Example 3: After Adding Mappings

```python
# Before: 5 unmapped keys
>>> stream._available_config_keys
['role', 'authenticator', 'ssl_mode', 'timeout', 'retries']

# Add 'role' and 'ssl_mode' to CONFORMED_PROPERTIES...

# After: Only 3 unmapped keys remain
>>> stream._available_config_keys
['authenticator', 'timeout', 'retries']
```

## Decision Matrix: Should You Add a Conformed Property?

| Criteria | Yes - Add It | No - Skip It |
|----------|-------------|--------------|
| **Used by multiple providers?** | ✅ 3+ providers | ❌ Only 1 provider |
| **Semantic meaning?** | ✅ Clear purpose | ❌ Provider-specific jargon |
| **User-facing?** | ✅ Users need access | ❌ Internal only |
| **Stable?** | ✅ Won't change | ❌ Experimental/beta |

**Good Candidates:**
- `role` - Used by Snowflake, PostgreSQL, Redshift
- `timeout` - Used by most database connectors
- `ssl_mode` - Used by many database connectors
- `batch_size` - Used by many connectors

**Poor Candidates:**
- `snowflake_edition` - Too Snowflake-specific
- `google_oauth_refresh_token` - Too Google-specific
- `_internal_config_version` - Internal implementation detail

## Helper Function

```python
from domolibrary2.classes.DomoDataset.stream_configs import get_available_config_keys

# Use directly on any stream-like object
available = get_available_config_keys(stream)
```

## Comparison with _missing_mappings

### _missing_mappings
**Shows:** Conformed properties that DON'T support this provider
```python
>>> stream._missing_mappings
['report_id', 'spreadsheet']  # These are defined but not applicable
```
**Use case:** Understanding why a property returns None

### _available_config_keys
**Shows:** Config keys that AREN'T mapped to conformed properties
```python
>>> stream._available_config_keys
['role', 'authenticator']  # These exist but aren't exposed
```
**Use case:** Finding gaps to extend conformed properties

## Real-World Workflow

### Scenario: Adding More Database Properties

```python
# Step 1: Survey multiple database streams
db_streams = [
    await DomoStream.get_by_id(auth, snowflake_id),
    await DomoStream.get_by_id(auth, postgres_id),
    await DomoStream.get_by_id(auth, redshift_id),
]

# Step 2: Collect all unmapped keys
all_unmapped = {}
for stream in db_streams:
    provider = stream.data_provider_key
    keys = stream._available_config_keys
    all_unmapped[provider] = keys
    print(f"{provider}: {keys}")

# Output:
# snowflake: ['role', 'authenticator', 'timeout']
# postgresql: ['role', 'ssl_mode', 'connection_timeout']
# redshift: ['role', 'ssl', 'max_connections']

# Step 3: Find common keys
from collections import Counter
all_keys = [key for keys in all_unmapped.values() for key in keys]
common_keys = [k for k, count in Counter(all_keys).items() if count >= 2]
print(f"Common keys: {common_keys}")
# ['role']  # Appears in all 3

# Step 4: Add 'role' to CONFORMED_PROPERTIES
# Step 5: Re-run - 'role' no longer appears in any _available_config_keys!
```

## Benefits

### 1. Discover Gaps ✅
- Automatically find unmapped configuration keys
- No manual inspection required
- Works across all provider types

### 2. Prioritize Work ✅
- See which keys are most common
- Focus on high-value properties first
- Avoid one-off, provider-specific keys

### 3. Validate Coverage ✅
- Empty list means full coverage
- Easy to track progress
- Know when you're "done"

### 4. Documentation ✅
- Self-documenting what's unmapped
- Helps new contributors understand gaps
- Makes conformed properties discoverable

## Implementation Details

```python
def get_available_config_keys(stream_obj: Any) -> list[str]:
    """Get list of typed_config keys that are NOT mapped to conformed properties."""

    # Get all non-private, non-callable attributes from typed_config
    all_keys = [attr for attr in dir(typed_config)
                if not attr.startswith("_")
                and not callable(getattr(typed_config, attr))]

    # Get mapped keys for this provider
    mapped_keys = set()
    for conf_prop in CONFORMED_PROPERTIES.values():
        key = conf_prop.get_key_for_provider(provider_key)
        if key:
            mapped_keys.add(key)

    # Return keys that aren't mapped
    return [key for key in all_keys if key not in mapped_keys]
```

## Testing

```bash
# Run tests
python tests/classes/DomoDataset/test_54_AvailableConfigKeys.py

# All tests pass:
✅ get_available_config_keys function works
✅ _available_config_keys property works
✅ Identifies gaps correctly
✅ Empty when all keys mapped
✅ Different providers show different keys
```

## Tips

### Tip 1: Batch Processing

```python
# Process multiple streams at once
async def survey_streams(auth, stream_ids):
    results = {}
    for stream_id in stream_ids:
        stream = await DomoStream.get_by_id(auth, stream_id)
        provider = stream.data_provider_key
        keys = stream._available_config_keys

        if provider not in results:
            results[provider] = set()
        results[provider].update(keys)

    return results

# Usage
unmapped_by_provider = await survey_streams(auth, all_stream_ids)
for provider, keys in unmapped_by_provider.items():
    print(f"{provider}: {sorted(keys)}")
```

### Tip 2: Export to CSV

```python
import csv

# Export for analysis
with open('unmapped_keys.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Provider', 'Unmapped Key'])

    for provider, stream in streams.items():
        for key in stream._available_config_keys:
            writer.writerow([provider, key])
```

### Tip 3: Track Progress

```python
# Before adding properties
initial_unmapped = {
    provider: len(stream._available_config_keys)
    for provider, stream in streams.items()
}

# Add some conformed properties...

# After
final_unmapped = {
    provider: len(stream._available_config_keys)
    for provider, stream in streams.items()
}

# Report progress
for provider in initial_unmapped:
    before = initial_unmapped[provider]
    after = final_unmapped[provider]
    reduction = before - after
    print(f"{provider}: {before} → {after} ({reduction} mapped)")
```

## Conclusion

`_available_config_keys` is an essential tool for:
- ✅ Discovering configuration gaps
- ✅ Extending conformed properties coverage
- ✅ Understanding provider capabilities
- ✅ Prioritizing development work

Use it whenever you're adding new schemas or extending conformed properties support!
