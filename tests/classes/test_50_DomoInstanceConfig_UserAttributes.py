r"""
Test file generated from 50_DomoInstanceConfig_UserAttributes.ipynb
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
    show_doc(UserAttribute.get_by_id)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(UserAttribute.update)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    show_doc(UserAttributes.create)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    show_doc(UserAttributes.delete)
