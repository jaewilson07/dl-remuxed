from domolibrary2.utils import chunk_execution as dmce
from domolibrary2.classes import DomoAccount as dmac
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


def unique_accounts(accounts: list[dmda.DomoAaccount]) -> list[dmds.DomoAccount]:
    seen_data_provider_type = set()

    unique_accounts = []

    for acc in accounts:
        if acc.data_provider_type not in seen_data_provider_type:
            seen_data_provider_type.add(acc.data_provider_type)
            unique_accounts.append(acc)

    return unique_accounts


async def main():

    config_auth = await get_auth("playstation-config", debug_api=False)
    target_auth = await get_auth_from_codeengine(config_auth, TEST_INSTANCE)

    # Get datasets and filter for snowflake ones
    print("\nFetching all datasets...")
    accounts = await dmac.DomoAccounts(auth=target_auth).get()

    print(f"Found {len(accounts)} total accounts")

    # Filter for snowflake datasets only
    snowflake_accounts = [
        acc
        for acc in accounts
        if acc.data_provider_type and "snowflake" in acc.data_provider_type.lower()
    ]
    print(f"Found {len(snowflake_accounts)} snowflake accounts")

    # Get unique by provider type
    unique_snowflake = []
    seen_types = set()
    for acc in snowflake_accounts:
        if acc.data_provider_type not in seen_types:
            seen_types.add(acc.data_provider_type)
            unique_snowflake.append(acc)

    print(f"\nUnique snowflake provider types: {len(unique_snowflake)}")
    for acc in unique_snowflake:
        print(f"  - {acc.data_provider_type}: {acc.name}")
    print("\n" + "=" * 80)
    print("Attempting to load streams for snowflake accounts...")
    print("=" * 80 + "\n")

    # Load streams using dataset_id as stream_id

    loaded_count = 0
    for acc in unique_snowflake:
        try:
            await acc._get_config()

            loaded_count += 1
            print(f"[OK] Loaded stream for [{acc.data_provider_type}]: {acc.name}")
        except Exception as e:
            print(f"[FAIL] Failed [{acc.data_provider_type}]: {acc.name}")
            print(f"       Error: {str(e)[:120]}")
            # Only print first failure in detail

    print(
        f"\n{'='*80}\nSuccessfully loaded {loaded_count} streams out of {len(unique_snowflake)} snowflake datasets\n{'='*80}\n"
    )

    with open("./account_config.txt", "w", encoding="utf-8") as f:
        for acc in unique_snowflake:

            f.write(f"Account: {acc.name} ({acc.id})\n")
            f.write(f"  Data Provider: {acc.data_provider_type}\n")

            f.write(f"\n  Configuration:\n")
            if acc.Config:
                f.write(f"    Config Object: {acc.Config}\n")
                f.write(f"    Config to_dict: {acc.Config.to_dict()}\n")

            if acc.raw and acc.raw.get("properties"):
                f.write(f"\n  Raw Properties:\n")
                for key, value in acc.raw.get("properties", {}).items():
                    f.write(f"    {key}: {value}\n")

            f.write("\n" + "=" * 80 + "\n\n")

    print(f"Wrote stream information to ./dataset_streams.txt")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
