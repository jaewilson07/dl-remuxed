"""
Test file generated from 50_DomoDatacenter.ipynb
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
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    additional_filters_ls = [
        datacenter_routes.generate_search_datacenter_filter(
            "dataprovidername_facet", "Jupyter Data"
        )
    ]

    res = await DomoDatacenter(auth = auth).search_datacenter(
        # additional_filters_ls=additional_filters_ls,
        # search_text="*kb*",
        entity_type=datacenter_routes.Datacenter_Enum.DATASET.value,
    )

    dataset_id = res[0]['databaseId']
    pd.DataFrame(res[0:5])


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await DomoDatacenter(auth = auth).get_cards_admin_summary(
        # return_raw = True,
        maximum=5,
        # debug_api = True
    )
