"""
Test file generated from 50_DomoAccount_Default.ipynb
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
        domo_instance=os.environ['DOMO_DOJO_INSTANCE'],
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    account = (await account_routes.get_account_by_id(auth =token_auth, account_id = 71)).response

    account_id = account['id']
    account


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    account_id = 145

    domo_account = await DomoAccount_Default.get_by_id(
        auth=token_auth,
        account_id=account_id,
        is_unmask = False,
        is_suppress_no_config=False,
        debug_api=False,
        return_raw=False,
    )

    print(domo_account)
    print(domo_account.Config)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_account = await DomoAccount_Default.get_by_id(auth=token_auth, account_id=account_id)
    domo_account.name = f"DomoLibrary - update {dt.datetime.now()}"
    await domo_account.update_name()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await domo_account.Access.get()


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_account = await DomoAccount_Default.get_by_id(account_id=5, auth=token_auth)

    domo_account.display_url()

    if not token_auth.user_id:
        await token_auth.who_am_i()

    try:
        print(
            await domo_account.Access.share(
                relation_type=ShareAccount_AccessLevel.OWNER,
                user_id=token_auth.user_id,
                debug_api=True,
            )
        )

    except Account_Share_Error as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_account = await DomoAccount_Default.get_by_id(account_id=45, auth=token_auth)
    try:
        print(
            await dmce.gather_with_concurrency(
                *[
                    domo_account.Access.share(
                        relation_type=ShareAccount_AccessLevel.CAN_EDIT,
                        user_id=token_auth.user_id,
                        debug_api=False,
                    )
                ],
                n=10 ))

    except Account_Share_Error as e:
        print(e)
