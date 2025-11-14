r"""
Test file generated from 50_DomoJupyter_Account.ipynb
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

    JUPYTER_TOKEN = " OT98Xy8sePH894pA7SgUhjEcjk1kHK"
    WORKSPACE_ID = '1cfe9db4-5937-4889-beb3-a311fc42f246' #learn_jupyter

    workspace_params = await get_workspace_auth_token_params(
        workspace_id=WORKSPACE_ID, auth=auth
    )

    dmda.DomoJupyterTokenAuth.convert_auth(
        auth=auth, jupyter_token=JUPYTER_TOKEN, **workspace_params
    )
