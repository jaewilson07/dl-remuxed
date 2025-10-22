"""
Test file generated from role.ipynb
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
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await token_auth.print_is_token()


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    role_ls = await get_roles(auth=token_auth)

    role = next(
        (role for role in role_ls.response if role.get("name") == "test_delete"), None
    )

    if not role:
        role = (
            await create_role(
                name="test_delete",
                description="test_delete",
                auth=token_auth,
                debug_api=False,
            )
        ).response

    print({"new_role": role})

    time.sleep(3)

    await delete_role(auth=token_auth, role_id=role["id"], debug_api=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await set_default_role(
        auth=token_auth,
        role_id=res.response,
        debug_api=False,
    )
