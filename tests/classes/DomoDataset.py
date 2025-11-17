r"""
Test file generated from 50_DomoDataset.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os

from dotenv import load_dotenv

import domolibrary2.classes.DomoDataset as dmds
import domolibrary2.auth as dmda

assert load_dotenv()


# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

dataset_id = os.environ["FEDERATED_DS_ID"]

federated_ds_id = os.environ["FEDERATED_DS_ID"]


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN"),
    )

    print("hello world")

    assert await token_auth.who_am_i()


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    assert await dmds.DomoDataset.get_by_id(dataset_id=dataset_id, auth=token_auth)


async def test_cell_2a(token_auth=token_auth):
    domo_dataset = await dmds.DomoDataset.get_by_id(
        dataset_id=dataset_id, auth=token_auth
    )
    assert await domo_dataset.Schema.get()


async def test_cell_3(token_auth=token_auth):
    domo_dataset = await dmds.DomoDataset.get_by_id(
        auth=token_auth, dataset_id=dataset_id
    )

    print(await domo_dataset.Data.list_partitions(debug_api=False))

    return True


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""

    assert await dmds.DomoDataset.get_by_id(
        dataset_id=federated_ds_id, auth=token_auth, is_use_default_dataset_class=False
    )


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    fds = await dmds.DomoDataset.get_by_id(
        dataset_id=federated_ds_id, auth=token_auth, is_use_default_dataset_class=False
    )

    await fds.Lineage.get(parent_auth=parent_auth)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""

    # import domolibrary2.classes.DomoDatacenter as dmdc
    # import domolibrary2.classes.DomoPublish as dmpb
    import domolibrary2.auth as dmda

    FEDERATED_DS_ID = "58a75bc7-e626-4ea1-a3d9-b1ae96188b5c"

    child_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN"),
    )

    # i should be able to "get_all datasets and have a list of 'normal' and federated datasets"
    ## PART 2!!!!
    # all_datasets : list[Union[DomoDataset, FederatedDomoDataset]] = await dmdc.DomoDatacenter(auth= child_auth).search_datasets(maximum = 10)

    # i should be able to define a "retrieve_auth" function that receives a subscription and can return a DomoAuth object
    # this is necessary assuming i am trying to retrieve lineage but don't already know my parent

    def retreive_parent_auth_fn(subscription=None):

        ## AN EXAMPLE OF HOW IT OUGHT TO WORK -- assumes you have multiple DOMO instances and access tokens stored in environment variables
        # parent_domain = subscription.domain
        # parent_auth = dmda.DomoTokenAuth(
        #     domo_instance=parent_domain,
        #     domo_access_token=os.environ.get(f"DOMO_{parent_domain.upper()}_ACCESS_TOKEN")
        # )

        ## CHEATING CODE
        parent_auth = dmda.DomoTokenAuth(
            domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
            domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
        )

        return parent_auth

    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    # the Lineage function should be able to use the retreive_parent_auth_fn function to get the parent auth
    # the Lineage class should be able to use methods embedded in the DomoFederatedEntity class to retrieve parent and child entities

    # PART 1.a
    ds = await dmds.FederatedDomoDataset.get_by_id(
        dataset_id=FEDERATED_DS_ID, auth=child_auth
    )

    await ds.get_federated_parent(
        parent_auth=parent_auth, parent_auth_retrieval_fn=retreive_parent_auth_fn
    )

    await ds.Lineage.get(
        parent_auth=parent_auth, parent_auth_retrieval_fn=retreive_parent_auth_fn
    )

    # print(test)

    # try:
    #     await ds.get_federated_parent(parent_auth_retrieval_fn=retreive_parent_auth_fn)
    # except Exception as e:
    #     print(e)


async def main():
    test_fns = [
        # test_cell_1,
        # test_cell_2,
        # test_cell_3,
        # test_cell_4,
        # test_cell_5,
        test_cell_6,
    ]

    for test_fn in test_fns:
        print(f"Running {test_fn.__name__}...")
        await test_fn(token_auth=token_auth)
        print(f"Completed {test_fn.__name__}.\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
