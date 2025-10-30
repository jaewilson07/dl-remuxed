import os
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoDataset as dmds
from dotenv import load_dotenv

assert load_dotenv()


CHILD_DATASET_ID = os.environ.get("CHILD_DATASET_ID")

child_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
    domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN"),
)

parent_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
    domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
)


def retreive_parent_auth_fn(subscription=None):

    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN"),
    )

    return parent_auth


async def dataset_lineage_test(token_auth=child_auth):

    ds = await dmds.FederatedDomoDataset.get_by_id(
        dataset_id=CHILD_DATASET_ID, auth=child_auth
    )

    await ds.get_federated_parent(
        parent_auth=parent_auth, parent_auth_retrieval_fn=retreive_parent_auth_fn
    )

    lineage = await ds.Lineage.get(
        parent_auth=parent_auth, parent_auth_retrieval_fn=retreive_parent_auth_fn
    )
    print(lineage)
    return lineage


async def main():
    test_fns = [
        dataset_lineage_test,
    ]

    for test_fn in test_fns:
        print(f"Running {test_fn.__name__}...")
        await test_fn(token_auth=child_auth)
        print(f"Completed {test_fn.__name__}.\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
