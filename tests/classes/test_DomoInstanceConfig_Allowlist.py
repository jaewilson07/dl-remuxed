"""
Test file for DomoInstanceConfig Allowlist class
Tests the DomoAllowlist class methods and route integration

Environment Variables Required:
    DOMO_INSTANCE: Your Domo instance name (e.g., "mycompany")
    DOMO_ACCESS_TOKEN: A valid Domo access token with appropriate permissions
    
How to Obtain Test Values:
    1. Navigate to your Domo instance
    2. Go to Admin > Security > IP Allowlist
    3. You'll need an access token with admin permissions to manage the allowlist
    
Running Tests:
    # Run unit tests only (no API calls)
    pytest tests/classes/test_DomoInstanceConfig_Allowlist.py -m "not integration"
    
    # Run all tests including integration tests (requires valid credentials)
    pytest tests/classes/test_DomoInstanceConfig_Allowlist.py
    
Note:
    Integration tests that modify the allowlist are commented out to prevent
    accidental changes. Uncomment them carefully for manual testing.
"""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.classes.DomoInstanceConfig.Allowlist as allowlist_module
import domolibrary2.client.auth as dmda

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_INSTANCE", ""),
    domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", ""),
)


@pytest.mark.asyncio
async def test_cell_0(token_auth=token_auth):
    """Test authentication setup"""
    assert token_auth.domo_instance, "DOMO_INSTANCE environment variable not set"
    assert token_auth.domo_access_token, "DOMO_ACCESS_TOKEN environment variable not set"
    return token_auth


@pytest.mark.asyncio
async def test_cell_1(token_auth=token_auth):
    """Test getting allowlist"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    result = await dmal.get(return_raw=False)
    assert isinstance(result, list), "Allowlist should return a list"
    assert dmal.allowlist is not None, "Allowlist should be populated after get()"
    return dmal


@pytest.mark.asyncio
async def test_cell_2(token_auth=token_auth):
    """Test from_dict method"""
    test_data = {
        "allowlist": ["192.168.1.1", "10.0.0.0/8"],
        "is_filter_all_traffic_enabled": True,
    }
    dmal = allowlist_module.DomoAllowlist.from_dict(auth=token_auth, obj=test_data)
    assert dmal.allowlist == test_data["allowlist"], "Allowlist should match input"
    assert (
        dmal.is_filter_all_traffic_enabled is True
    ), "Filter setting should match input"
    return dmal


@pytest.mark.asyncio
async def test_cell_3(token_auth=token_auth):
    """Test display_url property"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    url = dmal.display_url
    assert isinstance(url, str), "display_url should return a string"
    assert token_auth.domo_instance in url, "URL should contain instance name"
    assert "admin/security" in url, "URL should point to security settings"
    return url


@pytest.mark.asyncio
@pytest.mark.integration
async def test_cell_4(token_auth=token_auth):
    """Test adding IPs to allowlist (integration test - requires valid auth)"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    
    # Get current allowlist first
    current_list = await dmal.get()
    
    # This is a test that should be run carefully
    # test_ips = ['0.0.0.0/0']
    # await dmal.add_ips(test_ips)
    
    # Note: Commented out to prevent accidental modification
    # Uncomment and customize for actual testing
    return current_list


@pytest.mark.asyncio
@pytest.mark.integration
async def test_cell_5(token_auth=token_auth):
    """Test removing IPs from allowlist (integration test - requires valid auth)"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    
    # This is a test that should be run carefully
    # test_ips = ['0.0.0.0/0']
    # await dmal.remove_ips(ip_address_ls=test_ips, debug_api=False)
    
    # Note: Commented out to prevent accidental modification
    # Uncomment and customize for actual testing
    pass


@pytest.mark.asyncio
@pytest.mark.integration
async def test_cell_6(token_auth=token_auth):
    """Test setting allowlist (integration test - requires valid auth)"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    
    # This is a test that should be run carefully
    # await dmal.set(ip_address_ls=[])
    
    # Note: Commented out to prevent accidental modification
    # Uncomment and customize for actual testing
    pass


@pytest.mark.asyncio
@pytest.mark.integration
async def test_cell_7(token_auth=token_auth):
    """Test getting filter all traffic setting"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    result = await dmal.get_is_filter_all_traffic_enabled()
    assert isinstance(result, bool), "Filter setting should return a boolean"
    return result


@pytest.mark.asyncio
@pytest.mark.integration  
async def test_cell_8(token_auth=token_auth):
    """Test toggling filter all traffic setting (integration test)"""
    dmal = allowlist_module.DomoAllowlist(auth=token_auth)
    
    # This is a test that should be run carefully
    # result = await dmal.toggle_is_filter_all_traffic_enabled(
    #     is_enabled=False, debug_prn=True, return_raw=True
    # )
    
    # Note: Commented out to prevent accidental modification
    # Uncomment and customize for actual testing
    pass


@pytest.mark.asyncio
async def test_validate_ip_or_cidr():
    """Test IP/CIDR validation function"""
    # Valid IPv4 address
    assert allowlist_module.validate_ip_or_cidr("192.168.1.1") is True
    
    # Valid CIDR notation
    assert allowlist_module.validate_ip_or_cidr("10.0.0.0/8") is True
    
    # Invalid IP should raise ValueError
    with pytest.raises(ValueError):
        allowlist_module.validate_ip_or_cidr("not.an.ip.address")
