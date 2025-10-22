"""
Test file generated from RoleHierarchy.ipynb
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
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


    domo_roles = await get_roles_w_hierarchy(auth=token_auth)


    pd.DataFrame(
        [
            {
                "role_name": role.name,
                "role_id": role.id,
                "description": role.description,
                "hierarchy": role.hierarchy,
            }
            for role in sorted(domo_roles, key=lambda x: x.hierarchy, reverse=True)
        ]
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    print(await calc_role(3, "manual_super_admin", auth=token_auth, debug_prn=True))
    print("\n")
    print(
        await calc_role(
            3,
            "manual_super_admin",
            is_alter_system_roles=True,
            auth=token_auth,
            debug_prn=True,
        )
    )
    print("\n")
    try:
        print(
            await calc_role(
                3, "social", is_alter_system_roles=True, auth=token_auth, debug_prn=True
            )
        )
    except Exception as e:
        print(e)
    print("\n")
    print(
        await calc_role(
            3, "Social", is_alter_system_roles=True, auth=token_auth, debug_prn=True
        )
    )
