"""
Test file generated from codeengine_GET.ipynb
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
    auth

    PACKAGE_ID = "517ca12c-3459-4e66-b0bb-40f000720a84"
    VERSION_ID = "1.0.0"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    packages = (await get_packages(auth=auth, debug_api=False)).response

    packages[0:1]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    package = (
        await get_codeengine_package_by_id(
            auth=auth, package_id=PACKAGE_ID, debug_api=False
        )
    ).response

    package


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    res = (await get_package_versions(auth=auth, package_id=PACKAGE_ID)).response
    res


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    res = await get_codeengine_package_by_id_and_version(
        auth=token_auth,
        package_id=PACKAGE_ID,
        version=VERSION_ID,
        debug_api=False,
    )

    res.response


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    res = await get_codeengine_package_by_id_and_version(
        auth=auth, package_id=PACKAGE_ID, version=VERSION_ID, debug_api=False
    )

    res.response
