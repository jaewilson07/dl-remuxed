r"""
Test file generated from _50_DomoEnterpriseApps.ipynb
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
        domo_instance=os.environ['DOMO_DOJO_INSTANCE'],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()



async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_app = await DomoEnterpriseApp.get_by_id(
        # design_id=design_id_enterprise,
        design_id=design_id_ddx,
        auth=auth,
        return_raw=False,
    )

    # domo_app

    await domo_app.get_versions()
    domo_app.current_version = domo_app.versions[-1]
    # pprint(domo_app)

    await domo_app.share(debug_api=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    design_id_ddx = '5e9cf62a-fb00-4686-a1ae-c84ea5f58db1'

    domo_app = await DomoEnterpriseApp.get_by_id(
        # design_id=design_id_enterprise,
        design_id = design_id_ddx,
        auth=auth,
        return_raw= False
        )

    # domo_app

    await domo_app.get_versions()
    # domo_app.current_version = domo_app.versions[-1]
    # pprint(domo_app)
    await domo_app.share(debug_api = False)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_apps = DomoEnterpriseApps(auth=auth)
    # (await domo_apps.get_apps(debug_api=False, return_raw=False))[0:5]

    await domo_apps.get_all_app_source_code( download_folder = '../../test/', try_auto_share = True)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_apps.get_all_app_source_code( download_folder = '../../test/', try_auto_share = True)
