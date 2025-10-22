"""
Test file generated from 50_DomoAccount.ipynb
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
        domo_instance=os.environ["DOMO_DOJO_INSTANCE"],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    account = (await account_routes.get_account_by_id(auth=auth, account_id=71)).response

    account_id = account["id"]
    account


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_account = await DomoAccount.get_by_id(
        auth=auth, account_id=account_id, is_use_default_account_class=True
    )
    domo_account


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_account.name = f"DomoLibrary - update {dt.datetime.now()}"
    await domo_account.update_name()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await auth.who_am_i()

    await domo_account.Access.share(user_id=auth.user_id)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    alpha_auth = dmda.DomoTokenAuth(
        domo_instance="domo-alpha",
        domo_access_token=os.environ["ALPHA_ACCESS_TOKEN"],
    )

    domo_account = await DomoAccount.get_by_id(account_id=5, auth=alpha_auth)
    try:
        print(
            await domo_account.Access.share(
                relation_type=ShareAccount_AccessLevel.CAN_VIEW,
                group_id=1814479647,
                debug_api=False,
            )
        )

    except Account_Share_Error as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_accounts = DomoAccounts(auth=auth)
    (await domo_accounts.get())[0:5]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await domo_accounts.get_oauths()
