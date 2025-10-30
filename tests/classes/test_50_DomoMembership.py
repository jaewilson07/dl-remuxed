r"""
Test file generated from 50_DomoMembership.ipynb
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
    dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )



async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    group_membership = GroupMembership(auth=auth, parent_id=group_id, parent = None, )

    await group_membership.get_owners(return_raw=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    group_membership = GroupMembership(auth=auth, parent_id=group_id, parent = None)

    await group_membership.get_members(return_raw=False)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    group_membership._list_to_dict(group_membership.members)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await group_membership.get_owners(debug_api = False, return_raw = False)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    group_membership._list_to_dict(group_membership.owners)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await auth.who_am_i()

    oe = await dmdu.DomoUser.get_by_id(auth=auth, user_id = auth.user_id)

    group_membership = GroupMembership(auth =auth, parent_id = 1513712315, parent = None)


    await group_membership.remove_members(
        remove_user_ls=[Membership_Entity(entity = oe, relation_type = 'MEMBER', auth = auth)],
    )


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    oe = await dmdu.DomoUser.get_by_id(auth=auth, user_id = auth.user_id)

    group_membership = GroupMembership(auth =auth, parent_id = 1513712315, parent = None)


    await group_membership.add_owners(
        add_owner_ls =[Membership_Entity(entity = oe, relation_type = 'OWNER', auth = auth)],
    )
