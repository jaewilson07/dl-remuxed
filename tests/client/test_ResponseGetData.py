"""
Test file generated from ResponseGetData.ipynb
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
    rgd = ResponseGetData(status=200, response="test", is_success=True)
    rgd


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(ResponseGetData._from_requests_response)
