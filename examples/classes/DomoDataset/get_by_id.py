import domolibrary2.classes.DomoDataset as dmds
import domolibrary2.client.auth as dmda
import os
from dotenv import load_dotenv

assert load_dotenv(".env")


async def main():
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_CHILD_INSTANCE"],
        domo_access_token=os.environ["DOMO_CHILD_ACCESS_TOKEN"],
    )

    print(await auth.who_am_i(debug_api=True))
    ds = await dmds.DomoDataset.get_by_id(os.environ["CHILD_DATASET_ID"], auth=auth)

    print(ds)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
