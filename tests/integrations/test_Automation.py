r"""
Test file generated from Automation.ipynb
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
    dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await search_or_upsert_domo_group(auth = token_auth, group_name = 'dev_jupyter')


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    domo_accounts = dmacc.DomoAccounts(auth=token_auth)
    await domo_accounts.get()

    domo_account = domo_accounts.accounts[1]

    await share_domo_account_with_domo_group(
        auth=token_auth,
        account_name=domo_account.name,
        group_name="dev_jupyter",
        upsert_group_if_no_exist=True,
        is_hide_system_groups=False,
        debug_api=False,
    )
