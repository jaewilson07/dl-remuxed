"""
Test file for DomoAccount class following domolibrary2 patterns.

This test file validates the DomoAccount class structure, methods, and integration
with route functions according to domolibrary2 design patterns.
"""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
import domolibrary2.routes.account as account_routes
from domolibrary2.classes.DomoAccount import (
    DomoAccount,
    DomoAccounts,
)

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", ""),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", ""),
)

# Test constants - update these in your .env file
TEST_ACCOUNT_ID = int(os.environ.get("TEST_ACCOUNT_ID", "0"))


@pytest.mark.asyncio
async def test_cell_0() -> str:
    """Helper function to get account list for finding test IDs."""
    if not token_auth.domo_instance:
        pytest.skip("DOMO_INSTANCE not configured")

    # Get first few accounts to validate API connection
    res = await account_routes.get_accounts(
        auth=token_auth,
        debug_api=False,
        return_raw=True,
    )

    assert res.is_success, "Failed to retrieve accounts from API"
    assert len(res.response) > 0, "No accounts available for testing"

    return res.response[0].get("id")


@pytest.mark.asyncio
async def test_get_by_id():
    """Test DomoAccount.get_by_id() method."""
    if not TEST_ACCOUNT_ID:
        pytest.skip("TEST_ACCOUNT_ID not configured in .env")

    domo_account = await DomoAccount.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID,
        is_use_default_account_class=True,
        return_raw=False,
    )

    # Validate structure
    assert domo_account is not None
    assert domo_account.id == TEST_ACCOUNT_ID
    assert domo_account.auth == token_auth
    assert hasattr(domo_account, "name")
    assert hasattr(domo_account, "data_provider_type")
    assert hasattr(domo_account, "display_url")
    assert hasattr(domo_account, "Access")

    # Validate display_url returns proper format
    url = domo_account.display_url()
    assert token_auth.domo_instance in url
    assert "datacenter/accounts" in url


@pytest.mark.asyncio
async def test_from_dict():
    """Test DomoAccount.from_dict() method."""
    # Create sample account data
    sample_data = {
        "id": 12345,
        "displayName": "Test Account",
        "dataProviderType": "abstract-credential-store",
        "createdAt": 1640000000000,
        "modifiedAt": 1640000000000,
    }

    domo_account = DomoAccount.from_dict(
        obj=sample_data,
        auth=token_auth,
        is_admin_summary=True,
        is_use_default_account_class=True,
    )

    # Validate conversion
    assert domo_account is not None
    assert domo_account.id == 12345
    assert domo_account.name == "Test Account"
    assert domo_account.data_provider_type == "abstract-credential-store"
    assert domo_account.auth == token_auth
    assert domo_account.raw == sample_data


@pytest.mark.asyncio
async def test_accounts_manager_get():
    """Test DomoAccounts manager class get() method."""
    if not token_auth.domo_instance:
        pytest.skip("DOMO_INSTANCE not configured")

    domo_accounts = DomoAccounts(auth=token_auth)
    accounts = await domo_accounts.get(
        debug_api=False,
        return_raw=False,
        is_use_default_account_class=True,
    )

    # Validate manager functionality
    assert accounts is not None
    assert isinstance(accounts, list)
    assert len(accounts) > 0

    # Validate first account structure
    first_account = accounts[0]
    assert isinstance(first_account, DomoAccount)
    assert hasattr(first_account, "id")
    assert hasattr(first_account, "name")


@pytest.mark.asyncio
async def test_access_subentity():
    """Test DomoAccess_Account subentity integration."""
    if not TEST_ACCOUNT_ID:
        pytest.skip("TEST_ACCOUNT_ID not configured in .env")

    domo_account = await DomoAccount.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID,
        is_use_default_account_class=True,
    )

    # Validate Access subentity exists and is initialized
    assert domo_account.Access is not None
    assert hasattr(domo_account.Access, "parent")
    assert hasattr(domo_account.Access, "parent_id")
    assert domo_account.Access.parent_id == TEST_ACCOUNT_ID


@pytest.mark.asyncio
async def test_account_display_url():
    """Test display_url() method returns proper URL format."""
    if not TEST_ACCOUNT_ID:
        pytest.skip("TEST_ACCOUNT_ID not configured in .env")

    domo_account = await DomoAccount.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID,
        is_use_default_account_class=True,
    )

    url = domo_account.display_url()

    # Validate URL format
    assert url is not None
    assert isinstance(url, str)
    assert token_auth.domo_instance in url
    assert "datacenter/accounts" in url


if __name__ == "__main__":
    """Run tests when executed directly."""
    import asyncio

    async def run_tests():
        print("Running DomoAccount tests...")
        print("\n--- Test 0: Get Account list ---")
        account_id = await test_cell_0()
        print(f"Found account ID: {account_id}")

        print("\n--- Test 1: Get by ID ---")
        await test_get_by_id()
        print("✓ get_by_id() test passed")

        print("\n--- Test 2: From Dict ---")
        await test_from_dict()
        print("✓ from_dict() test passed")

        print("\n--- Test 3: Accounts Manager ---")
        await test_accounts_manager_get()
        print("✓ DomoAccounts.get() test passed")

        print("\n--- Test 4: Access Subentity ---")
        await test_access_subentity()
        print("✓ Access subentity test passed")

        print("\n--- Test 5: Display URL ---")
        await test_account_display_url()
        print("✓ display_url() test passed")

        print("\n✅ All tests completed successfully!")

    asyncio.run(run_tests())
