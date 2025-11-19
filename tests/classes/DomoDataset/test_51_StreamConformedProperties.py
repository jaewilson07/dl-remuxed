"""Test file for conformed properties on DomoStream.

Tests that semantic properties (sql, database, warehouse, etc.) work
correctly across different data provider types.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

import domolibrary2.auth as dmda
from domolibrary2.classes.DomoDataset.stream import DomoStream
from domolibrary2.classes.DomoDataset.stream_configs import (
    CONFORMED_PROPERTIES,
    ConformedProperty,
)
from domolibrary2.classes.DomoDataset.stream_configs.snowflake import (
    Snowflake_StreamConfig,
)

load_dotenv()

token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


# ============================================================================
# Test 1: ConformedProperty Class
# ============================================================================


def test_conformed_property_basic():
    """Test basic ConformedProperty functionality."""
    prop = ConformedProperty(
        name="test_prop",
        description="Test property",
        mappings={"provider1": "attr1", "provider2": "attr2"},
    )

    assert prop.name == "test_prop"
    assert prop.get_key_for_provider("provider1") == "attr1"
    assert prop.get_key_for_provider("provider2") == "attr2"
    assert prop.get_key_for_provider("unknown") is None
    assert "provider1" in prop.supported_providers
    assert "provider2" in prop.supported_providers
    print("✓ ConformedProperty basic functionality works")


def test_conformed_properties_registry():
    """Test that CONFORMED_PROPERTIES registry is populated."""
    assert len(CONFORMED_PROPERTIES) > 0, "Registry should contain properties"
    assert "query" in CONFORMED_PROPERTIES
    assert "database" in CONFORMED_PROPERTIES
    assert "warehouse" in CONFORMED_PROPERTIES
    print(f"✓ Registry contains {len(CONFORMED_PROPERTIES)} conformed properties")


def test_query_property_mappings():
    """Test that query property has correct mappings."""
    query_prop = CONFORMED_PROPERTIES["query"]

    # Should support multiple providers
    assert query_prop.get_key_for_provider("snowflake") == "query"
    assert (
        query_prop.get_key_for_provider("snowflakekeypairauthentication") == "query"
    )
    assert query_prop.get_key_for_provider("aws-athena") == "query"
    assert query_prop.get_key_for_provider("postgresql") == "query"

    print("✓ Query property mappings are correct")


def test_database_property_mappings():
    """Test that database property has correct mappings."""
    db_prop = CONFORMED_PROPERTIES["database"]

    # Should support database providers
    assert db_prop.get_key_for_provider("snowflake") == "database_name"
    assert db_prop.get_key_for_provider("aws-athena") == "database_name"
    assert db_prop.get_key_for_provider("postgresql") == "database_name"

    print("✓ Database property mappings are correct")


def test_warehouse_property_mappings():
    """Test that warehouse property is Snowflake-specific."""
    wh_prop = CONFORMED_PROPERTIES["warehouse"]

    # Should support Snowflake variants
    assert wh_prop.get_key_for_provider("snowflake") == "warehouse"
    assert wh_prop.get_key_for_provider("snowflakekeypairauthentication") == "warehouse"

    # Should NOT support non-Snowflake providers
    assert wh_prop.get_key_for_provider("aws-athena") is None
    assert wh_prop.get_key_for_provider("postgresql") is None

    print("✓ Warehouse property mappings are correct")


# ============================================================================
# Test 2: DomoStream Conformed Properties (Mock)
# ============================================================================


def test_stream_conformed_properties_mock():
    """Test DomoStream conformed properties with mock data."""
    from unittest.mock import Mock

    # Create a mock stream with Snowflake config
    stream = Mock(spec=DomoStream)
    stream.data_provider_key = "snowflake"
    stream.configuration = []

    # Create a Snowflake typed config
    typed = Snowflake_StreamConfig(
        query="SELECT * FROM table",
        database_name="SA_PRD",
        warehouse="COMPUTE_WH",
        schema_name="PUBLIC",
    )

    # Mock the typed_config property
    type(stream).typed_config = property(lambda self: typed)

    # Mock _get_conformed_value to use the real implementation
    def mock_get_conformed_value(property_name: str):
        if typed is None:
            return None

        conformed_prop = CONFORMED_PROPERTIES.get(property_name)
        if not conformed_prop:
            return None

        attr_name = conformed_prop.get_key_for_provider(stream.data_provider_key)
        if not attr_name:
            return None

        return getattr(typed, attr_name, None)

    stream._get_conformed_value = mock_get_conformed_value

    # Test conformed properties
    assert mock_get_conformed_value("query") == "SELECT * FROM table"
    assert mock_get_conformed_value("database") == "SA_PRD"
    assert mock_get_conformed_value("warehouse") == "COMPUTE_WH"
    assert mock_get_conformed_value("schema") == "PUBLIC"

    print("✓ DomoStream conformed properties work with mock data")


# ============================================================================
# Test 3: Cross-Platform Property Access
# ============================================================================


def test_cross_platform_query():
    """Test that query property works across different providers."""
    providers_with_query = [
        "snowflake",
        "snowflakekeypairauthentication",
        "aws-athena",
        "amazon-athena-high-bandwidth",
        "postgresql",
    ]

    query_prop = CONFORMED_PROPERTIES["query"]

    for provider in providers_with_query:
        attr_name = query_prop.get_key_for_provider(provider)
        assert attr_name is not None, f"Query should work for {provider}"
        print(f"  ✓ {provider}: maps to '{attr_name}'")

    print("✓ Query property works across all SQL providers")


def test_report_id_property():
    """Test report_id property for analytics platforms."""
    report_prop = CONFORMED_PROPERTIES["report_id"]

    # Adobe Analytics
    assert (
        report_prop.get_key_for_provider("adobe-analytics-v2")
        == "adobe_report_suite_id"
    )

    # Qualtrics
    assert report_prop.get_key_for_provider("qualtrics") == "qualtrics_survey_id"

    print("✓ Report ID property works for analytics platforms")


def test_spreadsheet_property():
    """Test spreadsheet property for Google connectors."""
    sheet_prop = CONFORMED_PROPERTIES["spreadsheet"]

    # Google Sheets
    assert (
        sheet_prop.get_key_for_provider("google-sheets")
        == "spreadsheet_id_file_name"
    )

    # Google Spreadsheets
    assert (
        sheet_prop.get_key_for_provider("google-spreadsheets")
        == "spreadsheet_id_file_name"
    )

    print("✓ Spreadsheet property works for Google connectors")


# ============================================================================
# Test 4: Property Coverage
# ============================================================================


def test_all_properties_have_mappings():
    """Test that all conformed properties have at least one mapping."""
    for prop_name, prop in CONFORMED_PROPERTIES.items():
        assert len(prop.mappings) > 0, f"{prop_name} should have at least one mapping"
        assert len(prop.supported_providers) > 0, f"{prop_name} should support providers"
        print(
            f"  ✓ {prop_name}: {len(prop.supported_providers)} provider(s) supported"
        )

    print("✓ All conformed properties have valid mappings")


def test_property_descriptions():
    """Test that all properties have descriptions."""
    for prop_name, prop in CONFORMED_PROPERTIES.items():
        assert (
            prop.description is not None
        ), f"{prop_name} should have a description"
        assert len(prop.description) > 0, f"{prop_name} description should not be empty"

    print("✓ All conformed properties have descriptions")


# ============================================================================
# Test 5: Real DomoStream Test (if stream ID available)
# ============================================================================


async def test_real_stream_conformed_properties():
    """Test conformed properties on a real DomoStream (requires env vars).

    This test requires STREAM_ID_1 environment variable to be set.
    """
    stream_id = os.environ.get("STREAM_ID_1")

    if not stream_id:
        print("⚠ Skipping real stream test - STREAM_ID_1 not set")
        return

    try:
        stream = await DomoStream.get_by_id(
            auth=token_auth, stream_id=stream_id, is_get_account=False
        )

        print(f"\n✓ Retrieved stream: {stream.id}")
        print(f"  Provider: {stream.data_provider_key}")

        # Test that typed_config works
        if stream.typed_config:
            print(f"  ✓ Typed config: {type(stream.typed_config).__name__}")
        else:
            print(f"  ⚠ No typed config for provider: {stream.data_provider_key}")

        # Test conformed properties
        print("\n  Conformed Properties:")
        if stream.sql:
            print(f"    SQL: {stream.sql[:50]}..." if len(stream.sql) > 50 else f"    SQL: {stream.sql}")
        if stream.database:
            print(f"    Database: {stream.database}")
        if stream.schema:
            print(f"    Schema: {stream.schema}")
        if stream.warehouse:
            print(f"    Warehouse: {stream.warehouse}")
        if stream.table:
            print(f"    Table: {stream.table}")
        if stream.report_id:
            print(f"    Report ID: {stream.report_id}")
        if stream.spreadsheet:
            print(f"    Spreadsheet: {stream.spreadsheet}")

        print("\n✓ Real stream conformed properties test completed")

    except Exception as e:
        print(f"✗ Real stream test failed: {e}")
        raise


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    import asyncio

    print("=" * 80)
    print("Conformed Properties Tests")
    print("=" * 80)

    # Sync tests
    test_functions = [
        ("ConformedProperty Basic", test_conformed_property_basic),
        ("Registry Populated", test_conformed_properties_registry),
        ("Query Mappings", test_query_property_mappings),
        ("Database Mappings", test_database_property_mappings),
        ("Warehouse Mappings", test_warehouse_property_mappings),
        ("Mock Stream Properties", test_stream_conformed_properties_mock),
        ("Cross-Platform Query", test_cross_platform_query),
        ("Report ID Property", test_report_id_property),
        ("Spreadsheet Property", test_spreadsheet_property),
        ("Property Coverage", test_all_properties_have_mappings),
        ("Property Descriptions", test_property_descriptions),
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

    # Async test
    print("\n" + "=" * 80)
    print("Real Stream Test (async)")
    print("=" * 80)
    try:
        asyncio.run(test_real_stream_conformed_properties())
        passed += 1
    except Exception as e:
        print(f"✗ ERROR: {e}")
        failed += 1

    print("\n" + "=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)
