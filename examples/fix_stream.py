# Sample code from MONIT_account_retrieves_sql.ipynb
# This script demonstrates Snowflake account access cleanup and account mapping via Domo Code Engine

import asyncio
from dotenv import load_dotenv
import domolibrary2.auth as dmda
import os
import domolibrary2.classes.DomoAccount as dmac
import domolibrary2.routes.codeengine as ce_routes
import domolibrary2.classes.DomoDataset.stream as dmst
import domolibrary2.classes.DomoDataset as dmds
import domolibrary2.classes.DomoDatacenter as dmdc
import domolibrary2.utils.chunk_execution as dmce

# Configuration
TEST_INSTANCE = "playstation-d2c"

assert load_dotenv("./.env")
assert load_dotenv("./local_work/work/.env")


async def get_auth(domo_instance: str, debug_api: bool = False) -> dmda.DomoTokenAuth:
    auth = dmda.DomoTokenAuth(
        domo_access_token=os.environ[f"{domo_instance.upper()}_ACCESS_TOKEN"],
        domo_instance=domo_instance,
    )
    await auth.who_am_i(debug_api=debug_api)
    return auth


async def get_auth_from_codeengine(config_auth: dmda.DomoAuth, target_instance: str):
    SUDO_PACKAGE_ID = "b368d630-7ca5-4b8a-b4ec-f130cf312dc1"
    res = await ce_routes.execute_codeengine_function(
        auth=config_auth,
        package_id=SUDO_PACKAGE_ID,
        version="1.3.1",
        function_name="get_account",
        input_variables={"auth_name": f"sdk_{target_instance}"},
    )
    target_auth = dmda.DomoTokenAuth(
        domo_access_token=res.response["properties"]["domoAccessToken"],
        domo_instance=target_instance,
    )
    assert await target_auth.print_is_token(), "invalid auth stored in domo"
    return target_auth


async def get_datasets(
    target_auth, dataset_id: str = "b4fb2687-eb95-4417-aeaf-e44a1d1bc9bf"
):
    ds = await dmds.DomoDataset.get_by_id(auth=target_auth, dataset_id=dataset_id)

    stream = await ds.Stream.refresh()

    print("Stream Info:")
    print(f"  Provider: {stream.data_provider_name}")
    print(f"  Account: {stream.account_display_name}")
    print(f"  Update Method: {stream.update_method}")

    # NEW: Use typed config for type-safe access
    if stream.typed_config:
        print(f"\nTyped Config ({type(stream.typed_config).__name__}):")
        print(f"  Database: {stream.typed_config.database_name}")
        print(f"  Schema: {stream.typed_config.schema_name}")
        print(f"  Warehouse: {stream.typed_config.warehouse}")

        # NEW: Convenient sql property
        if stream.sql:
            print(f"  SQL: {stream.sql[:100]}...")

    return ds


async def main(
    test_instance: str = "playstation-d2c",
    dataset_id: str = "b4fb2687-eb95-4417-aeaf-e44a1d1bc9bf",
):

    config_auth = await get_auth("playstation-config", debug_api=False)

    target_auth = await get_auth_from_codeengine(config_auth, test_instance)

    ds = await get_datasets(target_auth=target_auth, dataset_id=dataset_id)

    # Stream was already refreshed in get_datasets(), so just access it
    stream = ds.Stream

    # Additional demonstration of new features
    print("\n" + "="*80)
    print("Stream Configuration Access Patterns:")
    print("="*80)

    # OLD Pattern: Search through list of StreamConfig objects
    print("\nOLD Pattern (list-based):")
    query_config = next((c for c in stream.configuration if c.name == 'query'), None)
    if query_config:
        print(f"  Found query via list search: {query_config.value[:50]}...")

    # NEW Pattern: Type-safe attribute access
    print("\nNEW Pattern (typed config):")
    if stream.typed_config:
        print(f"  Type-safe access: {stream.typed_config.query[:50]}...")
        print(f"  Convenience property: {stream.sql[:50]}...")

    print(stream)


if __name__ == "__main__":
    asyncio.run(main())
