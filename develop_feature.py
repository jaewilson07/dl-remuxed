from domolibrary2.utils import chunk_execution as dmce
from domolibrary2.classes import DomoDataset as dmds
from domolibrary2.classes import DomoDatacenter as dmdc
from domolibrary2.routes import codeengine as ce_routes
from dotenv import load_dotenv
import domolibrary2.auth as dmda
import os
import json

assert load_dotenv("./local_work/work/.env")

TEST_INSTANCE = "playstation-d2c"
# DATASET_ID = "b4fb2687-eb95-4417-aeaf-e44a1d1bc9bf"


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

    # Debug: print response structure
    print(f"CodeEngine Response: {res.response}")

    # Handle different response structures
    if isinstance(res.response, dict):
        if "properties" in res.response:
            access_token = res.response["properties"]["domoAccessToken"]
        elif "domoAccessToken" in res.response:
            access_token = res.response["domoAccessToken"]
        else:
            raise ValueError(f"Unexpected response structure: {res.response}")
    else:
        raise ValueError(f"Response is not a dict: {type(res.response)}")

    target_auth = dmda.DomoTokenAuth(
        domo_access_token=access_token,
        domo_instance=target_instance,
    )
    assert await target_auth.print_is_token(), "invalid auth stored in domo"
    return target_auth


def unique_datasets(datasets: list[dmds.DomoDataset]) -> list[dmds.DomoDataset]:
    seen_data_provider_type = set()

    unique_datasets = []

    for ds in datasets:
        if ds.data_provider_type not in seen_data_provider_type:
            seen_data_provider_type.add(ds.data_provider_type)
            unique_datasets.append(ds)

    return unique_datasets


async def main():

    config_auth = await get_auth("playstation-config", debug_api=False)
    target_auth = await get_auth_from_codeengine(config_auth, TEST_INSTANCE)

    # Get datasets and filter for snowflake ones
    print("\nFetching all datasets...")
    datasets = await dmdc.DomoDatacenter(auth=target_auth).search_datasets()

    print(f"Found {len(datasets)} total datasets")

    # Filter for snowflake datasets only
    snowflake_datasets = [
        ds
        for ds in datasets
        if ds.data_provider_type and "snowflake" in ds.data_provider_type.lower()
    ]
    print(f"Found {len(snowflake_datasets)} snowflake datasets")

    # Get unique by provider type
    unique_snowflake = []
    seen_types = set()
    for ds in snowflake_datasets:
        if ds.data_provider_type not in seen_types:
            seen_types.add(ds.data_provider_type)
            unique_snowflake.append(ds)

    print(f"\nUnique snowflake provider types: {len(unique_snowflake)}")
    for ds in unique_snowflake:
        print(f"  - {ds.data_provider_type}: {ds.name}")

    print("\n" + "=" * 80)
    print("Attempting to load streams for snowflake datasets...")
    print("=" * 80 + "\n")

    # Load streams using dataset_id as stream_id

    loaded_count = 0
    for ds in unique_snowflake:
        try:
            await ds.refresh(debug_api=False)
            await ds.Stream.refresh(debug_api=False)

            loaded_count += 1
            print(f"[OK] Loaded stream for [{ds.data_provider_type}]: {ds.name}")
        except Exception as e:
            print(f"[FAIL] Failed [{ds.data_provider_type}]: {ds.name}")
            print(f"       Error: {str(e)[:120]}")
            # Only print first failure in detail

    print(
        f"\n{'='*80}\nSuccessfully loaded {loaded_count} streams out of {len(unique_snowflake)} snowflake datasets\n{'='*80}\n"
    )

    with open("./dataset_streams.txt", "w", encoding="utf-8") as f:
        for ds in unique_snowflake:
            stream = ds.Stream

            f.write(f"Dataset: {ds.name} ({ds.id})\n")
            f.write(f"  Data Provider: {ds.data_provider_type}\n")
            f.write(f"  Stream ID: {stream.id}\n")
            f.write(
                f"  Provider: {stream.data_provider_name or stream.data_provider_key}\n"
            )

            f.write(f"\n  Configuration:\n")
            if stream.configuration:
                for config in stream.configuration:
                    f.write(f"    {config.to_dict()}\n")

            # Show conformed properties (NEW FEATURE!)
            f.write(f"\n  Conformed Properties:\n")
            if stream.sql:
                f.write(
                    f"    SQL: {stream.sql[:100]}...\n"
                    if len(stream.sql) > 100
                    else f"    SQL: {stream.sql}\n"
                )
            if stream.database:
                f.write(f"    Database: {stream.database}\n")
            if stream.warehouse:
                f.write(f"    Warehouse: {stream.warehouse}\n")
            if stream.schema:
                f.write(f"    Schema: {stream.schema}\n")
            if stream.table:
                f.write(f"    Table: {stream.table}\n")
            if stream.report_id:
                f.write(f"    Report ID: {stream.report_id}\n")
            if stream.spreadsheet:
                f.write(f"    Spreadsheet: {stream.spreadsheet}\n")
            if stream.bucket:
                f.write(f"    Bucket: {stream.bucket}\n")
            if stream.dataset_id:
                f.write(f"    Dataset ID: {stream.dataset_id}\n")
            if stream.file_url:
                f.write(f"    File URL: {stream.file_url}\n")
            if stream.host:
                f.write(f"    Host: {stream.host}\n")
            if stream.port:
                f.write(f"    Port: {stream.port}\n")

            # Show the complete stream representation
            f.write(f"\n  Stream Repr:\n")
            f.write(f"    {repr(stream)}\n")

            # Show discovery properties (NEW FEATURES!)
            f.write(f"\n  Discovery:\n")
            missing = stream._missing_mappings
            available = stream._available_config_keys
            f.write(f"    Missing Mappings: {missing if missing else 'None'}\n")
            f.write(
                f"    Available Config Keys: {available if available else 'None'}\n"
            )

            f.write("\n" + "=" * 80 + "\n\n")

    print(f"Wrote stream information to ./dataset_streams.txt")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
