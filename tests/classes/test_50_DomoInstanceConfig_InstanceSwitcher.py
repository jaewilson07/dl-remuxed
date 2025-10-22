"""
Test file generated from 50_DomoInstanceConfig_InstanceSwitcher.ipynb
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

    # auth = dmda.DomoTokenAuth(
    #     domo_instance=os.environ["DOMO_DATACREW_INSTANCE"],
    #     domo_access_token=os.environ["DOMO_DATACREW_ACCESS_TOKEN"],
    # )
    # await auth.print_is_token()
