r"""
Test file generated from 50_DomoDataflow_History.ipynb
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

    history = (await dataflow_routes.get_dataflow_execution_history(auth = auth, dataflow_id = dataflow_id)).response
    history[0]['id']


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(DomoDataflow_History_Execution.get_by_id)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await DomoDataflow_History_Execution.get_by_id(
        dataflow_id=dataflow_id, execution_id=execution_id, auth=auth, return_raw=False
    )


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_dataflow_execution = await DomoDataflow_History_Execution.get_by_id(
        dataflow_id=dataflow_id, execution_id=execution_id, auth=auth, return_raw=False
    )
    await domo_dataflow_execution.get_actions()


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    show_doc(DomoDataflow_History.get_execution_history)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_dataflow_history = DomoDataflow_History(dataflow_id=dataflow_id, auth=auth)

    (await domo_dataflow_history.get_execution_history(debug_api=False, return_raw=False))[
        0:5
    ]
