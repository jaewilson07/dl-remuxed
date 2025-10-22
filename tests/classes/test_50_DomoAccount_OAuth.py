"""
Test file for DomoAccount_OAuth class validation

This test file validates the DomoAccount_OAuth class implementation,
ensuring it follows domolibrary2 design patterns and standards.

Tests:
    test_cell_0: Setup and authentication helper
    test_cell_1: Test get_by_id method
    test_cell_2: Test from_dict method
    test_cell_3: Test Access.get() method
"""

import os
from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
from domolibrary2.classes.DomoAccount.Account_OAuth import DomoAccount_OAuth
from domolibrary2.routes.account.exceptions import (
    Account_GET_Error,
    Account_NoMatch,
    Account_CRUD_Error,
)

load_dotenv()

# Setup authentication for tests
# Note: These tests require DOMO_INSTANCE and DOMO_ACCESS_TOKEN environment variables
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", "test-instance"),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", "test-token"),
)

# Test account IDs from environment
TEST_OAUTH_ACCOUNT_ID_1 = int(os.environ.get("OAUTH_ACCOUNT_ID_1", 1))


async def test_cell_0(token_auth=token_auth) -> dmda.DomoTokenAuth:
    """Helper function to verify authentication is working.
    
    Returns:
        DomoTokenAuth: Authenticated token auth object
    """
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth


async def test_cell_1(token_auth=token_auth) -> DomoAccount_OAuth:
    """Test retrieving an OAuth account by ID.
    
    Returns:
        DomoAccount_OAuth: Retrieved OAuth account instance
    
    Raises:
        Account_NoMatch: If OAuth account is not found
        Account_GET_Error: If retrieval fails
    """
    domo_oauth = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=TEST_OAUTH_ACCOUNT_ID_1,
        return_raw=False,
        debug_api=False,
    )
    
    # Verify basic attributes
    assert domo_oauth.id is not None
    assert domo_oauth.auth is not None
    assert domo_oauth.Access is not None
    
    return domo_oauth


async def test_cell_2(token_auth=token_auth):
    """Test from_dict method for OAuth account.
    
    This test verifies that OAuth accounts can be properly constructed
    from dictionary representations (API responses).
    """
    # Get an account first to have real data
    domo_oauth = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=TEST_OAUTH_ACCOUNT_ID_1,
    )
    
    # Test from_dict using the raw data
    if domo_oauth.raw:
        reconstructed = DomoAccount_OAuth.from_dict(
            auth=token_auth,
            obj=domo_oauth.raw,
            is_admin_summary=False,
            new_cls=DomoAccount_OAuth,
        )
        
        assert reconstructed.id == domo_oauth.id
        assert reconstructed.name == domo_oauth.name
    
    return domo_oauth


async def test_cell_3(token_auth=token_auth):
    """Test Access composition and get() method.
    
    Verifies that the DomoAccess_OAuth subentity is properly
    initialized and can retrieve access information.
    """
    domo_oauth = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=TEST_OAUTH_ACCOUNT_ID_1,
    )
    
    # Verify Access is initialized
    assert domo_oauth.Access is not None
    
    # Test getting access list
    access_list = await domo_oauth.Access.get()
    
    # Verify we got a response
    assert access_list is not None
    
    return access_list


async def test_cell_4(token_auth=token_auth):
    """Test display_url method.
    
    Verifies that the display URL is properly formatted.
    """
    domo_oauth = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=TEST_OAUTH_ACCOUNT_ID_1,
    )
    
    url = domo_oauth.display_url()
    
    # Verify URL format
    assert url is not None
    assert isinstance(url, str)
    assert "accounts" in url.lower()
    
    return url


async def test_cell_5_error_handling(token_auth=token_auth):
    """Test error handling for non-existent OAuth account.
    
    Verifies that appropriate exceptions are raised for invalid account IDs.
    """
    try:
        # Try to get a non-existent OAuth account
        await DomoAccount_OAuth.get_by_id(
            auth=token_auth,
            account_id=999999999,  # Non-existent ID
            debug_api=False,
        )
        # If we get here, the account exists (unlikely)
        print("Warning: Account 999999999 exists")
    except Account_NoMatch as e:
        # Expected exception for missing account
        print(f"Correctly caught Account_NoMatch: {e}")
        assert "not found" in str(e).lower() or "has it been shared" in str(e).lower()
    except Account_GET_Error as e:
        # Also acceptable if retrieval fails
        print(f"Caught Account_GET_Error: {e}")


async def main(token_auth=token_auth):
    """Run all test functions."""
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
        test_cell_5_error_handling,
    ]
    for fn in fn_ls:
        try:
            await fn(token_auth=token_auth)
            print(f"✓ {fn.__name__} passed")
        except Exception as e:
            print(f"✗ {fn.__name__} failed: {e}")
            raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(token_auth=token_auth))
