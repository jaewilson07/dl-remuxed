r"""
Test file generated from page.ipynb
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
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()



async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    show_doc(get_page_by_id)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    show_doc(get_page_definition)
