"""
Test file generated from xkcd_pass.ipynb
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
    sample_password = "hello world i am a wombat"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    add_leet_to_string('hello world', LEET)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    add_padding_characters_fn('hello', padding = PADDING , n =2 )


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    generate_xkcd_password()


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    {
        "random": process_random_capitalization_fn(sample_password, delimiter=" ")[0],
        "first": process_first_capitalization_fn(sample_password, delimiter=" ")[0],
    }


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    generate_domo_password(delimiter="-")
