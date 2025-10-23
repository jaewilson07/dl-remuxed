"""
Test file generated from CodeEngineManifest_Function.ipynb
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
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    PACKAGE_ID = "517ca12c-3459-4e66-b0bb-40f000720a84"
    VERSION_ID = "1.0.0"

    FUNCTION_INDEX = 3
    ARGUMENT_INDEX = 1

    res = await code_engine_routes.get_codeengine_package_by_id_and_version(
        auth=token_auth,
        package_id=PACKAGE_ID,
        version=VERSION_ID,
        debug_api=False,
    )
    compare_obj = res.response["functions"][FUNCTION_INDEX]

    ast_module = dmcv.convert_python_to_ast_module(python_str=res.response["code"])

    ast_functions = dmcv.extract_ast_functions(ast_module)

    test_fn = next((fn for fn in ast_functions if fn.name == compare_obj["name"]))

    assert test_fn.name == compare_obj["name"]

    test_fn.__dict__


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    res.response["code"]

    start_char_index = calculate_character_index_of_line_number(
        test_fn.lineno - 1, full_text=res.response["code"]
    )
    end_char_index = calculate_character_index_of_line_number(
        test_fn.end_lineno - 1, full_text=res.response["code"]
    )

    print(test_fn.lineno, test_fn.end_lineno)
    res.response["code"][start_char_index:end_char_index]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    res.response["code"].split("\n")[101]


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    extract_function_docstring(test_fn)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    ce_fn = CodeEngineManifest_Function.from_ast_function_def(
        test_fn, original_module_string=res.response["code"]
    )
    ce_fn.download_source_code(export_folder="../../EXPORT/CodeEngineFunctions/")
    # ce_fn.to_json()


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    ce_fn.validate_json_to_manifest(test_obj=compare_obj, debug_prn=True)
