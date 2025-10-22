"""
Test file generated from 99_DomoEntity.ipynb
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
    parent_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_PARENT_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_PARENT_ACCESS_TOKEN")
    )

    child_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get("DOMO_CHILD_INSTANCE"),
        domo_access_token=os.environ.get("DOMO_CHILD_ACCESS_TOKEN")
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    class TestEnum(DomoEnum):
        default = "default"
        value1 = "value1"
        value2 = "value2"
        value3 = "value3"

    TestEnum.get('abc')
