"""
Test file generated from 50_DomoIntegration.ipynb
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

    INTEGRATION_ID = "6475a657-6eda-4299-b43b-643d6977034d"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    (await DomoIntegration.get_by_id(auth = token_auth, integration_id = INTEGRATION_ID, return_raw = True)).response.keys()
