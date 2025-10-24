"""
Test file generated from 50_DomoRole.ipynb
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

    roles = (await role_routes.get_roles(auth=auth)).response
    role = next((role for role in roles if 'test' in role['name'].lower()))
    role_id = role["id"]

    users = (await user_routes.get_all_users(auth=auth)).response
    user = next((user for user in users if 'test' in user["emailAddress"].lower()))


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_role = await DomoRole.get_by_id(auth=auth, role_id=role_id)

    (await domo_role.get_grants(return_raw=False))[0:5]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_role = await DomoRole.get_by_id(role_id = role_id, auth = auth)

    role_grants = [
        "user.edit",
        "user.invite",
        # "user.session.edit",
        # "versions.repository.admin",
    ]

    await domo_role.set_grants(grants=role_grants, debug_api=False)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    (await domo_role.get_membership(return_raw=False))[0:5]


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_user = await dmdu.DomoUser.get_by_id(user_id=user["id"], auth=auth)
    domo_role = await DomoRole.get_by_id(auth=auth, role_id=role_id)

    (await domo_role.add_user(user=domo_user))[0:5]


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    try:
        await DomoRole.delete_role(role_id=role_id, auth=auth, debug_api=False)
    except dmde.DomoError as e:
        print(e)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_roles = DomoRoles(auth=auth)

    await domo_roles.get_default_role()

    domo_roles


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    (await domo_roles.get())[0:5]


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    await domo_roles.search_by_name(role_name="Admin")


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    domo_role = DomoRoles(auth =auth)

    try:
        await domo_role.create(
            name="super_admin_v3",
            description="created via DomoLibrary",
        )
    except dmde.DomoError as e:
        print(e)


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    grant_ls = [
        "cloud.admin",
        "versions.repository.admin",
        "codeengine.package.manage",
        "appstore.admin",
        "datastore.admin",
        "certifiedcontent.admin",
    ]


    await domo_roles.upsert(
        name="super_admin_v3",
        description="upsert via DomoLibrary",
        grants=grant_ls,
    )
