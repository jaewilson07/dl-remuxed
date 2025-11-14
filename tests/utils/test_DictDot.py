r"""
Test file generated from DictDot.ipynb
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
    foo = {
        "name": "my object",
        "description": "please convert me",
        "type": "a good old fashioned dictionary",
    }

    dd = DictDot(foo)

    print(dd)

    dd.type


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    dd = split_str_to_obj(
        piped_str="test_instance|myemail|sample_password",
        key_ls=["domo_instance", "domo_username", "domo_password"],
    )

    dd.domo_instance
