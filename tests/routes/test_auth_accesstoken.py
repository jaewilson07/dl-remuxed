"""
Test file generated from auth_accesstoken.ipynb
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


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    res = await get_access_tokens(debug_api=False, auth=token_auth)

    pd.DataFrame([r for r in res.response[0:5] if r["ownerId"] == 1216550715])


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    generate_expiration_unixtimestamp(1, debug_prn=True)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    user = (await token_auth.who_am_i()).response

    res_generate_token = await generate_access_token(
        user_id=user["id"], duration_in_days=90, token_name="DL_test", auth=token_auth
    )

    res_generate_token


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    access_token_id = res_generate_token.response["id"]

    await revoke_access_token(
        auth=token_auth, access_token_id=access_token_id, debug_api=False
    )
