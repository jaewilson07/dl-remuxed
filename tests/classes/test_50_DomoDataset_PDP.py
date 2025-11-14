r"""
Test file generated from 50_DomoDataset_PDP.ipynb
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
    param = PDP_Parameter(column_name="instance", column_values_ls=[os.environ['DOMO_INSTANCE']])

    PDP_Parameter.generate_body_from_parameter(param)
