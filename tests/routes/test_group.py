"""
Test file generated from group.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
import domolibrary.client.DomoAuth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    search_name = "Test Groupie"
    try:
        res = await search_groups_by_name(
            auth=auth, search_name=search_name, debug_api=False
        )
        print(res)
    except (Group_GET_Error, SearchGroups_Error) as e:
        print(e)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    res = await get_all_groups(auth=auth, maximum=5)

    print(f"{len(res.response)} groups retrieved")

    pd.DataFrame(res.response)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await is_system_groups_visible(auth=auth)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    res = await toggle_system_group_visibility(auth=auth, is_hide_system_groups=True)

    res = await get_all_groups(auth=auth)
    all_groups = res.response

    (
        await toggle_system_group_visibility(auth=auth, is_hide_system_groups=False)
    ).response

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


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    generate_body_create_group(
        group_name="test_group_name",
        group_type=GroupType_Enum.ADHOC.value,
        description="from jupyter",
    )


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    try:
        res = await create_group(
            auth=auth,
            group_name="hello world",
            description=f"updated via API on {dt.date.today()}",
            debug_api=False,
        )

        group_id = res.response.get("id")

        await delete_groups(auth=auth, group_ids=group_id, debug_api=False)
    except Exception as e:
        print(e)


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    group_id = 1781661643

    res = await get_group_owners(
        auth=auth,
        group_id=group_id,
        debug_api=False,
        # debug_loop = True,
        return_raw=False,
    )

    pd.DataFrame(res.response)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    generate_body_update_group_membership(group_id=123)


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    group_id = 1513712315

    add_obj = {"id": auth.user_id, "type": "USER"}

    try:
        print(
            await update_group_membership(
                auth=auth,
                group_id=group_id,
                add_member_arr=[add_obj],
                add_owner_arr=[add_obj],
                debug_api=False,
            )
        )

    except dmde.RouteError as e:
        print(e)
