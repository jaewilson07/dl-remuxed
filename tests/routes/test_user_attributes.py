"""
Test file generated from user_attributes.ipynb
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
    [{member.name, member.value} for member in UserAttributes_IssuerType]


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(get_user_attributes)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    show_doc(get_user_attribute_by_id)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    show_doc(update_user_attribute)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    show_doc(delete_user_attribute)
