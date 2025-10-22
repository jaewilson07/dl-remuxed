"""
Test file generated from 50_DomoDataset.ipynb
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
        domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN"),
    )

    await token_auth.who_am_i()

    dataset_id = "905fa986-fb88-412c-8a27-bc37b4c06617"

    print(dmdl.DomoLineage_ParentTypeEnum.__members__)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_dataset = await DomoDataset_Default.get_by_id(
        auth=token_auth, dataset_id=dataset_id, return_raw=False
    )


    from pprint import pprint

    pprint(domo_dataset)
    (await domo_dataset.Schema.get())[0:5]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    """try:

        dataset = await DomoDataset.get_by_id(auth=token_auth, dataset_id=dataset_id)

        ds_partition_ls = await dataset.list_partitions()
        print(ds_partition_ls)

        ds = await dataset.delete_partition(
            dataset_partition_id="2023-04-27",
            auth=token_auth,
            dataset_id=dataset_id,
            debug_api=False,
            debug_prn=True,
        )

        print(await dataset.list_partitions())

    except dmde.DomoError as e:
        print(e)"""


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    FEDERATED_DS_ID = '58a75bc7-e626-4ea1-a3d9-b1ae96188b5c'
    dataset_id = FEDERATED_DS_ID

    ds = await DomoDataset.get_by_id(dataset_id = dataset_id,
                                auth= token_auth,
                                is_use_default_dataset_class=False
                                )

    ds


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    parent_auth = dmda.DomoTokenAuth(
            domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
            domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN")
        )

    # await ds.Lineage.get(parent_auth_retreival_fn=retreive_parent_auth_fn)
    try:
        await ds.Lineage.get(parent_auth = parent_auth)

    except Exception as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    from typing import Union
    import domolibrary.classes.DomoDatacenter as dmdc
    import domolibrary.classes.DomoPublish as dmpb
    import domolibrary.client.DomoAuth as dmda

    FEDERATED_DS_ID = '58a75bc7-e626-4ea1-a3d9-b1ae96188b5c'

    child_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN")
    )

    # i should be able to "get_all datasets and have a list of 'normal' and federated datasets"
    ## PART 2!!!!
    #all_datasets : List[Union[DomoDataset, FederatedDomoDataset]] = await dmdc.DomoDatacenter(auth= child_auth).search_datasets(maximum = 10)


    # i should be able to define a "retrieve_auth" function that receives a subscription and can return a DomoAuth object
    # this is necessary assuming i am trying to retrieve lineage but don't already know my parent


    def retreive_parent_auth_fn(subscription : dmpb.DomoSubscription) :

        ## AN EXAMPLE OF HOW IT OUGHT TO WORK -- assumes you have multiple DOMO instances and access tokens stored in environment variables
        # parent_domain = subscription.domain
        # parent_auth = dmda.DomoTokenAuth(
        #     domo_instance=parent_domain,
        #     domo_access_token=os.environ.get(f"DOMO_{parent_domain.upper()}_ACCESS_TOKEN")
        # )

        ## CHEATING CODE
        parent_auth = dmda.DomoTokenAuth(
            domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
            domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN")
        )

        return parent_auth

    parent_auth = dmda.DomoTokenAuth(
            domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
            domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN")
        )

    # the Lineage function should be able to use the retreive_parent_auth_fn function to get the parent auth
    # the Lineage class should be able to use methods embedded in the DomoFederatedEntity class to retrieve parent and child entities

    # PART 1.a
    ds = await FederatedDomoDataset.get_by_id(dataset_id = FEDERATED_DS_ID, auth = child_auth)

    try:
        await ds.get_federated_parent(parent_auth_retrieval_fn=retreive_parent_auth_fn)
    except Exception as e:  
        print(e)
