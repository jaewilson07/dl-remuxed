"""
Test file generated from enterprise_apps.ipynb
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
        domo_instance=os.environ["DOMO_DOJO_INSTANCE"],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()

    design_id_card = "8c16c8ab-c068-4110-940b-f738d7146efc"
    design_id_enterprise = "fdbcd9e6-e58e-4d59-bb47-514676d5bef7"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    try:
        all_apps = (await get_all_designs(auth=auth, debug_api = False, return_raw= True)).response

        print(all_apps)

    except dmde.RouteError as e:
        print(e)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    design_id_enterprise = next(
        (
            app["id"]
            for app in all_apps
            if app.get("referencingCards")
            and any(
                (card for card in app.get("referencingCards") if card["type"] == "domoapp")
            )
        )
    )
    design_id_enterprise


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    design = (await get_design_by_id(
        auth=auth, design_id=design_id_enterprise, debug_api=False
    )).response

    design


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    design_versions = (
        await get_design_versions(
            auth=auth,
            design_id=design["id"],
        )
    ).response

    design_versions


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    await get_design_permissions(design_id=design_id_enterprise, auth=auth)

    await auth.who_am_i()

    await add_design_admin(
        design_id=design_id_enterprise, auth=auth, user_ids=[auth.user_id], debug_api=True
    )
