"""Test custom __repr__ with conformed properties on DomoStream."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

import domolibrary2.auth as dmda
from domolibrary2.classes.DomoDataset.stream import DomoStream
from domolibrary2.classes.DomoDataset.stream_configs._repr import (
    create_stream_repr,
    get_conformed_properties_for_repr,
)

load_dotenv()

token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


def test_repr_function():
    """Test the repr creation function with mock data."""
    print("=" * 80)
    print("Test 1: create_stream_repr Function")
    print("=" * 80)

    # Create a mock stream-like object
    class MockStream:
        id = "stream-123"
        data_provider_name = "Snowflake"
        data_provider_key = "snowflake"

        @property
        def sql(self):
            return "SELECT * FROM customers WHERE region = 'US'"

        @property
        def database(self):
            return "SA_PRD"

        @property
        def warehouse(self):
            return "COMPUTE_WH"

        @property
        def schema(self):
            return "PUBLIC"

    mock = MockStream()
    repr_str = create_stream_repr(mock)

    print(f"\nRepr: {repr_str}")
    print(f"Length: {len(repr_str)} chars")

    # Verify key components
    assert "stream-123" in repr_str
    assert "Snowflake" in repr_str or "snowflake" in repr_str
    assert "sql=" in repr_str
    assert "database=" in repr_str

    print("✓ Function test passed")


def test_get_conformed_properties():
    """Test getting conformed properties dict."""
    print("\n" + "=" * 80)
    print("Test 2: get_conformed_properties_for_repr")
    print("=" * 80)

    class MockStream:
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
        def report_id(self):
            return None  # Not applicable

    mock = MockStream()
    props = get_conformed_properties_for_repr(mock)

    print(f"\nProperties: {props}")
    print(f"Count: {len(props)}")

    assert "sql" in props
    assert "database" in props
    assert "warehouse" in props
    assert "report_id" not in props  # None values excluded

    print("✓ Get properties test passed")


def test_truncation():
    """Test that long values are truncated."""
    print("\n" + "=" * 80)
    print("Test 3: Value Truncation")
    print("=" * 80)

    class MockStream:
        id = "stream-456"
        data_provider_key = "snowflake"

        @property
        def sql(self):
            return "SELECT * FROM very_long_table_name WHERE column1 = 'value' AND column2 = 'value' AND column3 = 'value' AND column4 = 'value'"

        @property
        def database(self):
            return "SA_PRD"

    mock = MockStream()
    repr_str = create_stream_repr(mock, max_value_length=30)

    print(f"\nRepr: {repr_str}")

    # Long SQL should be truncated
    assert "..." in repr_str
    print("✓ Truncation test passed")


def test_priority_ordering():
    """Test that priority properties appear first."""
    print("\n" + "=" * 80)
    print("Test 4: Priority Ordering")
    print("=" * 80)

    class MockStream:
        id = "stream-789"
        data_provider_key = "snowflake"

        @property
        def sql(self):
            return "SELECT * FROM table"

        @property
        def database(self):
            return "SA_PRD"

        @property
        def table(self):
            return "customers"

        @property
        def spreadsheet(self):
            return "sheet123"  # Not relevant for Snowflake

    mock = MockStream()
    repr_str = create_stream_repr(mock)

    print(f"\nRepr: {repr_str}")

    # SQL should appear before table
    sql_pos = repr_str.find("sql=")
    table_pos = repr_str.find("table=")

    assert sql_pos < table_pos
    print("✓ Priority ordering test passed")


async def test_real_stream():
    """Test with a real DomoStream (requires env vars)."""
    print("\n" + "=" * 80)
    print("Test 5: Real DomoStream")
    print("=" * 80)

    stream_id = os.environ.get("STREAM_ID_1")

    if not stream_id:
        print("⚠ Skipping real stream test - STREAM_ID_1 not set")
        return

    try:
        stream = await DomoStream.get_by_id(
            auth=token_auth, stream_id=stream_id, is_get_account=False
        )

        print(f"\nStream repr:")
        print(f"  {stream}")
        print(f"\nRepr length: {len(repr(stream))} chars")

        # Verify repr includes key info
        repr_str = repr(stream)
        assert stream.id in repr_str
        print("✓ Real stream test passed")

        # Show conformed properties
        props = get_conformed_properties_for_repr(stream)
        print(f"\nConformed properties found: {list(props.keys())}")
        for key, value in props.items():
            value_preview = (
                str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            )
            print(f"  {key}: {value_preview}")

    except Exception as e:
        print(f"✗ Real stream test failed: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    # Sync tests
    test_repr_function()
    test_get_conformed_properties()
    test_truncation()
    test_priority_ordering()

    # Async test
    asyncio.run(test_real_stream())

    print("\n" + "=" * 80)
    print("All Tests Completed!")
    print("=" * 80)
