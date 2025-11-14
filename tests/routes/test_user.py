import os

from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
import domolibrary2.routes.user as user_routes

load_dotenv()


# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_cell_2(token_auth=token_auth):
    import pandas as pd

    """Test case from cell 2"""
    users = (await user_routes.get_all_users(auth=token_auth)).response

    print(len(users))
    df = pd.DataFrame(users[0:5])
    print(df)
    return True


# async def test_cell_5(token_auth=token_auth):

#     img_path = "../test/1833256765.png"

#     with open(img_path, "rb") as f:
#         bytestr = f.read()

#     await user_routes.upload_avatar(
#         user_id=test_user["id"],
#         auth=auth,
#         debug_api=False,
#         img_bytestr=bytestr,
#         img_type="jpg",
#     )


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_cell_2())
