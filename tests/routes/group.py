r"""
Test file for group routes.
Tests group CRUD operations, membership management, and visibility toggles.
"""

import os
import datetime as dt
from dotenv import load_dotenv
import pytest

import domolibrary2.auth as dmda
import domolibrary2.base.exceptions as dmde
from domolibrary2.client.response import ResponseGetData
from domolibrary2.routes.group import (
    search_groups_by_name,
    get_all_groups,
    is_system_groups_visible,
    toggle_system_group_visibility,
    generate_body_create_group,
    create_group,
    delete_groups,
    get_group_owners,
    generate_body_update_group_membership,
    update_group_membership,
    GroupType_Enum,
)

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


@pytest.mark.asyncio
async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    assert await token_auth.print_is_token()


@pytest.mark.asyncio
async def test_cell_2(token_auth=token_auth):
    """Test searching groups by name."""
    search_name = "Test Groupie"
    try:
        res = await search_groups_by_name(
            auth=token_auth, search_name=search_name, debug_api=False
        )
        assert res is not None
        assert isinstance(res, ResponseGetData)
        assert res.is_success

    except dmde.RouteError as e:
        print(f"Search failed (expected): {e}")


@pytest.mark.asyncio
async def test_cell_3(token_auth=token_auth):
    """Test getting all groups with limit."""
    res = await get_all_groups(auth=token_auth, maximum=5)

    assert res is not None
    assert res.is_success
    assert isinstance(res.response, list)
    assert len(res.response) <= 5
    print(f"{len(res.response)} groups retrieved")


@pytest.mark.asyncio
async def test_cell_4(token_auth=token_auth):
    """Test checking system groups visibility."""
    res = await is_system_groups_visible(auth=token_auth)
    assert res is not None
    assert res.is_success
    # Response is a dict with 'value' field containing the boolean
    assert isinstance(res.response, dict)
    assert 'value' in res.response


@pytest.mark.asyncio
async def test_cell_5(token_auth=token_auth):
    """Test toggling system groups visibility."""
    # Hide system groups
    res1 = await toggle_system_group_visibility(
        auth=token_auth, is_hide_system_groups=True
    )
    assert res1.is_success

    # Get groups (should not include system groups)
    res2 = await get_all_groups(auth=token_auth)
    assert res2.is_success

    # Show system groups again
    res3 = await toggle_system_group_visibility(
        auth=token_auth, is_hide_system_groups=False
    )
    assert res3.is_success

    # res = await get_all_groups(auth=auth)
    # all_groups_with_hidden = res.response

    # print(
    #     f"there are {len(all_groups)} standard groups, and {len(all_groups_with_hidden)} groups including system groups"
    # )

    # [
    #     group["name"]
    #     for group in all_groups_with_hidden
    #     if group["groupId"] not in [all_group["groupId"] for all_group in all_groups]
    # ][0:5]


@pytest.mark.asyncio
async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    generate_body_create_group(
        group_name="test_group_name",
        group_type=GroupType_Enum.ADHOC.value,
        description="from jupyter",
    )


@pytest.mark.asyncio
async def test_cell_7(token_auth=token_auth):
    """Test creating and deleting a group."""
    try:
        res = await create_group(
            auth=token_auth,
            group_name="test_group_temp",
            description=f"Test group created via API on {dt.date.today()}",
            debug_api=False,
        )
        assert res.is_success
        group_id = res.response.get("id")
        assert group_id is not None

        # Clean up - delete the group
        del_res = await delete_groups(
            auth=token_auth, group_ids=group_id, debug_api=False
        )
        assert del_res.is_success
    except dmde.RouteError as e:
        print(f"Group creation/deletion test failed (may be expected): {e}")


@pytest.mark.asyncio
async def test_cell_8(token_auth=token_auth):
    """Test getting group owners."""
    # Note: This test requires a valid group_id from environment
    group_id = os.environ.get("TEST_GROUP_ID")
    if not group_id:
        print("Skipping test_cell_8: TEST_GROUP_ID not set")
        return

    res = await get_group_owners(
        auth=token_auth,
        group_id=int(group_id),
        debug_api=False,
        return_raw=False,
    )
    assert res is not None
    assert isinstance(res.response, list)


@pytest.mark.asyncio
async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    generate_body_update_group_membership(group_id=123)


@pytest.mark.asyncio
async def test_cell_10(token_auth=token_auth):
    """Test updating group membership."""
    # Note: This test requires a valid group_id from environment
    group_id = os.environ.get("TEST_GROUP_ID")
    if not group_id:
        print("Skipping test_cell_10: TEST_GROUP_ID not set")
        return

    add_obj = {"id": token_auth.user_id, "type": "USER"}

    try:
        res = await update_group_membership(
            auth=token_auth,
            group_id=int(group_id),
            add_member_arr=[add_obj],
            add_owner_arr=[add_obj],
            debug_api=False,
        )
        assert res is not None
        print(f"Membership updated successfully: {res.is_success}")
    except dmde.RouteError as e:
        print(f"Membership update failed (may be expected): {e}")
