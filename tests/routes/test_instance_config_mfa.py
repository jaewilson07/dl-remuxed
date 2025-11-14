r"""
Test file generated from instance_config_mfa.ipynb
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
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    # auth = dmda.DomoTokenAuth(
    #     domo_instance=os.environ["DOMO_DATACREW_INSTANCE"],
    #     domo_access_token=os.environ["DOMO_DATACREW_ACCESS_TOKEN"],
    # )
    await auth.print_is_token()
