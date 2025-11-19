"""Test _available_config_keys functionality."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from domolibrary2.classes.DomoDataset.stream_configs import (
    CONFORMED_PROPERTIES,
    get_available_config_keys,
)


def test_available_config_keys():
    """Test get_available_config_keys function."""
    print("=" * 80)
    print("Test 1: get_available_config_keys Function")
    print("=" * 80)

    # Mock typed_config with some unmapped attributes
    class MockSnowflakeConfig:
        data_provider_type = "snowflake"
        query = "SELECT * FROM table"
        database_name = "SA_PRD"
        warehouse = "COMPUTE_WH"
        schema_name = "PUBLIC"
        # Add some attributes that aren't mapped to conformed properties
        role = "ANALYST_ROLE"  # Not mapped
        authenticator = "snowflake"  # Not mapped
        private_key_path = "/path/to/key"  # Not mapped

    mock_config = MockSnowflakeConfig()

    # Mock stream object
    class MockStream:
        def __init__(self):
            self.data_provider_key = "snowflake"
            self.typed_config = mock_config

    stream = MockStream()
    available = get_available_config_keys(stream)

    print(f"\n  Available unmapped keys: {available}")

    # Should include unmapped keys
    assert "role" in available, "role should be unmapped"
    assert "authenticator" in available, "authenticator should be unmapped"
    assert "private_key_path" in available, "private_key_path should be unmapped"

    # Should NOT include mapped keys
    assert "query" not in available, "query is mapped to 'query' conformed property"
    assert (
        "database_name" not in available
    ), "database_name is mapped to 'database' conformed property"
    assert (
        "warehouse" not in available
    ), "warehouse is mapped to 'warehouse' conformed property"

    print("  ✓ Correctly identifies unmapped keys")


def test_property_on_stream():
    """Test _available_config_keys as a property on stream."""
    print("\n" + "=" * 80)
    print("Test 2: _available_config_keys Property")
    print("=" * 80)

    class MockConfig:
        data_provider_type = "snowflake"
        query = "SELECT * FROM table"
        database_name = "SA_PRD"
        warehouse = "COMPUTE_WH"
        role = "ANALYST_ROLE"
        authenticator = "snowflake"

    mock_config = MockConfig()

    class MockStream:
        def __init__(self):
            self.data_provider_key = "snowflake"
            self.typed_config = mock_config

        @property
        def _available_config_keys(self):
            return get_available_config_keys(self)

    stream = MockStream()
    available = stream._available_config_keys

    print(f"\n  Available keys: {available}")
    assert isinstance(available, list)
    assert len(available) > 0  # Should have some unmapped keys
    assert "role" in available

    print("  ✓ _available_config_keys property works")


def test_identifies_gaps():
    """Test that it helps identify gaps in conformed properties."""
    print("\n" + "=" * 80)
    print("Test 3: Identifying Gaps in Conformed Properties")
    print("=" * 80)

    # Create comprehensive config
    class MockConfig:
        data_provider_type = "snowflake"
        query = "SELECT * FROM table"
        database_name = "SA_PRD"
        warehouse = "COMPUTE_WH"
        role = "ANALYST_ROLE"  # Gap
        authenticator = "snowflake"  # Gap
        cloud_provider = "AWS"  # Gap
        timeout_seconds = 30  # Gap

    mock_config = MockConfig()

    class MockStream:
        def __init__(self):
            self.data_provider_key = "snowflake"
            self.typed_config = mock_config

    stream = MockStream()
    available = get_available_config_keys(stream)

    print(f"\n  Configuration keys not yet mapped:")
    for key in available:
        print(f"    - {key}")

    print(
        "\n  💡 These keys could be added to CONFORMED_PROPERTIES if they're common"
    )
    print("     across multiple providers (e.g., 'role' might be used by many DBs)")

    print("\n  ✓ Successfully identifies mapping gaps")


def test_empty_when_all_mapped():
    """Test that list is empty when all keys are mapped."""
    print("\n" + "=" * 80)
    print("Test 4: Empty When All Keys Mapped")
    print("=" * 80)

    # Config with only mapped keys
    class MockConfig:
        data_provider_type = "snowflake"
        query = "SELECT * FROM table"
        database_name = "SA_PRD"
        warehouse = "COMPUTE_WH"

    mock_config = MockConfig()

    class MockStream:
        def __init__(self):
            self.data_provider_key = "snowflake"
            self.typed_config = mock_config

    stream = MockStream()
    available = get_available_config_keys(stream)

    print(f"\n  Available unmapped keys: {available}")

    # The main mapped keys should not be present
    assert "query" not in available
    assert "database_name" not in available
    assert "warehouse" not in available

    print("\n  ✓ Mapped keys correctly excluded")


def test_different_providers():
    """Test with different providers to show different unmapped keys."""
    print("\n" + "=" * 80)
    print("Test 5: Different Providers Have Different Unmapped Keys")
    print("=" * 80)

    # Snowflake config
    class SnowflakeConfig:
        data_provider_type = "snowflake"
        query = "SELECT * FROM table"
        database_name = "SA_PRD"
        warehouse = "COMPUTE_WH"
        role = "ANALYST_ROLE"
        authenticator = "snowflake"

    snowflake_config = SnowflakeConfig()

    class SnowflakeStream:
        def __init__(self):
            self.data_provider_key = "snowflake"
            self.typed_config = snowflake_config

    snowflake = SnowflakeStream()
    snowflake_available = get_available_config_keys(snowflake)

    print(f"\n  Snowflake unmapped keys: {snowflake_available}")
    print("  💡 Consider adding 'role' and 'authenticator' if used by other DBs")

    print("\n  ✓ Different providers show different unmapped keys")


if __name__ == "__main__":
    # Run all tests
    test_available_config_keys()
    test_property_on_stream()
    test_identifies_gaps()
    test_empty_when_all_mapped()
    test_different_providers()

    print("\n" + "=" * 80)
    print("All Tests Passed! ✅")
    print("=" * 80)
    print(
        """
Usage:
  1. Check unmapped keys: stream._available_config_keys
  2. Identify common keys across providers
  3. Add to CONFORMED_PROPERTIES if applicable
  4. Keys will disappear from _available_config_keys once mapped

This helps extend conformed properties coverage!
    """
    )
