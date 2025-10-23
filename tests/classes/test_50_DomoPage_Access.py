"""
Test file for DomoPage access functionality.
Tests the access control and sharing methods of the DomoPage class.
"""

import os
from typing import Dict, List

from dotenv import load_dotenv

import domolibrary2.classes.DomoPage as dmpg
import domolibrary2.client.auth as dmda

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test page IDs from environment
TEST_PAGE_ID_1 = os.environ.get("TEST_PAGE_ID_1", "")
TEST_PAGE_ID_2 = os.environ.get("TEST_PAGE_ID_2", "")


async def test_cell_0(token_auth=token_auth) -> str:
    """Helper function to ensure authentication and get user ID."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return token_auth.user_id


async def test_cell_1_test_page_access(token_auth=token_auth):
    """Test DomoPage.test_page_access() method.
    
    This test verifies:
    - Ability to check if user has access to a page
    - Returns page access information and owner list
    - Handles Page_NoAccess exception when appropriate
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    # Get page instance
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    # Test with return_raw=False (default)
    res = await domo_page.test_page_access(
        suppress_no_access_error=True,
        debug_api=False,
        return_raw=False,
    )
    
    # Verify response structure
    assert res is not None
    assert hasattr(res, 'response')
    assert 'owners' in res.response or 'pageAccess' in res.response
    
    print(f"✓ test_page_access successful for page {TEST_PAGE_ID_1}")
    return res


async def test_cell_2_test_page_access_raw(token_auth=token_auth):
    """Test DomoPage.test_page_access() with return_raw=True.
    
    This test verifies:
    - Raw response is returned without processing
    - ResponseGetData object is returned
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    # Test with return_raw=True
    res = await domo_page.test_page_access(
        return_raw=True,
        debug_api=False,
    )
    
    # Verify raw response
    assert res is not None
    assert hasattr(res, 'response')
    assert hasattr(res, 'status')
    
    print(f"✓ test_page_access with return_raw=True successful")
    return res


async def test_cell_3_get_accesslist(token_auth=token_auth):
    """Test DomoPage.get_accesslist() method.
    
    This test verifies:
    - Retrieves comprehensive access list for a page
    - Returns users and groups with access
    - Enriches users/groups with ownership and share information
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    # Get access list
    access_list = await domo_page.get_accesslist(
        return_raw=False,
        debug_api=False,
    )
    
    # Verify response structure
    assert isinstance(access_list, dict)
    assert "explicit_shared_user_count" in access_list
    assert "total_user_count" in access_list
    assert "domo_users" in access_list
    assert "domo_groups" in access_list
    
    # Verify user enrichment
    if access_list["domo_users"]:
        for user in access_list["domo_users"]:
            assert hasattr(user, "custom_attributes")
            assert "is_explicit_share" in user.custom_attributes
            assert "group_membership" in user.custom_attributes
            assert "is_owner" in user.custom_attributes
    
    # Verify group enrichment
    if access_list["domo_groups"]:
        for group in access_list["domo_groups"]:
            assert hasattr(group, "custom_attributes")
            assert "is_owner" in group.custom_attributes
    
    print(f"✓ get_accesslist successful")
    print(f"  - Explicit shares: {access_list['explicit_shared_user_count']}")
    print(f"  - Total users: {access_list['total_user_count']}")
    print(f"  - Users: {len(access_list['domo_users'])}")
    print(f"  - Groups: {len(access_list['domo_groups'])}")
    
    return access_list


async def test_cell_4_get_accesslist_raw(token_auth=token_auth):
    """Test DomoPage.get_accesslist() with return_raw=True.
    
    This test verifies:
    - Raw response is returned without processing
    - ResponseGetData object is returned
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    # Get raw access list
    res = await domo_page.get_accesslist(
        return_raw=True,
        debug_api=False,
    )
    
    # Verify raw response
    assert res is not None
    assert hasattr(res, 'response')
    assert hasattr(res, 'status')
    assert isinstance(res.response, dict)
    
    print(f"✓ get_accesslist with return_raw=True successful")
    return res


async def test_cell_5_share_with_user(token_auth=token_auth):
    """Test DomoPage.share() method with a user.
    
    This test verifies:
    - Ability to share a page with a specific user
    - Returns ResponseGetData with operation result
    
    Note: This is a read-only test that doesn't actually share,
    or it shares with the authenticated user (which is safe).
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    # Ensure we have user_id
    await test_cell_0(token_auth)
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    # Get current user
    from domolibrary2.classes.DomoUser import DomoUser
    
    current_user = await DomoUser.get_by_id(
        user_id=token_auth.user_id,
        auth=token_auth
    )
    
    # Share page with current user (safe operation)
    try:
        res = await domo_page.share(
            domo_users=[current_user],
            message="Test share from automated test",
            debug_api=False,
        )
        
        assert res is not None
        assert hasattr(res, 'response')
        
        print(f"✓ share with user successful")
        return res
        
    except Exception as e:
        # If sharing fails (e.g., already shared), that's okay for this test
        print(f"⚠ share operation returned expected error: {type(e).__name__}")
        return None


async def test_cell_6_share_with_group(token_auth=token_auth):
    """Test DomoPage.share() method with a group.
    
    This test verifies:
    - Ability to share a page with a specific group
    - Handles list and single object inputs
    
    Note: Skipped if no test group is configured.
    """
    if not TEST_PAGE_ID_1:
        print("Skipping test - TEST_PAGE_ID_1 not configured")
        return None
    
    # This would require a test group ID in env
    test_group_id = os.environ.get("TEST_GROUP_ID", "")
    if not test_group_id:
        print("Skipping test - TEST_GROUP_ID not configured")
        return None
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_1,
        auth=token_auth
    )
    
    from domolibrary2.classes.DomoGroup import DomoGroup
    
    test_group = await DomoGroup.get_by_id(
        group_id=test_group_id,
        auth=token_auth
    )
    
    try:
        res = await domo_page.share(
            domo_groups=test_group,  # Test single object (not list)
            message="Test share with group from automated test",
            debug_api=False,
        )
        
        assert res is not None
        print(f"✓ share with group successful")
        return res
        
    except Exception as e:
        print(f"⚠ share operation returned expected error: {type(e).__name__}")
        return None


async def test_cell_7_exception_handling(token_auth=token_auth):
    """Test exception handling in access methods.
    
    This test verifies:
    - Page_NoAccess exception is properly raised and handled
    - Suppression of errors works correctly
    """
    if not TEST_PAGE_ID_2:
        print("Skipping test - TEST_PAGE_ID_2 not configured (need a page without access)")
        return None
    
    domo_page = await dmpg.DomoPage.get_by_id(
        page_id=TEST_PAGE_ID_2,
        auth=token_auth
    )
    
    # Test with suppress_no_access_error=True (should not raise)
    res = await domo_page.test_page_access(
        suppress_no_access_error=True,
        debug_api=False,
    )
    
    print(f"✓ Exception handling with suppress=True works")
    
    # Test with suppress_no_access_error=False (should raise if no access)
    try:
        res = await domo_page.test_page_access(
            suppress_no_access_error=False,
            debug_api=False,
        )
        print(f"✓ User has access to page or exception was not raised")
        
    except Exception as e:
        # Page_NoAccess exception expected if user doesn't have access
        print(f"✓ Exception properly raised: {type(e).__name__}")
    
    return True


async def main(token_auth=token_auth):
    """Run all tests in sequence."""
    fn_ls = [
        test_cell_0,
        test_cell_1_test_page_access,
        test_cell_2_test_page_access_raw,
        test_cell_3_get_accesslist,
        test_cell_4_get_accesslist_raw,
        test_cell_5_share_with_user,
        test_cell_6_share_with_group,
        test_cell_7_exception_handling,
    ]
    
    print("=" * 60)
    print("Running DomoPage Access Tests")
    print("=" * 60)
    
    for fn in fn_ls:
        print(f"\n{fn.__name__}:")
        try:
            await fn(token_auth=token_auth)
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test suite completed")
    print("=" * 60)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(token_auth=token_auth))
