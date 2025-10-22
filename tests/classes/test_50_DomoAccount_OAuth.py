"""
Test file generated from 50_DomoAccount_OAuth.ipynb
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

    # res = await account_routes.get_oauth_accounts(auth=token_auth)

    # accounts = res.response
    # account = accounts[-1]

    # pd.DataFrame(accounts[0:5])


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_oauth = await DomoAccount_OAuth.get_by_id(
        account_id=1,
        auth=token_auth,
        # return_raw=False
    )

    domo_oauth


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    (await domo_oauth.Access.get())
