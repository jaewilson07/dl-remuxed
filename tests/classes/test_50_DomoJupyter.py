"""
Test file generated from 50_DomoJupyter.ipynb
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

    JUPYTER_TOKEN = "OT98Xy8sePH894pA7SgUhjEcjk1kHK"
    WORKSPACE_ID = "1cfe9db4-5937-4889-beb3-a311fc42f246"  # learn_jupyter

    try:
        await jupyter_routes.start_jupyter_workspace(auth = auth, workspace_id = WORKSPACE_ID)
    except dmde.DomoError as e:
        print(e)

    workspace_params = await get_workspace_auth_token_params(
        workspace_id=WORKSPACE_ID, auth=auth
    )


    dj_auth = dmda.DomoJupyterTokenAuth.convert_auth(
        auth=auth, jupyter_token=JUPYTER_TOKEN, **workspace_params
    )

    dj_auth


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    djw = await DomoJupyterWorkspace.get_by_id(
        workspace_id=WORKSPACE_ID, auth=auth, jupyter_token=JUPYTER_TOKEN
    )

    djw


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await djw.get_account_configuration()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    djw = await DomoJupyterWorkspace.get_by_id(
        workspace_id=WORKSPACE_ID, auth=auth, jupyter_token=JUPYTER_TOKEN
    )

    djw


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await djw.get_account_configuration()


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    dj_workspaces = DomoJupyterWorkspaces(auth = dj_auth)
    dj_workspace = None

    try:
        dj_workspace = await dj_workspaces.search_workspace_by_name(
            workspace_name="learn_jupyter", debug_api=False, return_raw=False
        )
        print(dj_workspace)
    except dmde.DomoError as e:
        print(e)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    if dj_workspace:
        [print(ac) for ac in dj_workspace.account_configuration]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    try:
        await djw.get_content()

    except (JupyterAPI_Error, dmda.InvalidAuthTypeError,TypeError  ) as e:
        print(e)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    test_content = None
    try:
        djw_content = await djw.get_content()

        test_content = next(
            (
                content
                for content in djw_content
                if content.name.startswith("updated_") and content.folder == "new_folder/"
            )
        )
        test_content.content = (
            f"jae rocks at debugging.  he's superfly -- updated {dt.date.today()}"
        )

        print((await test_content.update(debug_api=False)).response)

    except (JupyterAPI_Error, dmda.InvalidAuthTypeError) as e:
        print(e)


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    try:
        if test_content:
            test_content.export(output_folder="../test/")

    except Exception as e:
        print(e)


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    await dj_workspace.get_account_configuration()
