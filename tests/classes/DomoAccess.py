r"""
Test file generated from 50_DomoAccess.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os

import domolibrary2.auth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    account_access = DomoAccess_Account(
        auth=auth,
        # version=2,
        # share_enum=ShareAccount_AccessLevel.CAN_SHARE,
        parent_id=71,
        parent=None,
    )

    await account_access.get(debug_api=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    try:
        print(await account_access.get_all_users())

    except dmde.DomoError as e:
        print(e)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    if not auth.user_id:
        await auth.who_am_i()

    try:
        await account_access.share(
            user_id=auth.user_id,
            relation_type=account_routes.ShareAccount_AccessLevel.CAN_EDIT,
            debug_api=False,
        )

    except Account_Share_Error as e:
        print(e)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    try:
        await account_access.upsert_share(
            user_id=auth.user_id,
            relation_type=account_routes.ShareAccount_AccessLevel.OWNER,
            debug_api=False,
        )

    except Account_Share_Error as e:
        print(e)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    oauth_account_id = 1
    domo_access = DomoAccess_OAuth(auth=auth, parent_id=oauth_account_id, parent=None)

    await domo_access.get(return_raw=False)
