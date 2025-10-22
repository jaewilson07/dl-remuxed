"""
Test file generated from dataflow.ipynb
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
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    dataflows = (await get_dataflows( auth=token_auth)).response

    dataflows[0]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    dataflow_id = dataflows[0]['id']

    res = await get_dataflow_by_id(dataflow_id=dataflow_id, auth=token_auth)

    res.response.keys()

    all_keys = []
    for action in res.response.get("actions"):
        pprint(action)

    list(set(all_keys))


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    res = await get_dataflow_tags_by_id(dataflow_id=dataflow_id, auth=token_auth)

    df_tags = res.response['tags']
    res.response


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    dl_tag = next((tag for tag in df_tags if tag.startswith('dl_')), None)

    if dl_tag in df_tags:
        df_tags.remove(dl_tag)

    dl_tag = f"dl_updated - {dt.date.today()}"
    df_tags += [dl_tag]

    (await put_dataflow_tags_by_id(
        auth = token_auth,
        dataflow_id = dataflow_id,
        tag_ls = df_tags
    )).response


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    versions = (
        await get_dataflow_versions(dataflow_id=dataflow_id, auth=token_auth)
    ).response

    (await get_dataflow_by_id_and_version(
        dataflow_id=dataflow_id,
        version_id=versions[0]["id"],
        auth=token_auth,
        debug_api=False,
    )).response


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    (await get_dataflow_execution_history(dataflow_id=dataflow_id, maximum=2, auth=token_auth)).response[0]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    executions = (await get_dataflow_execution_history(dataflow_id=dataflow_id, maximum=2, auth=token_auth)).response


    res = await get_dataflow_execution_by_id(
        dataflow_id=dataflow_id, execution_id=executions[0]['id'], auth=token_auth
    )

    res.response


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    try:
        print(await execute_dataflow(dataflow_id=dataflow_id, auth=token_auth))

    except dmde.DomoError as e:
        print(e)


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    pd.DataFrame((await search_dataflows_to_jupyter_workspaces(auth = token_auth, debug_api = False)).response)[0:5]


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    try:
        await search_dataflows_to_jupyter_workspaces(auth = token_auth, 
                                                    dataflow_id = 86,
                                                    debug_api = False,
        )
    except dmde.DomoError as e:
        print(e)
