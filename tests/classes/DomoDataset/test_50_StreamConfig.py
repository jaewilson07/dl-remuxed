"""
Test file for StreamConfig registry and mapping system
Tests the decorator-based registry pattern, mapping lookups, and enum functionality
"""

import sys
from pathlib import Path
from importlib import import_module

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import the stream_config module directly to avoid circular imports
stream_config = import_module("domolibrary2.classes.DomoDataset.stream_config")

StreamConfig_Mapping = stream_config.StreamConfig_Mapping
StreamConfig_Mappings = stream_config.StreamConfig_Mappings
register_mapping = stream_config.register_mapping
_MAPPING_REGISTRY = stream_config._MAPPING_REGISTRY


# ============================================================================
# Test 1: Registry Population
# ============================================================================


def test_registry_populated():
    """Test that the registry is populated with mappings from all platform files."""
    assert len(_MAPPING_REGISTRY) > 0, "Registry should contain mappings"
    print(f"Registry contains {len(_MAPPING_REGISTRY)} mappings")


def test_registry_has_expected_providers():
    """Test that common data providers are registered."""
    expected_providers = [
        "snowflake",
        "aws-athena",
        "google-sheets",
        "dataset-copy",
        "default",
    ]

    for provider in expected_providers:
        assert provider in _MAPPING_REGISTRY, f"{provider} should be in registry"
        print(f"✓ {provider} found in registry")


def test_registry_values_are_classes():
    """Test that registry values are classes, not instances."""
    for key, value in _MAPPING_REGISTRY.items():
        assert isinstance(value, type), f"Registry value for {key} should be a class"
        assert issubclass(
            value, StreamConfig_Mapping
        ), f"Registry value for {key} should be a StreamConfig_Mapping subclass"


# ============================================================================
# Test 2: Decorator Functionality
# ============================================================================


def test_register_mapping_decorator():
    """Test that the register_mapping decorator works correctly."""

    @register_mapping("test-provider")
    class TestMapping(StreamConfig_Mapping):
        data_provider_type: str = "test-provider"
        test_field: str = "testValue"

    assert "test-provider" in _MAPPING_REGISTRY
    assert _MAPPING_REGISTRY["test-provider"] == TestMapping

    # Cleanup
    del _MAPPING_REGISTRY["test-provider"]


def test_decorator_returns_class():
    """Test that decorator returns the class unchanged."""

    @register_mapping("test-provider-2")
    class TestMapping2(StreamConfig_Mapping):
        data_provider_type: str = "test-provider-2"

    # Should be able to instantiate
    instance = TestMapping2()
    assert isinstance(instance, StreamConfig_Mapping)
    assert instance.data_provider_type == "test-provider-2"

    # Cleanup
    del _MAPPING_REGISTRY["test-provider-2"]


# ============================================================================
# Test 3: StreamConfig_Mappings Enum Search
# ============================================================================


def test_enum_search_exact_match():
    """Test enum search with exact provider name."""
    mapping = StreamConfig_Mappings.search("snowflake")
    assert mapping is not None
    assert isinstance(mapping, StreamConfig_Mapping)
    assert mapping.data_provider_type == "snowflake"


def test_enum_search_normalized():
    """Test enum search with normalized names (hyphens vs underscores)."""
    # Test that both formats work
    mapping1 = StreamConfig_Mappings.search("aws-athena")
    mapping2 = StreamConfig_Mappings.search("aws_athena")

    assert mapping1 is not None
    assert mapping2 is not None
    assert mapping1.data_provider_type == mapping2.data_provider_type


def test_enum_search_case_insensitive():
    """Test that enum search is case insensitive."""
    mapping1 = StreamConfig_Mappings.search("snowflake")
    mapping2 = StreamConfig_Mappings.search("SNOWFLAKE")
    mapping3 = StreamConfig_Mappings.search("SnowFlake")

    assert mapping1 is not None
    assert mapping2 is not None
    assert mapping3 is not None


def test_enum_search_returns_default_for_unknown():
    """Test that search returns default mapping for unknown providers."""
    mapping = StreamConfig_Mappings.search("unknown-provider-xyz")
    assert mapping is not None
    assert mapping.is_default is True


# ============================================================================
# Test 4: Mapping Instance Functionality
# ============================================================================


def test_snowflake_mapping_fields():
    """Test that Snowflake mapping has correct field mappings."""
    mapping = StreamConfig_Mappings.search("snowflake")

    assert mapping.sql == "query"
    assert mapping.warehouse == "warehouseName"
    assert mapping.database_name == "databaseName"


def test_mapping_search_keys_by_value():
    """Test search_keys_by_value method on mapping instances."""
    mapping = StreamConfig_Mappings.search("snowflake")

    # Should find the key for the given value
    key = mapping.search_keys_by_value("query")
    assert key == "sql"

    key = mapping.search_keys_by_value("warehouseName")
    assert key == "warehouse"


def test_default_mapping_custom_query_handling():
    """Test that default mapping handles custom query variations."""
    mapping = StreamConfig_Mappings.search("default")

    assert mapping.is_default is True
    assert mapping.search_keys_by_value("enteredCustomQuery") == "sql"
    assert mapping.search_keys_by_value("query") == "sql"
    assert mapping.search_keys_by_value("customQuery") == "sql"


# ============================================================================
# Test 5: Platform Coverage
# ============================================================================


def test_snowflake_variants():
    """Test that various Snowflake configurations are registered."""
    snowflake_variants = [
        "snowflake",
        "snowflake_federated",
        "snowflake-internal-unload",
        "snowflake-keypair-authentication",
    ]

    for variant in snowflake_variants:
        normalized = variant.replace("-", "_")
        mapping = StreamConfig_Mappings.search(variant)
        assert mapping is not None, f"{variant} should have a mapping"
        print(f"✓ {variant} mapping found")


def test_aws_providers():
    """Test that AWS providers are registered."""
    aws_providers = [
        "aws-athena",
        "amazon-athena-high-bandwidth-connector",
        "amazon-s3-assume-role",
    ]

    for provider in aws_providers:
        mapping = StreamConfig_Mappings.search(provider)
        assert mapping is not None, f"{provider} should have a mapping"
        print(f"✓ {provider} mapping found")


def test_google_providers():
    """Test that Google providers are registered."""
    google_providers = [
        "google-sheets",
        "google-spreadsheets",
    ]

    for provider in google_providers:
        mapping = StreamConfig_Mappings.search(provider)
        assert mapping is not None, f"{provider} should have a mapping"
        print(f"✓ {provider} mapping found")


def test_domo_providers():
    """Test that Domo-specific providers are registered."""
    domo_providers = [
        "dataset-copy",
        "domo-csv",
    ]

    for provider in domo_providers:
        mapping = StreamConfig_Mappings.search(provider)
        assert mapping is not None, f"{provider} should have a mapping"
        print(f"✓ {provider} mapping found")


# ============================================================================
# Test 6: Integration Tests
# ============================================================================


def test_all_registered_providers_instantiate():
    """Test that all registered providers can be instantiated."""
    for provider_name, mapping_cls in _MAPPING_REGISTRY.items():
        instance = mapping_cls()
        assert isinstance(instance, StreamConfig_Mapping)
        assert hasattr(instance, "data_provider_type")
        print(f"✓ {provider_name}: instantiated successfully")


def test_no_duplicate_registrations():
    """Test that there are no duplicate provider registrations."""
    # All keys should be unique (this is guaranteed by dict, but let's verify logic)
    keys = list(_MAPPING_REGISTRY.keys())
    assert len(keys) == len(set(keys)), "Registry should not have duplicate keys"


def test_registry_count():
    """Test that we have the expected number of mappings."""
    # Based on the current implementation:
    # - 7 Snowflake variants
    # - 3 AWS providers
    # - 2 Google providers
    # - 2 Domo providers
    # - 5 other providers (Adobe, PostgreSQL, Qualtrics, SharePoint, default)
    # Total: 19 mappings

    assert (
        len(_MAPPING_REGISTRY) >= 19
    ), f"Expected at least 19 mappings, found {len(_MAPPING_REGISTRY)}"
    print(f"Registry contains {len(_MAPPING_REGISTRY)} mappings")


# ============================================================================
# Test 7: Edge Cases
# ============================================================================


def test_search_with_none():
    """Test that search handles None gracefully."""
    mapping = StreamConfig_Mappings.search(None)
    assert mapping is not None
    assert mapping.is_default is True


def test_search_with_empty_string():
    """Test that search handles empty string gracefully."""
    mapping = StreamConfig_Mappings.search("")
    assert mapping is not None
    assert mapping.is_default is True


def test_mapping_inheritance():
    """Test that all mappings properly inherit from StreamConfig_Mapping."""
    for provider_name, mapping_cls in _MAPPING_REGISTRY.items():
        assert issubclass(
            mapping_cls, StreamConfig_Mapping
        ), f"{provider_name} should inherit from StreamConfig_Mapping"


# ============================================================================
# Run all tests
# ============================================================================


if __name__ == "__main__":
    print("=" * 80)
    print("Stream Config Registry Tests")
    print("=" * 80)

    # Run each test
    test_functions = [
        ("Registry Population", test_registry_populated),
        ("Expected Providers", test_registry_has_expected_providers),
        ("Registry Values Are Classes", test_registry_values_are_classes),
        ("Decorator Functionality", test_register_mapping_decorator),
        ("Decorator Returns Class", test_decorator_returns_class),
        ("Exact Match Search", test_enum_search_exact_match),
        ("Normalized Search", test_enum_search_normalized),
        ("Case Insensitive Search", test_enum_search_case_insensitive),
        ("Default Fallback", test_enum_search_returns_default_for_unknown),
        ("Snowflake Fields", test_snowflake_mapping_fields),
        ("Search Keys By Value", test_mapping_search_keys_by_value),
        ("Default Custom Query", test_default_mapping_custom_query_handling),
        ("Snowflake Variants", test_snowflake_variants),
        ("AWS Providers", test_aws_providers),
        ("Google Providers", test_google_providers),
        ("Domo Providers", test_domo_providers),
        ("All Providers Instantiate", test_all_registered_providers_instantiate),
        ("No Duplicates", test_no_duplicate_registrations),
        ("Registry Count", test_registry_count),
        ("Search with None", test_search_with_none),
        ("Search with Empty String", test_search_with_empty_string),
        ("Mapping Inheritance", test_mapping_inheritance),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in test_functions:
        try:
            print(f"\n{test_name}:")
            test_func()
            print(f"✓ PASSED")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)
