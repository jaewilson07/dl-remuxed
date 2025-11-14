r"""
Test file generated from _codeengine_package_analyzer.ipynb
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
    ca = CodeEngineScriptAnalyzer()
    with open('../test/int_package.py') as f:
        code_content = f.read()

    ca = CodeEngineScriptAnalyzer()
    manifest = ca.generate_manifest_from_string(code_content)
    int_package_builder = CodeEnginePackageBuilder().set_code(code_content).set_environment("LAMBDA").set_language("PYTHON").set_name("GM Int Package").set_version("1.0.0").set_manifest(manifest)
    await create_package(int_package_builder, auth=auth, debug_api=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    res.response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    package_id = "0b628c44-0a1a-4e76-83ae-681cde27b129"
    version = "2.0.5"

    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    res = await get_codeengine_package_by_id_and_version(
        auth=token_auth, package_id=package_id, version=version, debug_api=False
    )

    package = res.response

    extract_functions(
        function_ls=package["functions"], code=package["code"], language="JAVASCRIPT"
    )


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    package_id = "37e449bf-52da-43ab-872e-361a643e13b6"
    version = "1.0.0"

    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    res = await get_codeengine_package_by_id_and_version(
        auth=token_auth, package_id=package_id, version=version, debug_api=False
    )

    package = res.response

    extract_functions(
        function_ls=package["functions"], code=package["code"], language="PYTHON"
    )
