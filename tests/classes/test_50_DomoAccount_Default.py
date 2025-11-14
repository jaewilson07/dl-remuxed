"""
Test file for DomoAccount_Default class.

Tests the Account_Default class to ensure it follows domolibrary2 design patterns
and standards.
"""

import os

from dotenv import load_dotenv

import domolibrary2.classes.DomoAccount.Account_Default as dmac
import domolibrary2.client.auth as dmda
import domolibrary2.routes.account as account_routes

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", ""),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", ""),
)

# Test account IDs - set these in your .env file
TEST_ACCOUNT_ID_1 = int(os.environ.get("ACCOUNT_DEFAULT_ID_1", 0))
TEST_ACCOUNT_ID_2 = int(os.environ.get("ACCOUNT_DEFAULT_ID_2", 0))


async def test_cell_0(token_auth=token_auth) -> dmda.DomoTokenAuth:
    """Helper function to verify authentication is set up correctly."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    assert token_auth.user_id is not None, "Authentication failed"
    return token_auth


async def test_cell_1(token_auth=token_auth) -> dmac.DomoAccount_Default:
    """Test get_by_id method - retrieves an account by its ID."""
    if TEST_ACCOUNT_ID_1 == 0:
        print("Skipping test - ACCOUNT_DEFAULT_ID_1 not set in .env")
        return None

    domo_account = await dmac.DomoAccount_Default.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        is_suppress_no_config=True,
        debug_api=False,
        return_raw=False,
    )

    assert domo_account is not None, "Failed to retrieve account"
    assert domo_account.id == TEST_ACCOUNT_ID_1, "Account ID mismatch"
    assert domo_account.auth == token_auth, "Auth mismatch"

    print(f"Successfully retrieved account: {domo_account.name}")
    return domo_account


async def test_cell_2(token_auth=token_auth) -> dmac.DomoAccount_Default:
    """Test from_dict method - creates account object from dictionary."""
    # First get an account to use its raw data
    if TEST_ACCOUNT_ID_1 == 0:
        print("Skipping test - ACCOUNT_DEFAULT_ID_1 not set in .env")
        return None

    # Get account data from route
    res = await account_routes.get_account_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        debug_api=False,
    )

    # Create account from dictionary
    domo_account = dmac.DomoAccount_Default.from_dict(
        auth=token_auth,
        obj=res.response,
        is_admin_summary=False,
        is_use_default_account_class=True,
    )

    assert domo_account is not None, "Failed to create account from dict"
    assert domo_account.id == TEST_ACCOUNT_ID_1, "Account ID mismatch"
    assert domo_account.name == res.response.get("displayName"), "Name mismatch"

    print(f"Successfully created account from dict: {domo_account.name}")
    return domo_account


async def test_cell_3(token_auth=token_auth):
    """Test display_url method - returns URL to account in Domo."""
    if TEST_ACCOUNT_ID_1 == 0:
        print("Skipping test - ACCOUNT_DEFAULT_ID_1 not set in .env")
        return

    domo_account = await dmac.DomoAccount_Default.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
    )

    url = domo_account.display_url()

    assert url is not None, "display_url returned None"
    assert token_auth.domo_instance in url, "Instance not in URL"
    assert "datacenter/accounts" in url, "Expected path not in URL"

    print(f"Account URL: {url}")
    return url


async def test_cell_4(token_auth=token_auth):
    """Test Access subentity - verifies DomoAccess_Account is initialized."""
    if TEST_ACCOUNT_ID_1 == 0:
        print("Skipping test - ACCOUNT_DEFAULT_ID_1 not set in .env")
        return

    domo_account = await dmac.DomoAccount_Default.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
    )

    assert domo_account.Access is not None, "Access subentity not initialized"
    assert domo_account.Access.parent_id == domo_account.id, "Parent ID mismatch"

    print("Access subentity properly initialized")
    return domo_account.Access


async def main(token_auth=token_auth):
    """Run all test functions."""
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
    ]

    for fn in fn_ls:
        print(f"\n=== Running {fn.__name__} ===")
        try:
            await fn(token_auth=token_auth)
            print(f"✓ {fn.__name__} passed")
        except Exception as e:
            print(f"✗ {fn.__name__} failed: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(token_auth=token_auth))
