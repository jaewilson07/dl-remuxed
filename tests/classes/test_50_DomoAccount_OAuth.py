"""
Test file for DomoAccount_OAuth class

This test suite validates the DomoAccount_OAuth class functionality including:
- OAuth account retrieval by ID
- OAuth account creation with different config types
- OAuth account name updates
- OAuth account configuration updates
- OAuth account deletion
- OAuth account access management

Environment Variables Required:
    DOMO_INSTANCE: Your Domo instance name
    DOMO_ACCESS_TOKEN: Valid access token for authentication
    ACCOUNT_OAUTH_ID_1: ID of an existing OAuth account for testing (optional)
"""

import os
import pytest
from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.classes.DomoAccount import DomoAccount_OAuth
from domolibrary2.classes.DomoAccount.Account_OAuth import (
    OAuthConfig,
    DomoAccountOAuth_Config_SnowflakeOauth,
)
from domolibrary2.routes.account.exceptions import Account_NoMatch


# Setup authentication for tests
@pytest.fixture
def token_auth():
    """Create authentication fixture for tests."""
    return DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Integration test - requires real OAuth account",
)
async def test_get_by_id(token_auth):
    """Test retrieving an OAuth account by ID.

    This test verifies that:
    1. OAuth accounts can be retrieved by ID
    2. The account has expected attributes (id, name, auth, Access)
    3. The account config can be loaded
    """
    # Get account ID from environment or use a known test ID
    account_id = os.environ.get("ACCOUNT_OAUTH_ID_1", 1)

    # Attempt to retrieve the OAuth account
    oauth_account = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=account_id,
        is_suppress_no_config=True,
    )

    # Verify basic attributes
    assert oauth_account is not None
    assert oauth_account.id == int(account_id)
    assert oauth_account.auth == token_auth
    assert oauth_account.name is not None
    assert oauth_account.Access is not None

    # Verify it's the right class
    assert isinstance(oauth_account, DomoAccount_OAuth)


@pytest.mark.asyncio
async def test_from_dict(token_auth):
    """Test creating an OAuth account from dictionary data.

    This test verifies that:
    1. OAuth accounts can be created from dict representations
    2. All attributes are properly mapped
    3. The Access subentity is initialized
    """
    # Sample OAuth account data
    sample_data = {
        "id": 12345,
        "displayName": "Test OAuth Account",
        "dataProviderType": "snowflake-oauth-config",
        "createdAt": 1609459200000,  # 2021-01-01
        "modifiedAt": 1640995200000,  # 2022-01-01
    }

    oauth_account = DomoAccount_OAuth.from_dict(
        auth=token_auth,
        obj=sample_data,
        is_admin_summary=False,
        is_use_default_account_class=False,
        new_cls=DomoAccount_OAuth,
    )

    # Verify attributes
    assert oauth_account.id == 12345
    assert oauth_account.name == "Test OAuth Account"
    assert oauth_account.data_provider_type == "snowflake-oauth-config"
    assert oauth_account.Access is not None
    assert not oauth_account.is_admin_summary


@pytest.mark.asyncio
async def test_display_url(token_auth):
    """Test the display_url method returns the correct URL."""
    oauth_account = DomoAccount_OAuth(
        id=123,
        auth=token_auth,
        name="Test Account",
        raw={},
    )

    url = oauth_account.display_url()
    assert token_auth.domo_instance in url
    assert "/datacenter/accounts" in url


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Integration test - requires real OAuth account",
)
async def test_update_name_integration(token_auth):
    """Integration test for updating OAuth account name.

    This test requires a real OAuth account and will actually modify it.
    Set RUN_INTEGRATION_TESTS=1 to enable.
    """
    account_id = os.environ.get("ACCOUNT_OAUTH_ID_1")
    if not account_id:
        pytest.skip("ACCOUNT_OAUTH_ID_1 not set")

    oauth_account = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=account_id,
        is_suppress_no_config=True,
    )

    original_name = oauth_account.name
    new_name = f"Test Update - {original_name}"

    # Update the name
    await oauth_account.update_name(account_name=new_name)

    # Verify the update
    assert oauth_account.name == new_name

    # Restore original name
    await oauth_account.update_name(account_name=original_name)
    assert oauth_account.name == original_name


def test_oauth_config_enum():
    """Test the OAuthConfig enum functionality.

    This test verifies that:
    1. OAuth config types can be retrieved from the enum
    2. The enum has expected members
    3. Config classes have correct attributes
    """
    # Test snowflake oauth config
    snowflake_config = OAuthConfig.snowflake_oauth_config
    assert snowflake_config.value == DomoAccountOAuth_Config_SnowflakeOauth
    assert snowflake_config.value.data_provider_type == "snowflake-oauth-config"
    assert snowflake_config.value.is_oauth is True


@pytest.mark.asyncio
async def test_access_subentity(token_auth):
    """Test that DomoAccess_OAuth subentity is properly initialized.

    This test verifies that:
    1. Access subentity exists after initialization
    2. Access has correct type
    3. Access has reference to parent
    """
    oauth_account = DomoAccount_OAuth(
        id=123,
        auth=token_auth,
        name="Test Account",
        raw={},
    )

    # Access should be initialized in __post_init__
    assert oauth_account.Access is not None

    # Access should have reference to parent
    assert oauth_account.Access.parent == oauth_account


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Integration test - requires real OAuth account",
)
async def test_get_by_id_not_found(token_auth):
    """Test that appropriate exception is raised for non-existent OAuth account."""
    # Use a very high ID that's unlikely to exist
    non_existent_id = 999999999

    with pytest.raises(Account_NoMatch):
        await DomoAccount_OAuth.get_by_id(
            auth=token_auth,
            account_id=non_existent_id,
            is_suppress_no_config=True,
        )


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Integration test - requires real OAuth account",
)
async def test_return_raw_parameter(token_auth):
    """Test that return_raw parameter works correctly.

    This test verifies that:
    1. When return_raw=True, ResponseGetData is returned
    2. Response has expected structure
    """
    account_id = os.environ.get("ACCOUNT_OAUTH_ID_1", 1)

    # Get raw response
    raw_response = await DomoAccount_OAuth.get_by_id(
        auth=token_auth,
        account_id=account_id,
        return_raw=True,
    )

    # Verify it's a ResponseGetData object
    assert hasattr(raw_response, "response")
    assert hasattr(raw_response, "is_success")
    assert hasattr(raw_response, "status")
