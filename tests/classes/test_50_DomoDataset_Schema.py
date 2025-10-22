"""
Test file generated from 50_DomoDataset_Schema.ipynb
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
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await token_auth.who_am_i()

    DATASET_ID = 'e1b88aab-42b5-4733-9817-cae8937ecb08'


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    schema = DomoDataset_Schema(parent_id=DATASET_ID, auth=token_auth, parent = None, raw = None)

    (await schema.get(return_raw = False))
    # [0:5]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    pd.DataFrame(schema.to_dict()["columns"])


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    pd.DataFrame(schema.to_dict()["columns"])[0:5]


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    schema.columns[0].replace_tag("dl_update", f"dl_update {dt.datetime.now()}")
    schema.columns[0]

    print(await schema.alter_schema(
        auth=token_auth, dataset_id=DATASET_ID, return_raw=False,
        debug_api = False
    ))


    await schema.alter_schema_descriptions(
        auth=token_auth, dataset_id=DATASET_ID, return_raw=False,
        debug_api = False
    )
