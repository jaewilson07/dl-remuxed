# to_dict() Usage Guide

## Overview

The `to_dict()` method on all Domo entities now properly filters fields and supports both camelCase and snake_case output formats.

## Key Features

### 1. Field Filtering
- **Includes**: Only fields with `repr=True` and non-None values
- **Excludes**: Fields marked with `repr=False` (auth, raw, lineage, data, schema, stream, tags, pdp, certification)
- **Always includes**: Properties listed in `__serialize_properties__` (even if None)

### 2. Property Serialization
Classes can define `__serialize_properties__` to include computed properties:

```python
from typing import ClassVar

@dataclass
class DomoDataset(DomoEntity):
    __serialize_properties__: ClassVar[tuple] = ("display_url", "transport_type")

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/datasources/{self.id}"

    @property
    def transport_type(self):
        return self.raw.get("transportType", "").upper()
```

### 3. Case Format Options

#### Default: camelCase (for JavaScript/API compatibility)
```python
ds = DomoDataset.get_by_id(auth=auth, dataset_id="abc-123")
result = ds.to_dict()
# {
#     'id': 'abc-123',
#     'name': 'My Dataset',
#     'dataProviderType': 'snowflake',
#     'transportType': 'CLOUD',
#     'displayUrl': 'https://...',
#     'rowCount': 1000,
#     'columnCount': 5
# }
```

#### snake_case (for Python/DataFrame compatibility)
```python
ds = DomoDataset.get_by_id(auth=auth, dataset_id="abc-123")
result = ds.to_dict(return_snake_case=True)
# {
#     'id': 'abc-123',
#     'name': 'My Dataset',
#     'data_provider_type': 'snowflake',
#     'transport_type': 'CLOUD',
#     'display_url': 'https://...',
#     'row_count': 1000,
#     'column_count': 5
# }
```

## Common Use Cases

### Creating DataFrames

```python
import pandas as pd
from domolibrary2.classes.DomoDataset import DomoDataset

# Get datasets
datasets = await datacenter.search_datasets()

# Option 1: camelCase columns
df = pd.DataFrame([ds.to_dict() for ds in datasets])
print(df[['id', 'name', 'transportType', 'displayUrl']])

# Option 2: snake_case columns (more Pythonic)
df = pd.DataFrame([ds.to_dict(return_snake_case=True) for ds in datasets])
print(df[['id', 'name', 'transport_type', 'display_url']])
```

### Filtering by Transport Type

```python
# Get all datasets
datasets = await datacenter.search_datasets()

# Convert to DataFrame with snake_case
df = pd.DataFrame([ds.to_dict(return_snake_case=True) for ds in datasets])

# Filter by transport type
cloud_datasets = df[df['transport_type'] == 'CLOUD']
api_datasets = df[df['transport_type'] == 'API']
connector_datasets = df[df['transport_type'] == 'CONNECTOR']
```

### Exporting to JSON

```python
import json

# camelCase for API/JavaScript consumption
datasets_dict = [ds.to_dict() for ds in datasets]
with open('datasets.json', 'w') as f:
    json.dump(datasets_dict, f, indent=2, default=str)

# snake_case for Python processing
datasets_dict = [ds.to_dict(return_snake_case=True) for ds in datasets]
with open('datasets_snake.json', 'w') as f:
    json.dump(datasets_dict, f, indent=2, default=str)
```

## Excluded Fields

The following fields are **never** included in `to_dict()` output (marked with `repr=False`):

- `auth` - Authentication object (sensitive)
- `raw` - Raw API response (verbose, already represented in other fields)
- `lineage` - Lineage tracking object (use dedicated lineage methods)
- `Relations` - Relationship controller (use dedicated relationship methods)
- `Data` - Data subentity (use `dataset.Data` methods)
- `Schema` - Schema subentity (use `dataset.Schema` methods)
- `Stream` - Stream subentity (use `dataset.Stream` methods)
- `Tags` - Tags subentity (use `dataset.Tags` methods)
- `PDP` - PDP policies subentity (use `dataset.PDP` methods)
- `Certification` - Certification subentity (use `dataset.Certification` methods)

## Custom Override

You can provide a custom function to completely override the default behavior:

```python
def custom_serializer(entity):
    return {
        'dataset_id': entity.id,
        'dataset_name': entity.name,
        'full_url': entity.display_url
    }

result = ds.to_dict(override_fn=custom_serializer)
# {'dataset_id': 'abc-123', 'dataset_name': 'My Dataset', 'full_url': 'https://...'}
```

## Migration Guide

If you were previously using the old `to_dict()` behavior:

### Before (old behavior)
```python
# Returned ALL fields including auth, raw, data, schema, etc.
result = ds.to_dict()
# Had to manually filter unwanted fields
```

### After (new behavior)
```python
# Automatically excludes repr=False fields
result = ds.to_dict()  # Clean, serializable output

# Choose your preferred case format
result_camel = ds.to_dict()  # camelCase (default)
result_snake = ds.to_dict(return_snake_case=True)  # snake_case
```

## Benefits

1. **Cleaner Output**: No more nested objects or sensitive data in serialized form
2. **DataFrame Ready**: Direct conversion to pandas DataFrames without cleanup
3. **Consistent Columns**: `__serialize_properties__` ensures computed properties are always included
4. **Format Flexibility**: Choose camelCase or snake_case based on your needs
5. **Performance**: Only serializes necessary fields
