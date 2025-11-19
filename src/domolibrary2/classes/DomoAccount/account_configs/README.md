# DomoAccount Configuration Classes

> Last updated: 2025-11-19

This directory contains account configuration classes for various Domo connectors and data providers. These classes handle serialization/deserialization of account credentials and settings for different data sources.

## Overview

All account configuration classes inherit from `DomoAccount_Config` (defined in `_base.py`) and provide a consistent interface for:
- Converting API responses to Python objects (`from_dict`)
- Converting Python objects back to API format (`to_dict`)
- Validating serialization consistency
- Managing field mappings between API keys and Python attributes

## Recent Changes (November 2025)

### Major Refactoring
**Removed 18 custom `from_dict()` implementations** in favor of using the base class method with declarative `_field_map` and `_fields_for_serialization` attributes.

**Benefits:**
- Reduced code duplication (~180 lines removed)
- Consistent behavior across all config classes
- Centralized mapping logic in base class
- Easier to maintain and extend

### Bug Fix: `_field_map` Extraction
Fixed a critical bug where `_field_map` was not being properly extracted from dataclass field's `default_factory`. This caused mappings like `passPhrase` → `passphrase` to fail, resulting in incorrect attribute names like `pass_phrase`.

**Solution:** Modified `DomoAccount_Config.from_dict()` to properly call `default_factory()` when accessing `_field_map` from the class definition.

## How to Use DomoAccount_Config

### Basic Configuration Class

For simple configurations where API keys follow standard camelCase → snake_case conversion:

```python
from dataclasses import dataclass, field
from ._base import DomoAccount_Config
from ..config import register_account_config

@register_account_config("my-connector")
@dataclass
class DomoAccount_Config_MyConnector(DomoAccount_Config):
    data_provider_type: str = "my-connector"
    is_oauth: bool = False

    # Define your attributes (snake_case)
    username: str = None
    password: str = field(repr=False, default=None)
    account: str = None

    # List Python attribute names (not API keys)
    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "username",
            "password",
            "account",
        ]
    )
```

**API Response:**
```json
{
    "username": "user@example.com",
    "password": "secret",
    "account": "myaccount",
    "allowExternalUse": "true"
}
```

**Usage:**
```python
config = DomoAccount_Config_MyConnector.from_dict(api_response)
# config.username == "user@example.com"
# config.password == "secret"

api_dict = config.to_dict()
# Returns: {"username": "user@example.com", "password": "secret",
#           "account": "myaccount", "allowExternalUse": true}
```

### Configuration with Custom Field Mappings

When API keys don't follow standard camelCase or need special mapping, use `_field_map`:

```python
@register_account_config("snowflake-keypair")
@dataclass
class DomoAccount_Config_SnowflakeKeyPair(DomoAccount_Config):
    data_provider_type: str = "snowflake-keypair"
    is_oauth: bool = False

    private_key: str = field(repr=False, default=None)
    account: str = None
    passphrase: str = field(repr=False, default=None)  # Note: NOT pass_phrase
    username: str = None

    # Map API keys to Python attributes
    _field_map: dict = field(
        default_factory=lambda: {
            "passPhrase": "passphrase",  # API key -> Python attribute
        },
        repr=False,
        init=False,
    )

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "private_key",
            "account",
            "username",
            "passphrase",
        ]
    )
```

**API Response:**
```json
{
    "privateKey": "-----BEGIN PRIVATE KEY-----...",
    "account": "myaccount",
    "passPhrase": "my-secret-passphrase",
    "username": "user",
    "allowExternalUse": "false"
}
```

**How it works:**
1. `from_dict()` sees `passPhrase` in API response
2. Looks up in `_field_map`: `{"passPhrase": "passphrase"}`
3. Sets `config.passphrase = "my-secret-passphrase"` (NOT `pass_phrase`)
4. `to_dict()` reverses the mapping back to `passPhrase`

### Configuration with Custom Logic

For configs that need custom initialization or transformation:

```python
@register_account_config("amazon-s3")
@dataclass
class DomoAccount_Config_AmazonS3(DomoAccount_Config):
    data_provider_type: str = "amazon-s3"
    is_oauth: bool = False

    access_key: str = None
    secret_key: str = field(repr=False, default=None)
    bucket: str = None
    region: str = "us-west-2"

    def __post_init__(self):
        # Custom logic: clean s3:// prefix from bucket
        self.bucket = self._clean_bucket()
        super().__post_init__()  # IMPORTANT: Call parent's __post_init__

    _fields_for_serialization: list[str] = field(
        default_factory=lambda: [
            "access_key",
            "secret_key",
            "bucket",
            "region",
        ]
    )

    def _clean_bucket(self):
        bucket = self.bucket
        if bucket and bucket.lower().startswith("s3://"):
            bucket = bucket[5:]
        return bucket
```

**Note:** Always call `super().__post_init__()` to ensure validation runs.

## Key Concepts

### `_fields_for_serialization`
- **Required** for all configs
- Lists Python attribute names (snake_case) to include in `to_dict()` output
- Base class automatically converts to camelCase (or uses `_field_map`)
- Excludes internal fields like `raw`, `parent`, `_field_map`

### `_field_map`
- **Optional** - only needed for non-standard mappings
- Maps API keys (camelCase) to Python attributes (snake_case)
- Used bidirectionally: `from_dict()` and `to_dict()`
- Common use cases:
  - Non-standard casing: `passPhrase` → `passphrase`
  - Different names: `user` → `username`, `apikey` → `access_token`
  - Prefixes: `awsAccessKey` → `access_key`, `s3StagingDir` → `bucket`

### Automatic Conversions
The base class automatically handles:
- **camelCase ↔ snake_case**: `accessKey` ↔ `access_key`
- **allowExternalUse**: Always included in `to_dict()` output
- **Optional fields**: Fields with `None` values are excluded from `to_dict()`
- **Validation**: Compares `to_dict()` output with original API response

## Common Patterns

### Pattern 1: Simple Credentials
```python
_fields_for_serialization: list[str] = field(
    default_factory=lambda: ["username", "password", "account"]
)
```

### Pattern 2: AWS-style Keys
```python
_field_map: dict = field(
    default_factory=lambda: {
        "awsAccessKey": "access_key",
        "awsSecretKey": "secret_key",
    }
)
_fields_for_serialization: list[str] = field(
    default_factory=lambda: ["access_key", "secret_key", "bucket", "region"]
)
```

### Pattern 3: Non-standard Naming
```python
_field_map: dict = field(
    default_factory=lambda: {
        "instance": "domo_instance",
        "accessToken": "access_token",
        "apikey": "access_token",
        "customer": "domo_instance",
        "user": "username",
    }
)
```

## Files in This Directory

- **`_base.py`**: Base class with `from_dict()`, `to_dict()`, and validation logic
- **`snowflake.py`**: Snowflake connector configurations (10 variants)
- **`aws.py`**: AWS connector configurations (S3, Athena, etc.)
- **`domo.py`**: Domo-specific configurations (dataset copy, governance, etc.)
- **`__init__.py`**: Re-exports base class and error classes

## Migration Guide

If you're creating a new config class or updating an old one:

### Old Pattern (Before Refactoring)
```python
@classmethod
def from_dict(cls, obj: dict, parent: Any = None, **kwargs):
    return cls(
        access_key=obj["accessKey"],
        secret_key=obj["secretKey"],
        bucket=obj["bucket"],
        parent=parent,
        raw=obj,
    )
```

### New Pattern (After Refactoring)
```python
# Just define _fields_for_serialization - that's it!
_fields_for_serialization: list[str] = field(
    default_factory=lambda: ["access_key", "secret_key", "bucket"]
)
# No custom from_dict needed - base class handles it!
```

### When You Need `_field_map`
If API keys don't follow camelCase pattern or need custom mapping:
```python
_field_map: dict = field(
    default_factory=lambda: {
        "awsAccessKey": "access_key",  # Non-standard prefix
        "passPhrase": "passphrase",     # Non-standard casing
        "user": "username",             # Different name
    },
    repr=False,
    init=False,
)
```

## Troubleshooting

### Error: "unexpected keyword argument 'xxx_yyy'"
**Problem:** API key being converted to snake_case with underscores (e.g., `pass_phrase` instead of `passphrase`)

**Solution:** Add a `_field_map` entry:
```python
_field_map: dict = field(
    default_factory=lambda: {
        "passPhrase": "passphrase",  # Map API key to correct Python attribute
    }
)
```

### Error: "Serialization mismatch"
**Problem:** `to_dict()` output doesn't match original API response keys

**Solution:** Check that:
1. `_fields_for_serialization` lists Python attribute names (not API keys)
2. `_field_map` includes all non-standard mappings
3. All attributes have corresponding API keys

### Missing attributes after `from_dict()`
**Problem:** Attributes are `None` when they shouldn't be

**Solution:** Check:
1. API response has the expected keys
2. `_field_map` correctly maps API keys to Python attributes
3. Attribute names match exactly (case-sensitive)

## Examples

See the existing configuration classes for reference implementations:
- **Basic**: `DomoAccount_Config_Snowflake` (snowflake.py)
- **With field_map**: `DomoAccount_Config_SnowflakeKeyPairInternalManagedUnload` (snowflake.py)
- **With custom logic**: `DomoAccount_Config_AmazonS3` (aws.py)
- **Complex mapping**: `DomoAccount_Config_AwsAthena` (aws.py)

## Testing

Always test your config class with real API responses:

```python
# Test deserialization
api_response = {
    "accessKey": "AKIAIOSFODNN7EXAMPLE",
    "secretKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "bucket": "my-bucket",
    "region": "us-west-2",
    "allowExternalUse": "true"
}

config = DomoAccount_Config_MyConnector.from_dict(api_response)
assert config.access_key == "AKIAIOSFODNN7EXAMPLE"
assert config.secret_key == "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Test serialization
output = config.to_dict()
assert output["accessKey"] == "AKIAIOSFODNN7EXAMPLE"
assert output["secretKey"] == "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
assert output["allowExternalUse"] is True
```

## Questions?

For questions or issues with account configurations:
1. Check this README
2. Review existing config classes for patterns
3. See `_base.py` for base class implementation details
4. Consult `.github/instructions/general.instructions.md` for project guidelines
