"""
Test file generated from 50_DomoAccessToken.ipynb
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

    domo_user = await dmdu.DomoUser.get_by_id(user_id = token_auth.user_id, auth = token_auth)
    domo_user


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await DomoAccessToken.get_by_id(auth=token_auth, access_token_id=token.id)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_access_tokenstoken = await DomoAccessToken.generate(
        token_name=f"DL test {dt.date.today()}",
        owner=domo_user,
        duration_in_days=30,
        auth=token_auth,
        debug_api=False,
    )

    print(domo_access_tokenstoken)

    await domo_access_tokenstoken.regenerate()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_access_tokens = DomoAccessTokens(auth=token_auth)

    (await domo_access_tokens.get())[0:5]
