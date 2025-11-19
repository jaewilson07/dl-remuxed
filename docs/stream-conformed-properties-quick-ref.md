# Conformed Properties Quick Reference

## Quick Start

```python
from domolibrary2.classes.DomoDataset.stream import DomoStream

# Get any stream
stream = await DomoStream.get_by_id(auth, stream_id)

# Access properties (works across all providers)
stream.sql          # SQL query
stream.database     # Database name
stream.warehouse    # Compute warehouse (Snowflake)
stream.schema       # Schema name
stream.table        # Table name
stream.report_id    # Report/survey ID (analytics)
stream.spreadsheet  # Spreadsheet ID (Google)
stream.bucket       # S3 bucket
stream.host         # Host address
stream.port         # Port number
stream.dataset_id   # Source/parent dataset ID
stream.file_url     # File URL
```

## Property Reference

| Property | Returns | Providers |
|----------|---------|-----------|
| `sql` | SQL query string | Snowflake, AWS Athena, PostgreSQL (8 total) |
| `database` | Database name | Snowflake, AWS Athena, PostgreSQL (8 total) |
| `warehouse` | Warehouse name | Snowflake variants (5 total) |
| `schema` | Schema name | Snowflake (keypair), PostgreSQL (2 total) |
| `table` | Table name | AWS Athena, Snowflake Writeback (2 total) |
| `report_id` | Report suite/survey ID | Adobe Analytics, Qualtrics (2 total) |
| `spreadsheet` | Spreadsheet ID | Google Sheets, Google Spreadsheets (2 total) |
| `bucket` | S3 bucket name | Amazon S3 (2 total) |
| `host` | Host/server address | PostgreSQL, SharePoint (2 total) |
| `port` | Port number | PostgreSQL (1 total) |
| `dataset_id` | Dataset ID | Dataset Copy + all streams |
| `file_url` | File URL | Domo CSV (1 total) |

All properties return `str | None` (None if not applicable for the provider).

## Common Patterns

### Pattern 1: Cross-Platform Query Access
```python
# Works for Snowflake, Athena, PostgreSQL, etc.
async def get_query(stream_id: str) -> str:
    stream = await DomoStream.get_by_id(auth, stream_id)
    return stream.sql or "No query available"
```

### Pattern 2: Conditional Logic
```python
stream = await DomoStream.get_by_id(auth, stream_id)

if stream.sql:
    # SQL-based connector
    print(f"Database: {stream.database}")
    print(f"Query: {stream.sql[:100]}...")

elif stream.report_id:
    # Analytics connector
    print(f"Report: {stream.report_id}")

elif stream.spreadsheet:
    # Spreadsheet connector
    print(f"Sheet: {stream.spreadsheet}")
```

### Pattern 3: Property Inspection
```python
from domolibrary2.classes.DomoDataset.stream_configs import CONFORMED_PROPERTIES

# Check if a provider supports a property
query_prop = CONFORMED_PROPERTIES["query"]
if "snowflake" in query_prop.supported_providers:
    print("Snowflake supports SQL queries")

# List all providers that support SQL
for provider in query_prop.supported_providers:
    print(f"  - {provider}")
```

## Provider Support Matrix

### SQL Properties
- ✅ Snowflake (all 7 variants)
- ✅ AWS Athena (2 variants)
- ✅ PostgreSQL
- ❌ Google Sheets
- ❌ Adobe Analytics
- ❌ Qualtrics

### Warehouse Property (Snowflake Only)
- ✅ Snowflake (5 variants)
- ❌ All other providers

### Report ID Property
- ✅ Adobe Analytics V2
- ✅ Qualtrics
- ❌ All other providers

### Spreadsheet Property
- ✅ Google Sheets
- ✅ Google Spreadsheets
- ❌ All other providers

## Implementation Details

### Registry
```python
from domolibrary2.classes.DomoDataset.stream_configs import CONFORMED_PROPERTIES

# Get a property definition
query_prop = CONFORMED_PROPERTIES["query"]

# Check mappings
attr_name = query_prop.get_key_for_provider("snowflake")
# Returns: "query"

# List supported providers
providers = query_prop.supported_providers
# Returns: ['snowflake', 'aws-athena', ...]
```

### How It Works
1. `stream.sql` calls `_get_conformed_value("query")`
2. Looks up "query" in `CONFORMED_PROPERTIES`
3. Gets mapping for current provider (e.g., "snowflake" → "query")
4. Returns `stream.typed_config.query`

### Adding New Properties
See `docs/stream-conformed-properties.md` for full guide.

Quick steps:
1. Add to `CONFORMED_PROPERTIES` in `_conformed.py`
2. Add `@property` method to `DomoStream` in `stream.py`
3. Update documentation

## Testing

```powershell
# Run conformed properties tests
python tests/classes/DomoDataset/test_51_StreamConformedProperties.py

# Run example
python examples/stream_conformed_properties_example.py
```

## Documentation

- **Full Guide**: `docs/stream-conformed-properties.md`
- **Examples**: `examples/stream_conformed_properties_example.py`
- **Tests**: `tests/classes/DomoDataset/test_51_StreamConformedProperties.py`
- **Implementation**: `src/domolibrary2/classes/DomoDataset/stream_configs/_conformed.py`

## Benefits

✅ **No more provider-specific logic** - Same code works everywhere
✅ **Type-safe** - IDE autocomplete works
✅ **Discoverable** - Just type `stream.` and explore
✅ **Pythonic** - Properties return None when not applicable
✅ **Backward compatible** - Existing code continues to work

## Comparison

### Before (Provider-Specific)
```python
if stream.data_provider_key == "snowflake":
    query = stream.typed_config.query
elif stream.data_provider_key == "amazon-athena-high-bandwidth":
    query = stream.typed_config.query
# ... more conditions
```

### After (Cross-Platform)
```python
query = stream.sql  # Works for all SQL providers
```
