"""
Test file generated from dataset.ipynb
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

    dataset_id = '04c1574e-c8be-4721-9846-c6ffa491144b'


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    sql = f"SELECT * FROM TABLE"

    pd.DataFrame(
        (
            await query_dataset_private(
                dataset_id=dataset_id,
                auth=token_auth,
                sql=sql,
                skip=0,
                maximum=10,
                # filter_pdp_policy_id_ls=[1225, 1226],  # to apply pdp filter context
                loop_until_end=False,
                debug_api=True,
                timeout=30,
            )
        ).response
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    schema_res = await get_schema(dataset_id=dataset_id, auth=token_auth)

    schema_obj = schema_res.response["tables"][0]

    await alter_schema(dataset_id=dataset_id, auth=token_auth, schema_obj=schema_obj)

    ## must index dataset after alter schema
    # await index_dataset(dataset_id=os.environ["DOJO_DATASET_ID"], auth=token_auth )
