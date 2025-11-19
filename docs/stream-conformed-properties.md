# Stream Configuration Conformed Properties

## Overview

The **Conformed Properties** feature provides a semantic layer over platform-specific stream configuration parameters. This allows you to access common configuration values (like SQL queries, database names, etc.) using consistent property names, regardless of the underlying data provider.

## Problem Solved

Different data providers use different parameter names for conceptually similar values:

- **Snowflake** uses `query` for SQL
- **Amazon Athena High Bandwidth** uses `enteredCustomQuery` for SQL
- **Snowflake Internal Unload** uses `customQuery` for SQL

Without conformed properties, you'd need provider-specific logic:

```python
# ❌ Without conformed properties - requires provider-specific logic
if stream.data_provider_key == "snowflake":
    sql = stream.typed_config.query
elif stream.data_provider_key == "amazon-athena-high-bandwidth":
    sql = stream.typed_config.query  # Different internal mapping
elif stream.data_provider_key == "snowflake-internal-unload":
    sql = stream.typed_config.query  # Yet another mapping
```

With conformed properties, access is consistent:

```python
# ✅ With conformed properties - works across all providers
sql = stream.sql  # Works for Snowflake, Athena, PostgreSQL, etc.
```

## Architecture

### 1. ConformedProperty Class

Defines a semantic property and maps it to provider-specific attribute names:

```python
from domolibrary2.classes.DomoDataset.stream_configs import ConformedProperty

query_property = ConformedProperty(
    name="query",
    description="SQL query or data selection statement",
    mappings={
        "snowflake": "query",
        "aws-athena": "query",
        "amazon-athena-high-bandwidth": "query",
        "snowflake-internal-unload": "query",  # Maps to customQuery internally
    }
)
```

### 2. CONFORMED_PROPERTIES Registry

Central registry of all conformed properties:

```python
from domolibrary2.classes.DomoDataset.stream_configs import CONFORMED_PROPERTIES

# Access a specific property
query_prop = CONFORMED_PROPERTIES["query"]

# List all properties
property_names = list(CONFORMED_PROPERTIES.keys())
# ['query', 'database', 'warehouse', 'table', 'report_id', ...]

# Check which providers support a property
snowflake_providers = query_prop.supported_providers
# ['snowflake', 'snowflakekeypairauthentication', 'aws-athena', ...]
```

### 3. DomoStream Properties

`DomoStream` provides `@property` methods for each conformed property:

```python
stream = await DomoStream.get_by_id(auth, stream_id)

# Access conformed properties
sql = stream.sql              # SQL query (cross-platform)
database = stream.database    # Database name (cross-platform)
warehouse = stream.warehouse  # Compute warehouse (Snowflake-specific)
```

## Available Conformed Properties

### SQL/Database Properties

| Property | Description | Supported Providers |
|----------|-------------|-------------------|
| `sql` | SQL query or data selection statement | Snowflake (all variants), AWS Athena, PostgreSQL |
| `database` | Database name or identifier | Snowflake, AWS Athena, PostgreSQL |
| `schema` | Database schema name | Snowflake (keypair auth), PostgreSQL |
| `warehouse` | Compute warehouse or resource pool | Snowflake (all variants) |
| `table` | Table name or identifier | AWS Athena, Snowflake Writeback |

### Cloud Storage Properties

| Property | Description | Supported Providers |
|----------|-------------|-------------------|
| `bucket` | S3 bucket or cloud storage location | Amazon S3 AssumeRole |
| `host` | Database host or server address | PostgreSQL, SharePoint Online |
| `port` | Database port number | PostgreSQL |

### Analytics/Reporting Properties

| Property | Description | Supported Providers |
|----------|-------------|-------------------|
| `report_id` | Report identifier (suite/survey ID) | Adobe Analytics, Qualtrics |
| `spreadsheet` | Spreadsheet identifier or file name | Google Sheets, Google Spreadsheets |

### Domo-Specific Properties

| Property | Description | Supported Providers |
|----------|-------------|-------------------|
| `dataset_id` | Source dataset ID (for dataset copy) or parent dataset ID | Dataset Copy, all streams |
| `file_url` | URL or path to data file | Domo CSV |

## Usage Examples

### Example 1: Cross-Platform SQL Access

```python
from domolibrary2.classes.DomoDataset.stream import DomoStream

# Works for Snowflake
snowflake_stream = await DomoStream.get_by_id(auth, snowflake_stream_id)
print(snowflake_stream.sql)  # "SELECT * FROM my_table"
print(snowflake_stream.database)  # "SA_PRD"
print(snowflake_stream.warehouse)  # "COMPUTE_WH"

# Works for AWS Athena
athena_stream = await DomoStream.get_by_id(auth, athena_stream_id)
print(athena_stream.sql)  # "SELECT * FROM logs"
print(athena_stream.database)  # "analytics_db"
print(athena_stream.warehouse)  # None (Athena doesn't use warehouses)
```

### Example 2: Provider-Agnostic Code

```python
async def get_stream_query(stream_id: str) -> str:
    """Get SQL query from a stream, regardless of provider type."""
    stream = await DomoStream.get_by_id(auth, stream_id)

    # Works for any SQL-based provider
    return stream.sql

# Works for Snowflake, Athena, PostgreSQL, etc.
query = await get_stream_query("stream-123")
```

### Example 3: Analytics Report ID

```python
# Adobe Analytics
adobe_stream = await DomoStream.get_by_id(auth, adobe_stream_id)
print(adobe_stream.report_id)  # "report_suite_12345"

# Qualtrics
qualtrics_stream = await DomoStream.get_by_id(auth, qualtrics_stream_id)
print(qualtrics_stream.report_id)  # "survey_67890"

# Google Sheets (uses different property)
sheets_stream = await DomoStream.get_by_id(auth, sheets_stream_id)
print(sheets_stream.spreadsheet)  # "1A2B3C4D5E6F7G8H9I"
```

### Example 4: Checking Property Availability

```python
stream = await DomoStream.get_by_id(auth, stream_id)

# Properties return None if not available for the provider
if stream.sql:
    print(f"SQL Query: {stream.sql}")
else:
    print("This stream doesn't use SQL queries")

if stream.warehouse:
    print(f"Warehouse: {stream.warehouse}")
else:
    print("This provider doesn't use warehouses")
```

## How It Works

### Step 1: Typed Config

Each stream has a `typed_config` that converts the list-based configuration to a typed object:

```python
stream = await DomoStream.get_by_id(auth, stream_id)

# Direct typed config access (provider-specific)
if stream.data_provider_key == "snowflake":
    config = stream.typed_config  # Snowflake_StreamConfig instance
    print(config.query)           # Type-safe access
    print(config.database_name)   # Provider-specific name
```

### Step 2: Conformed Property Lookup

Conformed properties use the registry to find the correct attribute:

```python
# Internal flow for stream.sql:
# 1. Get typed_config (Snowflake_StreamConfig instance)
# 2. Look up "query" in CONFORMED_PROPERTIES
# 3. Get mapping for "snowflake" provider → "query"
# 4. Return typed_config.query value
```

### Step 3: Fallback Behavior

Properties return `None` if not available:

```python
# Google Sheets stream doesn't have SQL
sheets_stream = await DomoStream.get_by_id(auth, sheets_stream_id)
print(sheets_stream.sql)  # None (not applicable)
print(sheets_stream.spreadsheet)  # "1A2B3C4D..." (available)
```

## Adding New Conformed Properties

To add a new conformed property:

### 1. Add to CONFORMED_PROPERTIES registry

Edit `src/domolibrary2/classes/DomoDataset/stream_configs/_conformed.py`:

```python
CONFORMED_PROPERTIES = {
    # ... existing properties ...

    "new_property": ConformedProperty(
        name="new_property",
        description="Description of what this property represents",
        mappings={
            "provider1": "attribute_name_1",
            "provider2": "attribute_name_2",
        }
    ),
}
```

### 2. Add property to DomoStream

Edit `src/domolibrary2/classes/DomoDataset/stream.py`:

```python
@property
def new_property(self) -> str | None:
    """Get new property from stream configuration (cross-platform).

    Works for: Provider1, Provider2

    Returns:
        Property value or None if not available
    """
    return self._get_conformed_value("new_property")
```

### 3. Document the property

Add to this documentation and update docstrings.

## Design Benefits

✅ **Consistent API**: Same property names work across all providers
✅ **Type Safety**: IDE autocomplete works for all properties
✅ **Maintainable**: Add new mappings in one place
✅ **Discoverable**: Properties are documented and easy to find
✅ **Backward Compatible**: Doesn't break existing `typed_config` access
✅ **Extensible**: Easy to add new properties and providers
✅ **Testable**: Clear separation of concerns makes testing simple

## Testing

Run tests to verify conformed properties:

```powershell
# Run conformed properties tests
python tests/classes/DomoDataset/test_51_StreamConformedProperties.py

# Run all stream config tests
pytest tests/classes/DomoDataset/ -k stream -v
```

## Related Documentation

- [Stream Configuration Redesign](../STREAM_CONFIG_REDESIGN.md) - Overall architecture
- [Register Pattern](design-patterns/register-pattern.md) - Decorator-based registry
- [Circular Import Resolution](circular-import-resolution-summary.md) - Import structure

## Future Enhancements

Potential improvements to consider:

1. **Validation**: Add validation to ensure mapped attributes exist on typed configs
2. **Enum-based access**: Provide `ConformedPropertyEnum` for structured access
3. **Auto-discovery**: Automatically discover common properties across providers
4. **Type hints**: Add specific return types based on property (int for port, etc.)
5. **Deprecation warnings**: Warn when accessing deprecated properties
