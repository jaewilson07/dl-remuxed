r"""
Test file generated from CodeEngineManifest_Argument.ipynb
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
    dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    PACKAGE_ID = "517ca12c-3459-4e66-b0bb-40f000720a84"
    VERSION_ID = "1.0.0"

    FUNCTION_INDEX = 3

    res = await codeengine_routes.get_codeengine_package_by_id_and_version(
        auth=token_auth,
        package_id=PACKAGE_ID,
        version=VERSION_ID,
        debug_api=False,
    )
    compare_obj = res.response["functions"][FUNCTION_INDEX]

    ast_module = dmcv.convert_python_to_ast_module(python_str=res.response["code"])

    ast_functions = dmcv.extract_ast_functions(ast_module)

    test_fn = next(fn for fn in ast_functions if fn.name == compare_obj["name"])

    assert test_fn.name == compare_obj["name"]

    test_fn.__dict__


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    test_arg = test_fn.args.args[ARGUMENT_INDEX]

    pprint(
        {
            **test_arg.__dict__,
            "🚀 extract_ast_arg_type_annotation": extract_ast_arg_type_annotation(
                test_arg
            ),
        }
    )


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    pprint(
        {**test_arg.__dict__, "🚀 extract_ast_arg_name": extract_ast_arg_name(test_arg)}
    )


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    {
        **test_arg.__dict__,
        "🚀 extract_ast_arg_default_value": extract_ast_arg_default_value(
            test_arg, test_fn
        ),
    }


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    PythonTypeToSchemaType.get("str")


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    {
        "Optional[list[str]]": CodeEngine_Argument.init(
            "Optional[list[str]]", has_default_value=False
        ).to_dict(),
        "list[dict]": CodeEngine_Argument.init(
            "list[dict]", has_default_value=True
        ).to_dict(),
        "str": CodeEngine_Argument.init("str", has_default_value=None).to_dict(),
    }


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    CodeEngineManifest_Argument.from_ast_function_return_arg(test_fn).to_dict()


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    pd.DataFrame(
        [
            CodeEngineManifest_Argument.from_ast_arg(arg, test_fn).to_dict()
            for arg in test_fn.args.args
        ]
    )
