r"""
Test file generated from 50_DomoTag.ipynb
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

    datasets = (
        await datacenter_routes.search_datacenter(
            auth=token_auth,
            entity_type="DATASET",
            # maximum = 25
        )
    ).response

    dataset = next(

            dataset
            for dataset in datasets
            if dataset["rowCount"] != 0
            # and dataset["ownedById"] == token_auth.user_id

    )
    dataset
    dataset_id = dataset["databaseId"]
    dataset_id


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    today_year = dt.datetime.today().strftime("%Y")

    await ds_tags.add(add_tag_ls=[today_year])
