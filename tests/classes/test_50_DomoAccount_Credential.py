"""
Test file for DomoAccount_Credential class.

This module tests credential management functionality for Domo accounts including
authentication testing, password management, and access token operations.
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoAccount.Account_Credential as dmac

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", ""),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", ""),
)

# Test account IDs from environment
TEST_ACCOUNT_ID_1 = int(os.environ.get("ACCOUNT_CREDENTIAL_ID_1", 0))
TEST_TARGET_INSTANCE = os.environ.get("ACCOUNT_TARGET_INSTANCE", "")


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to verify authentication is valid."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1(token_auth=token_auth) -> dmac.DomoAccount_Credential:
    """Test retrieving an account credential by ID using get_by_id."""
    if not TEST_ACCOUNT_ID_1:
        print("Skipping test_cell_1: ACCOUNT_CREDENTIAL_ID_1 not set in environment")
        return None
    
    account_credential = await dmac.DomoAccount_Credential.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        is_suppress_no_config=True,
        debug_api=False,
        return_raw=False,
    )
    
    print(f"Retrieved account: {account_credential.name} (ID: {account_credential.id})")
    print(f"Data provider type: {account_credential.data_provider_type}")
    
    return account_credential


async def test_cell_2(token_auth=token_auth):
    """Test creating an account credential from dictionary representation."""
    # Sample account data structure
    account_data = {
        "id": 999,
        "displayName": "Test Account",
        "dataProviderType": "test-provider",
        "createdAt": 1234567890000,
        "modifiedAt": 1234567890000,
    }
    
    account_credential = dmac.DomoAccount_Credential.from_dict(
        auth=token_auth,
        obj=account_data,
        is_admin_summary=True,
        target_instance=TEST_TARGET_INSTANCE,
    )
    
    print(f"Created account from dict: {account_credential.name}")
    print(f"Target instance: {account_credential.target_instance}")
    
    return account_credential


async def test_cell_3(token_auth=token_auth):
    """Test account credential methods: set_password, set_username, set_access_token."""
    if not TEST_ACCOUNT_ID_1:
        print("Skipping test_cell_3: ACCOUNT_CREDENTIAL_ID_1 not set in environment")
        return None
    
    account_credential = await dmac.DomoAccount_Credential.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        is_suppress_no_config=True,
    )
    
    # Test setter methods (these update in memory, not persisted yet)
    account_credential.set_username("test_user@example.com")
    account_credential.set_password("test_password")
    account_credential.set_access_token("test_token_value")
    
    print(f"Updated credential setters for account: {account_credential.name}")
    print(f"Config username: {account_credential.Config.username if account_credential.Config else 'No config'}")
    
    return account_credential


async def test_cell_4(token_auth=token_auth):
    """Test display_url property."""
    if not TEST_ACCOUNT_ID_1:
        print("Skipping test_cell_4: ACCOUNT_CREDENTIAL_ID_1 not set in environment")
        return None
    
    account_credential = await dmac.DomoAccount_Credential.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        is_suppress_no_config=True,
    )
    
    display_url = account_credential.display_url()
    print(f"Display URL: {display_url}")
    
    return display_url


async def test_cell_5(token_auth=token_auth):
    """Test to_dict method for credential information."""
    if not TEST_ACCOUNT_ID_1:
        print("Skipping test_cell_5: ACCOUNT_CREDENTIAL_ID_1 not set in environment")
        return None
    
    account_credential = await dmac.DomoAccount_Credential.get_by_id(
        auth=token_auth,
        account_id=TEST_ACCOUNT_ID_1,
        is_suppress_no_config=True,
    )
    
    credential_dict = account_credential.to_dict()
    print(f"Credential dictionary: {credential_dict}")
    
    return credential_dict

