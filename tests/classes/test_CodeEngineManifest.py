r"""
Test file generated from CodeEngineManifest.ipynb
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
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    PACKAGE_ID ="517ca12c-3459-4e66-b0bb-40f000720a84"
    VERSION_ID = '1.0.0'

    FUNCTION_INDEX = 3

    res = await code_engine_routes.get_codeengine_package_by_id_and_version(
        auth=token_auth,
        package_id=PACKAGE_ID,
        version = VERSION_ID,
        debug_api=False,
    )
    compare_obj = res.response['functions'][FUNCTION_INDEX]

    ast_module = dmcv.convert_python_to_ast_module(python_str=res.response['code'])

    ast_functions = dmcv.extract_ast_functions(ast_module)

    test_fn = next(fn for fn in ast_functions if fn.name == compare_obj['name'])

    assert test_fn.name == compare_obj['name']

    test_fn.__dict__


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    cem = CodeEngineManifest.from_api(obj=res.response)

    cem.download_source_code(export_folder='../../EXPORT/CodeEngineManifest/')
