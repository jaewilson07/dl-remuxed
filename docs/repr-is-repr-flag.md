# is_repr Flag and _missing_mappings Enhancement

## Overview

Enhanced the custom `__repr__` implementation with two new features:
1. **`is_repr` flag** - Control which properties appear in repr
2. **`_missing_mappings` property** - Discover which properties aren't supported by a provider

## Problem Solved

### Before
- All conformed properties appeared in repr (12 properties)
- Sensitive data (host, port) shown in repr
- No way to know which properties aren't applicable for a provider

### After
- Only important properties appear in repr (7 properties with `is_repr=True`)
- Sensitive properties excluded by default
- `_missing_mappings` shows unsupported properties

## 1. is_repr Flag

### Configuration

Each `ConformedProperty` now has an `is_repr` flag:

```python
CONFORMED_PROPERTIES = {
    "query": ConformedProperty(
        name="query",
        description="SQL query",
        mappings={...},
        is_repr=True,  # ✅ Show in repr
    ),
    "host": ConformedProperty(
        name="host",
        description="Database host",
        mappings={...},
        is_repr=False,  # ❌ Don't show in repr (security)
    ),
}
```

### Properties with is_repr=True (7 total)
✅ **Shown in repr:**
- `query` - SQL query (most important)
- `database` - Database name
- `schema` - Schema name
- `warehouse` - Compute warehouse
- `table` - Table name
- `report_id` - Report/survey ID
- `spreadsheet` - Spreadsheet ID

### Properties with is_repr=False (5 total)
❌ **Hidden from repr:**
- `bucket` - S3 bucket (not usually interesting)
- `dataset_id` - Dataset ID (shown via parent anyway)
- `file_url` - File URL (usually too long)
- `host` - Host address (security concern)
- `port` - Port number (not usually interesting)

### Example Output

**Snowflake Stream:**
```python
>>> stream
DomoStream(id='abc123', provider='snowflake',
           sql='SELECT * FROM customers',
           database='SA_PRD',
           warehouse='COMPUTE_WH')
# ✅ Shows important properties only
# ❌ Doesn't show host/port (security)
```

**Google Sheets Stream:**
```python
>>> stream
DomoStream(id='def456', provider='google-sheets',
           spreadsheet='1A2B3C4D5E6F7G8H9I')
# ✅ Shows relevant property for this provider
# ❌ Doesn't show SQL properties (not applicable)
```

## 2. _missing_mappings Property

### Purpose

Discover which conformed properties aren't supported by a stream's provider:

```python
>>> stream.data_provider_key = "snowflake"
>>> stream._missing_mappings
['schema', 'table', 'report_id', 'spreadsheet']
# These properties don't have mappings for Snowflake
```

### Use Cases

**1. Debugging**
```python
# Why doesn't my stream have a schema property?
>>> stream.schema
None
>>> stream._missing_mappings
['schema', 'report_id', 'spreadsheet']
# Ah, 'schema' isn't supported for 'snowflake' provider
```

**2. Provider Capability Discovery**
```python
# What properties does this provider NOT support?
>>> google_sheets_stream._missing_mappings
['query', 'database', 'schema', 'warehouse', 'table', 'report_id']
# Google Sheets doesn't support SQL properties
```

**3. Validation**
```python
# Check if a property is applicable before using it
if "query" not in stream._missing_mappings:
    print(f"SQL: {stream.sql}")
else:
    print("This provider doesn't use SQL")
```

### Implementation

```python
@property
def _missing_mappings(self) -> list[str]:
    """Get list of conformed properties without mappings for this provider.

    Returns only properties where is_repr=True.

    Returns:
        List of property names that don't support this provider
    """
    from .stream_configs._repr import get_missing_mappings
    return get_missing_mappings(self)
```

### Helper Function

```python
from domolibrary2.classes.DomoDataset.stream_configs import get_missing_mappings

# Get missing mappings for any stream-like object
missing = get_missing_mappings(stream)
# ['report_id', 'spreadsheet']
```

## Examples by Provider

### Snowflake
```python
>>> snowflake_stream._missing_mappings
['schema', 'table', 'report_id', 'spreadsheet']

>>> repr(snowflake_stream)
DomoStream(id='...', provider='snowflake',
           sql='SELECT...', database='SA_PRD', warehouse='COMPUTE_WH')
# ✅ Shows: query, database, warehouse
# ❌ Missing: schema (not in 'snowflake' mappings), table, report_id, spreadsheet
```

### Google Sheets
```python
>>> sheets_stream._missing_mappings
['query', 'database', 'schema', 'warehouse', 'table', 'report_id']

>>> repr(sheets_stream)
DomoStream(id='...', provider='google-sheets',
           spreadsheet='1A2B3C4D5E')
# ✅ Shows: spreadsheet
# ❌ Missing: all SQL properties (not applicable)
```

### Adobe Analytics
```python
>>> adobe_stream._missing_mappings
['query', 'database', 'schema', 'warehouse', 'table', 'spreadsheet']

>>> repr(adobe_stream)
DomoStream(id='...', provider='adobe-analytics-v2',
           report_id='report_suite_123')
# ✅ Shows: report_id
# ❌ Missing: SQL and spreadsheet properties
```

## Optional: Show Missing Mappings in Repr

```python
from domolibrary2.classes.DomoDataset.stream_configs import create_stream_repr

# Include missing mappings count in repr
custom_repr = create_stream_repr(stream, include_missing_mappings=True)
# DomoStream(..., _missing_mappings=4)
```

## Benefits

### 1. Security
- ✅ Host/port no longer shown in logs
- ✅ Sensitive URLs excluded from repr
- ✅ Only business-relevant properties shown

### 2. Clarity
- ✅ Repr is shorter and clearer
- ✅ Only shows properties that matter
- ✅ Less noise in debug output

### 3. Discoverability
- ✅ `_missing_mappings` makes limitations clear
- ✅ Easy to understand provider capabilities
- ✅ Helpful for debugging None values

### 4. Maintainability
- ✅ Single source of truth (`is_repr` flag)
- ✅ Easy to add/remove properties from repr
- ✅ No code changes to DomoStream class

## Configuration Guide

### Adding a New Property to Repr

```python
"new_property": ConformedProperty(
    name="new_property",
    description="...",
    mappings={...},
    is_repr=True,  # ✅ Show in repr
)
```

### Excluding a Property from Repr

```python
"sensitive_property": ConformedProperty(
    name="sensitive_property",
    description="...",
    mappings={...},
    is_repr=False,  # ❌ Don't show in repr
)
```

### Changing an Existing Property

```python
# Change from is_repr=False to True
"bucket": ConformedProperty(
    name="bucket",
    description="S3 bucket",
    mappings={...},
    is_repr=True,  # Now shows in repr
)
```

## Testing

```bash
# Run tests
python tests/classes/DomoDataset/test_53_ReprFlags.py

# All tests pass:
✓ is_repr flags configured correctly
✓ get_missing_mappings works
✓ Repr respects is_repr flag
✓ include_missing_mappings parameter works
✓ _missing_mappings property works
```

## Comparison

### Before (All Properties in Repr)
```python
DomoStream(id='123', provider='snowflake',
           sql='SELECT...', database='SA_PRD', warehouse='COMPUTE_WH',
           host='db.example.com', port='5432', dataset_id='456', ...)
# 🔴 Too long, includes sensitive data
```

### After (Only is_repr=True Properties)
```python
DomoStream(id='123', provider='snowflake',
           sql='SELECT...', database='SA_PRD', warehouse='COMPUTE_WH')
# ✅ Concise, no sensitive data, clear and useful
```

## Implementation Summary

**Files Modified:**
1. `stream_configs/_conformed.py` - Added `is_repr` field, updated all properties
2. `stream_configs/_repr.py` - Added `get_missing_mappings()`, updated `create_stream_repr()`
3. `stream.py` - Added `_missing_mappings` property
4. `stream_configs/__init__.py` - Export `get_missing_mappings`

**Tests:**
5. `tests/test_53_ReprFlags.py` - All tests passing

**Properties Updated:**
- 7 properties: `is_repr=True` (shown in repr)
- 5 properties: `is_repr=False` (hidden from repr)

## Backward Compatibility

✅ **Fully backward compatible**
- Existing code continues to work
- Default behavior unchanged (properties still accessible)
- Only repr output changes (improvement, not breaking change)
- `_missing_mappings` is new (additive)

## Recommendation

**✅ Use this enhancement** because:
1. **Better security** - Sensitive data not in logs
2. **Clearer output** - Repr is concise and meaningful
3. **Better debugging** - `_missing_mappings` explains None values
4. **No breaking changes** - Fully backward compatible

This makes DomoStream repr **even better** while adding powerful debugging capabilities!
