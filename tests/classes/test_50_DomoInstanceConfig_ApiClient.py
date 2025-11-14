r"""
Test file generated from 50_DomoInstanceConfig_ApiClient.ipynb
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
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    dmda.DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_clients = ApiClients(auth=full_auth)

    (await domo_clients.get(return_raw = True)).response

    # await domo_clients.get_by_name(client_name="AWS Export")


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_clients = ApiClients(auth=full_auth)
    (await domo_clients.get(return_raw=False))[0:5]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    pprint(

            await ApiClient.get_by_id(
                auth=token_auth, client_id=domo_clients.domo_clients[0].id, return_raw=False
            )

    )


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_clients = ApiClients(auth=full_auth)

    domo_client = None

    try:
        domo_client = await domo_clients.create_for_authorized_user(
            client_name="catty rats2",
            scope=[ApiClient_ScopeEnum.DATA, ApiClient_ScopeEnum.AUDIT],
            debug_api=False,
        )

    except ApiClient_CRUD_Error as e:
        print(e)

    domo_client


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    if domo_client:
        print(await domo_client.revoke())


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await domo_clients.upsert_client(
        client_name="catty rats2",
        scope=[ApiClient_ScopeEnum.DATA, ApiClient_ScopeEnum.AUDIT],
        debug_api=False,
        is_regenerate = False
    )
