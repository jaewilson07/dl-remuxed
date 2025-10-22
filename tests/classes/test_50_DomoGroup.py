"""
Test file generated from 50_DomoGroup.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
import domolibrary.client.DomoAuth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ['DOMO_INSTANCE'],
    domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    groups = (await group_routes.get_all_groups(auth=auth)).response
    group = next((group for group in groups if "test" in group["name"].lower()))

    group_id = group["groupId"]


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id, return_raw=False)
    domo_group


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    (await domo_group.Membership.get_members())[0:5]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    group_name = "Test Group ac"
    domo_group = None
    try:
        domo_group = await DomoGroup.create_from_name(group_name=group_name, auth=auth)
        print(domo_group)
    except Group_CRUD_Error as e:
        print(e)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_group = await DomoGroup.get_by_id(group_id=group_id, auth=auth)

    try:
        await domo_group.update_metadata(
            auth=auth,
            # group_name="Test Group ABCs",
            group_type="open",
            description=f"updated via API on {dt.date.today()}",
            debug_api=False,
        )

    except (Group_CRUD_Error, Group_Class_Error) as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_users = await dmu.DomoUsers.all_users(auth=auth)
    domo_users[0:5]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    print(
        f"validate old membership {', '.join([str(id) for id in domo_group.members_id_ls])}"
    )

    new_membership = await dmu.DomoUsers.by_id(
        user_ids=[domo_user.id for domo_user in domo_users], auth=auth, only_allow_one=False
    )

    (await domo_group.Membership.add_members(add_user_ls=new_membership, debug_api=False))[
        0:5
    ]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    print(
        f"validate old membership {', '.join([str(id) for id in domo_group.members_id_ls])}"
    )


    remove_membership = await dmu.DomoUsers.by_id(
        user_ids=[domo_user.id for domo_user in domo_users], auth=auth, only_allow_one=False
    )

    try:
        print(
            (await domo_group.Membership.remove_members(remove_user_ls=remove_membership))[
                0:5
            ]
        )

    except dmde.DomoError as e:
        print(e)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    print(
        f"validate old membership {', '.join([str(id) for id in domo_group.members_id_ls])}"
    )

    set_membership = await dmu.DomoUsers.by_id(
        user_ids=[domo_user.id for domo_user in domo_users],
        auth=auth,
        only_allow_one=False,
    )

    (await domo_group.Membership.add_members(add_user_ls=set_membership))[0:5]


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    await domo_group.Membership.get_owners()

    print(f"validate old ownership {', '.join([str(id) for id in domo_group.owner_id_ls])}")

    new_ownership_user = await dmu.DomoUsers.by_id(
        user_ids=[auth.user_id], auth=auth, only_allow_one=False
    )

    (await domo_group.Membership.add_owners(add_owner_ls=new_ownership_user))[0:5]


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    try:

        print(
            f"validate old ownership {', '.join([str(id) for id in domo_group.owner_id_ls])}"
        )

        remove_owner = await dmu.DomoUsers.by_id(
            user_ids=[auth.user_id], auth=auth, only_allow_one=False
        )

        print(await domo_group.Membership.remove_owners(remove_owner_ls=remove_owner))

    except SearchUser_NoResults as e:
        print(e)


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    await domo_group.Membership.add_owner_manage_all_groups_role()


async def test_cell_13(token_auth=token_auth):
    """Test case from cell 13"""
    domo_group = await DomoGroup.get_by_id(auth=auth, group_id=group_id)

    print(
        f"validate old ownership {', '.join([str(id) for id in domo_group.members_id_ls])}"
    )

    set_ownership = await dmce.gather_with_concurrency(
        n=60,
        *[DomoGroup.get_by_id(group_id=group_id, auth=auth) for group_id in [group_id]],
    )

    try:
        print(await domo_group.Membership.add_owners(add_owner_ls=set_ownership))


    except Exception as e:
        print(e)


async def test_cell_14(token_auth=token_auth):
    """Test case from cell 14"""
    domo_groups = DomoGroups(auth=auth)
    (await domo_groups.get())[0:5]


async def test_cell_15(token_auth=token_auth):
    """Test case from cell 15"""
    domo_groups = DomoGroups(auth=auth)

    await domo_groups.search_by_name(group_name="April 2023 Cohort")


async def test_cell_16(token_auth=token_auth):
    """Test case from cell 16"""
    domo_group = DomoGroups(auth=auth)

    all_groups_with_hidden = await domo_group.get(is_hide_system_groups=True)

    all_groups = await domo_group.get(is_hide_system_groups=False)


    print(
        f"there are {len(all_groups)} standard groups, and {len(all_groups_with_hidden)} groups including system groups"
    )


async def test_cell_17(token_auth=token_auth):
    """Test case from cell 17"""
    domo_groups = DomoGroups(auth=auth)

    try:
        await domo_groups.upsert(
            group_name="test_DO_NOT_DELETE",
            description=f"updated via upsert_group on {dt.date.today()}",
            debug_api=False,
        )

    except dmde.DomoError as e:
        print(e)


async def test_cell_18(token_auth=token_auth):
    """Test case from cell 18"""
    domo_groups = DomoGroups(auth=auth)
    try:
        domo_group = await domo_groups.upsert(
            group_name="hello world",
            description=f"updated via API on {dt.date.today()}",
            debug_api=False,
        )

        await domo_group.delete(debug_api=False)

    except dmde.DomoError as e:
        print(e)
