"""
Example: Share Domo Accounts with CodeEngine Package

This example demonstrates how to share Domo accounts with a CodeEngine package,
allowing the package to access specific accounts via aliases.
"""

import asyncio
import os

from dotenv import load_dotenv

import domolibrary2.auth as dmda
from domolibrary2.routes import codeengine as ce_routes

# Load environment variables
load_dotenv()


async def main():
    """Share accounts with a CodeEngine package."""
    # Initialize authentication
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    # Package ID to share accounts with
    package_id = "b368d630-7ca5-4b8a-b4ec-f130cf312dc1"

    # Define account mappings
    # Each mapping contains an accountId and an alias that the package can use
    account_mappings = [
        {"accountId": 92, "alias": "sdk_playstation-config"},
        {"accountId": 189, "alias": "sdk_playstation-d2c"},
        {"accountId": 366, "alias": "sdk_playstation-audit"},
        {"accountId": "231", "alias": "sdk_playstation-ae"},  # Can be string or int
    ]

    try:
        # Replace all account mappings (is_set=True, default behavior)
        result = await ce_routes.share_accounts_with_package(
            auth=auth,
            package_id=package_id,
            account_mappings=account_mappings,
            is_set=True,  # Replace all existing mappings
            debug_api=False,  # Set to True to see API request details
        )

        print(f"✅ Successfully set {len(account_mappings)} accounts for package")
        print(f"Package ID: {package_id}")
        print("\nShared accounts:")
        for mapping in account_mappings:
            print(f"  - Account {mapping['accountId']}: {mapping['alias']}")

        # Optionally print the full response
        if result.response:
            manifest = result.response.get("manifest", {})
            config = manifest.get("configuration", {})
            actual_mappings = config.get("accountsMapping", [])
            print(f"\nConfirmed {len(actual_mappings)} accounts in package manifest")

    except ce_routes.CodeEngine_GET_Error as e:
        print(f"❌ Failed to retrieve package: {e}")
    except ce_routes.CodeEngine_CRUD_Error as e:
        print(f"❌ Failed to share accounts: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def example_add_accounts():
    """Example showing how to add accounts to existing mappings."""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    package_id = "b368d630-7ca5-4b8a-b4ec-f130cf312dc1"

    # First, set initial account mappings
    initial_accounts = [
        {"accountId": 92, "alias": "sdk_playstation-config"},
        {"accountId": 189, "alias": "sdk_playstation-d2c"},
    ]

    print("Setting initial accounts...")
    await ce_routes.share_accounts_with_package(
        auth=auth,
        package_id=package_id,
        account_mappings=initial_accounts,
        is_set=True,  # Replace all existing
    )
    print(f"✅ Set {len(initial_accounts)} initial accounts")

    # Now add more accounts without removing existing ones
    additional_accounts = [
        {"accountId": 366, "alias": "sdk_playstation-audit"},
        {"accountId": "231", "alias": "sdk_playstation-ae"},
    ]

    print("\nAdding additional accounts...")
    result = await ce_routes.share_accounts_with_package(
        auth=auth,
        package_id=package_id,
        account_mappings=additional_accounts,
        is_set=False,  # Add to existing
    )

    # Check final count
    if result.response:
        manifest = result.response.get("manifest", {})
        config = manifest.get("configuration", {})
        all_mappings = config.get("accountsMapping", [])
        print(f"✅ Added {len(additional_accounts)} accounts")
        print(f"Total accounts now: {len(all_mappings)}")
        print("\nAll shared accounts:")
        for mapping in all_mappings:
            print(f"  - Account {mapping['accountId']}: {mapping['alias']}")


async def example_with_session():
    """Example using a shared HTTP session for multiple operations."""
    import httpx

    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    package_id = "b368d630-7ca5-4b8a-b4ec-f130cf312dc1"
    account_mappings = [
        {"accountId": 92, "alias": "sdk_playstation-config"},
    ]

    # Use a shared session for better performance with multiple API calls
    async with httpx.AsyncClient() as session:
        # First, get the package details
        package = await ce_routes.get_codeengine_package_by_id(
            auth=auth,
            package_id=package_id,
            session=session,
        )

        print(f"Package name: {package.response.get('name')}")
        print(f"Package version: {package.response.get('version')}")

        # Then share accounts
        result = await ce_routes.share_accounts_with_package(
            auth=auth,
            package_id=package_id,
            account_mappings=account_mappings,
            is_set=True,  # Replace existing
            session=session,  # Reuse the same session
        )

        print(f"✅ Accounts shared successfully")


if __name__ == "__main__":
    # Run the main example (set/replace accounts)
    asyncio.run(main())

    # Uncomment to run the add accounts example
    # asyncio.run(example_add_accounts())

    # Uncomment to run the session example
    # asyncio.run(example_with_session())
