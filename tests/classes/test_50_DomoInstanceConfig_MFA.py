"""
Test file generated from 50_DomoInstanceConfig_MFA.ipynb
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
    community_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await community_auth.print_is_token()

    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_DATACREW_INSTANCE"],
        domo_access_token=os.environ["DOMO_DATACREW_ACCESS_TOKEN"],
    )
    await auth.print_is_token()


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    mfa_config = await MFA_Config.get_instance_config(
        auth=auth, return_raw=False, debug_num_stacks_to_drop=2
    )

    await mfa_config.toggle_mfa(is_enable_MFA=None, debug_api=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await mfa_config.update(
        is_enable_MFA=True, max_code_attempts=7, num_days_valid=32, debug_prn=True
    )
