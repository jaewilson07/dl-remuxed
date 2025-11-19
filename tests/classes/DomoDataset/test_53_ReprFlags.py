"""Test is_repr flag and _missing_mappings functionality."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from domolibrary2.classes.DomoDataset.stream_configs import (
    CONFORMED_PROPERTIES,
    create_stream_repr,
    get_missing_mappings,
)


def test_is_repr_flag():
    """Test that is_repr flag is set correctly on properties."""
    print("=" * 80)
    print("Test 1: is_repr Flag Configuration")
    print("=" * 80)

    # Properties that should have is_repr=True
    repr_properties = ["query", "database", "schema", "warehouse", "table", "report_id", "spreadsheet"]

    # Properties that should have is_repr=False
    no_repr_properties = ["bucket", "dataset_id", "file_url", "host", "port"]

    for prop_name in repr_properties:
        prop = CONFORMED_PROPERTIES.get(prop_name)
        assert prop is not None, f"{prop_name} should exist"
        assert prop.is_repr is True, f"{prop_name} should have is_repr=True"
        print(f"  ✓ {prop_name}: is_repr=True")

    for prop_name in no_repr_properties:
        prop = CONFORMED_PROPERTIES.get(prop_name)
        assert prop is not None, f"{prop_name} should exist"
        assert prop.is_repr is False, f"{prop_name} should have is_repr=False"
        print(f"  ✓ {prop_name}: is_repr=False")

    print("✓ All properties have correct is_repr flags")


def test_missing_mappings():
    """Test get_missing_mappings function."""
    print("\n" + "=" * 80)
    print("Test 2: get_missing_mappings Function")
    print("=" * 80)

    # Mock stream object
    class MockStream:
        def __init__(self, provider_key):
            self.data_provider_key = provider_key

    # Test Snowflake (should be missing analytics properties)
    snowflake_stream = MockStream("snowflake")
    missing = get_missing_mappings(snowflake_stream)
    print(f"\n  Snowflake missing: {missing}")
    assert "report_id" in missing, "Snowflake should be missing report_id"
    assert "spreadsheet" in missing, "Snowflake should be missing spreadsheet"
    assert "query" not in missing, "Snowflake should NOT be missing query"
    assert "database" not in missing, "Snowflake should NOT be missing database"

    # Test Google Sheets (should be missing SQL properties)
    sheets_stream = MockStream("google-sheets")
    missing = get_missing_mappings(sheets_stream)
    print(f"  Google Sheets missing: {missing}")
    assert "query" in missing, "Sheets should be missing query"
    assert "database" in missing, "Sheets should be missing database"
    assert "spreadsheet" not in missing, "Sheets should NOT be missing spreadsheet"

    # Test Adobe Analytics (should be missing SQL properties)
    adobe_stream = MockStream("adobe-analytics-v2")
    missing = get_missing_mappings(adobe_stream)
    print(f"  Adobe Analytics missing: {missing}")
    assert "query" in missing, "Adobe should be missing query"
    assert "report_id" not in missing, "Adobe should NOT be missing report_id"

    print("\n✓ Missing mappings correctly identified")


def test_repr_respects_is_repr_flag():
    """Test that repr only includes properties with is_repr=True."""
    print("\n" + "=" * 80)
    print("Test 3: Repr Respects is_repr Flag")
    print("=" * 80)

    class MockStream:
        id = "stream-123"
        data_provider_key = "snowflake"
        data_provider_name = "Snowflake"

        @property
        def sql(self):
            return "SELECT * FROM table"

        @property
        def database(self):
            return "SA_PRD"

        @property
        def warehouse(self):
            return "COMPUTE_WH"

        @property
        def host(self):
            # This has is_repr=False, should NOT appear
            return "db.example.com"

        @property
        def port(self):
            # This has is_repr=False, should NOT appear
            return "5432"

        @property
        def file_url(self):
            # This has is_repr=False, should NOT appear
            return "https://example.com/file.csv"

    mock = MockStream()
    repr_str = create_stream_repr(mock)

    print(f"\n  Repr: {repr_str}")

    # Should include properties with is_repr=True
    assert "sql=" in repr_str, "Should include sql (is_repr=True)"
    assert "database=" in repr_str, "Should include database (is_repr=True)"
    assert "warehouse=" in repr_str, "Should include warehouse (is_repr=True)"

    # Should NOT include properties with is_repr=False
    assert "host=" not in repr_str, "Should NOT include host (is_repr=False)"
    assert "port=" not in repr_str, "Should NOT include port (is_repr=False)"
    assert "file_url=" not in repr_str, "Should NOT include file_url (is_repr=False)"

    print("  ✓ Repr only includes is_repr=True properties")


def test_include_missing_mappings_flag():
    """Test that include_missing_mappings parameter works."""
    print("\n" + "=" * 80)
    print("Test 4: include_missing_mappings Parameter")
    print("=" * 80)

    class MockStream:
        id = "stream-456"
        data_provider_key = "google-sheets"

        @property
        def spreadsheet(self):
            return "1A2B3C4D5E"

    mock = MockStream()

    # Without missing mappings
    repr_without = create_stream_repr(mock, include_missing_mappings=False)
    print(f"\n  Without: {repr_without}")
    assert "_missing_mappings=" not in repr_without

    # With missing mappings
    repr_with = create_stream_repr(mock, include_missing_mappings=True)
    print(f"  With:    {repr_with}")
    assert "_missing_mappings=" in repr_with

    print("\n  ✓ include_missing_mappings parameter works")


def test_missing_mappings_property():
    """Test _missing_mappings as a property."""
    print("\n" + "=" * 80)
    print("Test 5: _missing_mappings Property")
    print("=" * 80)

    class MockStream:
        data_provider_key = "snowflake"

        @property
        def _missing_mappings(self):
            return get_missing_mappings(self)

    mock = MockStream()
    missing = mock._missing_mappings

    print(f"\n  Snowflake _missing_mappings: {missing}")
    assert isinstance(missing, list)
    assert len(missing) > 0  # Snowflake should be missing some properties
    assert "report_id" in missing
    assert "spreadsheet" in missing

    print("  ✓ _missing_mappings property works")


if __name__ == "__main__":
    # Run all tests
    test_is_repr_flag()
    test_missing_mappings()
    test_repr_respects_is_repr_flag()
    test_include_missing_mappings_flag()
    test_missing_mappings_property()

    print("\n" + "=" * 80)
    print("All Tests Passed! ✅")
    print("=" * 80)
