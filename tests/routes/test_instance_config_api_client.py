"""
Test file generated from instance_config_api_client.ipynb
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
    import pandas as pd


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    full_auth = dmda.DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password = os.environ['DOMO_PASSWORD']
    )

    await full_auth.print_is_token()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    pd.DataFrame(
    (
    await get_api_clients(auth=auth,
                        #   return_raw = True
    )
    ).response[0:5])


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    (await get_client_by_id(auth=auth, client_id=4731, debug_api=False)).response


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    res = None
    try:
        res = await create_api_client(
            auth=full_auth,
            client_name="catty wompus5",
            # description = 'hello world',
            scope=[ApiClient_ScopeEnum.DATA, ApiClient_ScopeEnum.AUDIT],
            debug_api=False,
        )
    except ApiClient_CRUD_Error as e:
        res = e

    res


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    try:
        await revoke_api_client(auth=auth, client_id=33897)

    except ApiClient_RevokeError as e:
        print(e)
