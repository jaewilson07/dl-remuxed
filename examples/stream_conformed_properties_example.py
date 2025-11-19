"""Example demonstrating conformed properties usage.

This shows how to use conformed properties to access stream configuration
parameters in a provider-agnostic way.
"""

import asyncio

from domolibrary2.classes.DomoDataset.stream import DomoStream
from domolibrary2.classes.DomoDataset.stream_configs import CONFORMED_PROPERTIES


def show_available_properties():
    """Display all available conformed properties."""
    print("=" * 80)
    print("Available Conformed Properties")
    print("=" * 80)

    for prop_name, prop in CONFORMED_PROPERTIES.items():
        print(f"\n{prop_name}:")
        print(f"  Description: {prop.description}")
        print(f"  Supported providers ({len(prop.supported_providers)}):")
        for provider in sorted(prop.supported_providers):
            attr = prop.get_key_for_provider(provider)
            print(f"    - {provider} → {attr}")


async def example_snowflake_stream(auth, stream_id):
    """Example: Accessing Snowflake stream properties."""
    print("\n" + "=" * 80)
    print("Example 1: Snowflake Stream")
    print("=" * 80)

    stream = await DomoStream.get_by_id(auth, stream_id, is_get_account=False)

    print(f"\nStream ID: {stream.id}")
    print(f"Provider: {stream.data_provider_key}")
    print(f"Display URL: {stream.display_url}")

    # Conformed properties
    print("\nConformed Properties:")
    print(f"  SQL Query: {stream.sql[:80] if stream.sql else 'N/A'}...")
    print(f"  Database: {stream.database or 'N/A'}")
    print(f"  Schema: {stream.schema or 'N/A'}")
    print(f"  Warehouse: {stream.warehouse or 'N/A'}")

    # Direct typed config access (provider-specific)
    if stream.typed_config:
        print("\nTyped Config (provider-specific):")
        print(f"  Type: {type(stream.typed_config).__name__}")
        print(f"  Query: {stream.typed_config.query[:80] if stream.typed_config.query else 'N/A'}...")


async def example_cross_platform(auth, stream_ids: list[str]):
    """Example: Processing multiple streams regardless of provider."""
    print("\n" + "=" * 80)
    print("Example 2: Cross-Platform Stream Processing")
    print("=" * 80)

    for stream_id in stream_ids:
        try:
            stream = await DomoStream.get_by_id(auth, stream_id, is_get_account=False)

            print(f"\nStream: {stream.id}")
            print(f"  Provider: {stream.data_provider_key}")

            # Works for any SQL-based provider
            if stream.sql:
                print(f"  ✓ Has SQL query")
                print(f"    Database: {stream.database or 'default'}")
                if stream.warehouse:
                    print(f"    Warehouse: {stream.warehouse}")

            # Works for reporting providers
            elif stream.report_id:
                print(f"  ✓ Analytics/Reporting connector")
                print(f"    Report ID: {stream.report_id}")

            # Works for spreadsheet providers
            elif stream.spreadsheet:
                print(f"  ✓ Spreadsheet connector")
                print(f"    Spreadsheet: {stream.spreadsheet}")

            else:
                print(f"  ⚠ No SQL/report/spreadsheet properties available")

        except Exception as e:
            print(f"  ✗ Error: {e}")


def example_property_inspection():
    """Example: Inspecting conformed property support."""
    print("\n" + "=" * 80)
    print("Example 3: Property Support Inspection")
    print("=" * 80)

    # Check which providers support SQL queries
    query_prop = CONFORMED_PROPERTIES["query"]
    print(f"\nSQL Query Support:")
    print(f"  Providers supporting SQL queries: {len(query_prop.supported_providers)}")
    for provider in sorted(query_prop.supported_providers):
        print(f"    - {provider}")

    # Check warehouse support (Snowflake-specific)
    warehouse_prop = CONFORMED_PROPERTIES["warehouse"]
    print(f"\nWarehouse Support:")
    print(f"  Providers with warehouses: {len(warehouse_prop.supported_providers)}")
    for provider in sorted(warehouse_prop.supported_providers):
        print(f"    - {provider}")

    # Check reporting support
    report_prop = CONFORMED_PROPERTIES["report_id"]
    print(f"\nReporting Support:")
    print(f"  Providers with report IDs: {len(report_prop.supported_providers)}")
    for provider in sorted(report_prop.supported_providers):
        print(f"    - {provider}")


if __name__ == "__main__":
    # Show available properties
    show_available_properties()

    # Property inspection example
    example_property_inspection()

    # Note: To run async examples, uncomment and provide auth + stream IDs:
    #
    # import os
    # from dotenv import load_dotenv
    # import domolibrary2.auth as dmda
    #
    # load_dotenv()
    # token_auth = dmda.DomoTokenAuth(
    #     domo_instance=os.environ["DOMO_INSTANCE"],
    #     domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    # )
    #
    # # Example with single stream
    # asyncio.run(example_snowflake_stream(
    #     auth=token_auth,
    #     stream_id=os.environ["STREAM_ID_1"]
    # ))
    #
    # # Example with multiple streams
    # asyncio.run(example_cross_platform(
    #     auth=token_auth,
    #     stream_ids=[
    #         os.environ["STREAM_ID_1"],  # Snowflake
    #         os.environ["STREAM_ID_2"],  # AWS Athena
    #         os.environ["STREAM_ID_3"],  # Google Sheets
    #     ]
    # ))

    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
