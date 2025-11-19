"""Comprehensive example demonstrating all conformed property features.

This example showcases:
1. Conformed properties (cross-platform access)
2. Custom repr (automatic property display)
3. is_repr flag (control visibility)
4. _missing_mappings (discover limitations)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from domolibrary2.classes.DomoDataset.stream_configs import (
    CONFORMED_PROPERTIES,
    create_stream_repr,
    get_missing_mappings,
)


def demo_conformed_properties():
    """Demo 1: Conformed Properties - Cross-Platform Access."""
    print("=" * 80)
    print("Demo 1: Conformed Properties - Cross-Platform Access")
    print("=" * 80)

    # Mock streams from different providers
    class SnowflakeStream:
        id = "snowflake-123"
        data_provider_key = "snowflake"
        data_provider_name = "Snowflake"

        @property
        def sql(self):
            return "SELECT * FROM customers WHERE region = 'US'"

        @property
        def database(self):
            return "SA_PRD"

        @property
        def warehouse(self):
            return "COMPUTE_WH"

    class SheetsStream:
        id = "sheets-456"
        data_provider_key = "google-sheets"
        data_provider_name = "Google Sheets"

        @property
        def spreadsheet(self):
            return "1A2B3C4D5E6F7G8H9I0J"

    # Use same property names across different providers
    snowflake = SnowflakeStream()
    sheets = SheetsStream()

    print("\nSnowflake Stream:")
    print(f"  SQL: {snowflake.sql}")
    print(f"  Database: {snowflake.database}")
    print(f"  Warehouse: {snowflake.warehouse}")

    print("\nGoogle Sheets Stream:")
    print(f"  Spreadsheet: {sheets.spreadsheet}")

    print("\n✓ Same property names work across different providers!")


def demo_custom_repr():
    """Demo 2: Custom Repr - Automatic Display."""
    print("\n" + "=" * 80)
    print("Demo 2: Custom Repr - Automatic Display")
    print("=" * 80)

    class MockStream:
        id = "stream-789"
        data_provider_key = "snowflake"
        data_provider_name = "Snowflake"

        @property
        def sql(self):
            return "SELECT id, name, email FROM users WHERE active = TRUE"

        @property
        def database(self):
            return "SA_PRD"

        @property
        def warehouse(self):
            return "COMPUTE_WH"

        @property
        def host(self):
            # This has is_repr=False, won't appear in repr
            return "db.example.com"

    stream = MockStream()
    repr_str = create_stream_repr(stream)

    print("\nRepr Output:")
    print(f"  {repr_str}")

    print("\n✓ Shows: SQL, database, warehouse (is_repr=True)")
    print("✓ Hides: host (is_repr=False)")
    print("✓ Properties automatically visible when printing!")


def demo_is_repr_flag():
    """Demo 3: is_repr Flag - Control Visibility."""
    print("\n" + "=" * 80)
    print("Demo 3: is_repr Flag - Control Visibility")
    print("=" * 80)

    print("\nProperties with is_repr=True (shown in repr):")
    for prop_name, prop in CONFORMED_PROPERTIES.items():
        if prop.is_repr:
            print(f"  ✅ {prop_name}: {prop.description}")

    print("\nProperties with is_repr=False (hidden from repr):")
    for prop_name, prop in CONFORMED_PROPERTIES.items():
        if not prop.is_repr:
            print(f"  ❌ {prop_name}: {prop.description}")

    print("\n✓ Fine-grained control over repr visibility")
    print("✓ Security: Sensitive properties (host, port) hidden")
    print("✓ Clarity: Only important properties shown")


def demo_missing_mappings():
    """Demo 4: _missing_mappings - Discover Limitations."""
    print("\n" + "=" * 80)
    print("Demo 4: _missing_mappings - Discover Limitations")
    print("=" * 80)

    providers = [
        ("snowflake", "Snowflake"),
        ("google-sheets", "Google Sheets"),
        ("adobe-analytics-v2", "Adobe Analytics V2"),
        ("postgresql", "PostgreSQL"),
    ]

    for provider_key, provider_name in providers:

        class MockStream:
            id = f"{provider_key}-stream"
            data_provider_key = provider_key
            data_provider_name = provider_name

        stream = MockStream()
        missing = get_missing_mappings(stream)

        print(f"\n{provider_name} ({provider_key}):")
        print(f"  Missing {len(missing)} properties:")
        for prop in missing:
            print(f"    - {prop}")

    print("\n✓ Easy to see which properties aren't supported")
    print("✓ Helpful for debugging None values")
    print("✓ Understand provider capabilities")


def demo_debugging_scenario():
    """Demo 5: Debugging with _missing_mappings."""
    print("\n" + "=" * 80)
    print("Demo 5: Debugging Scenario")
    print("=" * 80)

    class GoogleSheetsStream:
        id = "sheets-debug"
        data_provider_key = "google-sheets"

        @property
        def sql(self):
            return None  # Google Sheets doesn't use SQL

        @property
        def spreadsheet(self):
            return "1A2B3C4D5E"

        @property
        def _missing_mappings(self):
            return get_missing_mappings(self)

    stream = GoogleSheetsStream()

    print("\nScenario: Why is stream.sql None?")
    print(f"  stream.sql = {stream.sql}")

    print("\nDebug with _missing_mappings:")
    missing = stream._missing_mappings
    print(f"  stream._missing_mappings = {missing}")

    if "query" in missing:
        print("\n  💡 Insight: 'query' is in _missing_mappings!")
        print("     Google Sheets doesn't support SQL queries.")
        print("     This is expected behavior, not a bug.")

    print("\n✓ _missing_mappings explains why properties are None")


def demo_complete_workflow():
    """Demo 6: Complete Workflow."""
    print("\n" + "=" * 80)
    print("Demo 6: Complete Workflow")
    print("=" * 80)

    class ProductionStream:
        id = "prod-stream-001"
        data_provider_key = "snowflake"
        data_provider_name = "Snowflake"

        @property
        def sql(self):
            return "SELECT * FROM orders WHERE date >= CURRENT_DATE - 30"

        @property
        def database(self):
            return "ANALYTICS_PROD"

        @property
        def warehouse(self):
            return "TRANSFORM_WH"

        @property
        def _missing_mappings(self):
            return get_missing_mappings(self)

    stream = ProductionStream()

    print("\n1. Quick inspection (repr):")
    repr_str = create_stream_repr(stream)
    print(f"   {repr_str}")

    print("\n2. Access properties programmatically:")
    print(f"   SQL: {stream.sql[:50]}...")
    print(f"   Database: {stream.database}")
    print(f"   Warehouse: {stream.warehouse}")

    print("\n3. Check what's not supported:")
    print(f"   Missing mappings: {stream._missing_mappings}")

    print("\n4. Conditional logic:")
    if "query" not in stream._missing_mappings:
        print("   ✓ This is a SQL-based connector")
        print(f"     Query length: {len(stream.sql)} chars")
    else:
        print("   ✗ This is not a SQL-based connector")

    print("\n✓ Complete workflow from discovery to usage")


if __name__ == "__main__":
    # Run all demos
    demo_conformed_properties()
    demo_custom_repr()
    demo_is_repr_flag()
    demo_missing_mappings()
    demo_debugging_scenario()
    demo_complete_workflow()

    print("\n" + "=" * 80)
    print("All Demos Complete! 🎉")
    print("=" * 80)
    print("""
Features Demonstrated:
  1. ✅ Conformed Properties - Cross-platform property access
  2. ✅ Custom Repr - Automatic property display
  3. ✅ is_repr Flag - Fine-grained visibility control
  4. ✅ _missing_mappings - Capability discovery
  5. ✅ Debugging - Understanding None values
  6. ✅ Complete Workflow - End-to-end usage

These features make DomoStream:
  • Self-documenting (repr shows what matters)
  • Maintainable (single source of truth)
  • Discoverable (properties easy to find)
  • Debuggable (_missing_mappings explains limitations)
  • Secure (sensitive data excluded from repr)
    """)
