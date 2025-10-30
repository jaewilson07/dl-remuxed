r"""
Test file generated from CodeEngine.ipynb
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


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    package = await DomoCodeEngine_PackageVersion.get_by_id_and_version(
        package_id="0b628c44-0a1a-4e76-83ae-681cde27b129",
        version="2.0.5",
        auth=auth,
        debug_api=False,
        language="JAVASCRIPT",
        # return_raw=True
    )
    # pprint(package)


    # package.Manifest
    await package.download_source_code(
        download_folder="../../test/CodeEnginePackage_JS/",
        debug_api=True
    )

    # package.functions


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    package_id = "37e449bf-52da-43ab-872e-361a643e13b6"
    version = "1.0.0"

    dcep = await DomoCodeEngine_PackageVersion.get_by_id_and_version(
        package_id=package_id,
        version=version,
        auth=auth,
        debug_api=False,
        language="PYTHON",
        # return_raw=True
    )

    dcep.Manifest.functions


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    package_id = "37e449bf-52da-43ab-872e-361a643e13b6"
    version = "1.0.0"

    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    domo_version = await DomoCodeEngine_PackageVersion.get_by_id_and_version(
        package_id=package_id,
        version=version,
        auth=token_auth,
        debug_api=False,
        language="PYTHON",
        # return_raw=True
    )

    domo_version.export(output_folder="../test/code_engine")


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    res = await DomoCodeEngine_Package.get_by_id(
        package_id="517ca12c-3459-4e66-b0bb-40f000720a84",
        auth=token_auth,
        debug_api=False,
        # return_raw=True
    )

    pprint(res)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    package_id = "0b628c44-0a1a-4e76-83ae-681cde27b129"

    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


    domo_codeengine_version = await DomoCodeEngine_Package.get_current_version_by_id(
        package_id=package_id,
        auth=token_auth,
        debug_api=False,
        # return_raw=True
    )
    domo_codeengine_version


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_codeengine_version
