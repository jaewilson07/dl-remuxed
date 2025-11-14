r"""
Test file generated from 50_DomoDataflow.ipynb
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
        domo_instance=os.environ['DOMO_DOJO_INSTANCE'],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    dataflows = (await dataflow_routes.get_dataflows(auth = auth)).response
    dataflow_id = dataflows[0]['id']

    versions = (await dataflow_routes.get_dataflow_versions(auth =auth, dataflow_id = dataflow_id)).response
    versions[0]['id']


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_dataflow = await DomoDataflow.get_by_id(dataflow_id=dataflow_id, auth=auth, return_raw = False)
    domo_dataflow


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    dataflow_definition = (await domo_dataflow.get_definition(return_raw = True)).response
    dataflow_definition

    await domo_dataflow.update_dataflow_definition(
        new_dataflow_definition = dataflow_definition
    )


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    lineage = await domo_dataflow.Lineage.get(
        return_raw=True,
        debug_api = False)

    lineage


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    try:
        domo_dataflow = await DomoDataflow.get_by_id(dataflow_id=86, auth=auth, return_raw = False)


        print(await domo_dataflow.get_jupyter_config())

    except dmde.DomoError as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    try:
        domo_dataflow = await DomoDataflow.get_by_id(dataflow_id=dataflow_id, auth=auth)

        print(await domo_dataflow.execute())

    except dmde.DomoError as e:
        print(e)


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    (await domo_dataflow.get_versions(return_raw=False))[0:5]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    (await DomoDataflows(auth = auth).get(return_raw = False))[0:5]
