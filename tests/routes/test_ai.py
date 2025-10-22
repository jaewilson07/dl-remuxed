"""
Test file generated from ai.ipynb
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
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
        domo_instance=os.environ["DOMO_INSTANCE"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    (await llm_generate_text(text_input="why is the sky blue", auth=auth)).response['output']


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    (await llm_summarize_text(
        "it is 50 degrees in seoul.  we decided to run for the hills.  curiously the windchill is relatively low",
        auth = auth
    )).response['output']


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    dataset_id = 'e1b88aab-42b5-4733-9817-cae8937ecb08'

    res = await get_dataset_ai_readiness(
        auth = auth,
        dataset_id = dataset_id,
        # debug_api = True,
    )

    res


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    data_dictionary = res.response[0]["dataDictionary"]
    data_dictionary

    await update_dataset_ai_readiness(
        auth = auth,
        dataset_id = dataset_id,
        body = data_dictionary,
        debug_api = False,
    )
