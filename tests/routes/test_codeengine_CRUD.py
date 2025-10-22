"""
Test file generated from codeengine_CRUD.ipynb
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
    auth


    PACKAGE_ID = "517ca12c-3459-4e66-b0bb-40f000720a84"
    VERSION_ID = "1.0.0"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    try:
        res = await deploy_code_engine_package(
            package_id=PACKAGE_ID, version=VERSION_ID, auth=auth, debug_api=False
        )
        print(res.response)

    except CodeEngine_API_Error as e:
        print(e)
