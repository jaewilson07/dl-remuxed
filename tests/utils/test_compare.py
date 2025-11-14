r"""
Test file generated from compare.ipynb
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
    dict1 = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 4,
                'e': [1, 2, 3]
            }
        }

    dict2 = {
            'a': 1,
            'b': 3,
            'c': {
                'd': 4,
                'e': [1, 2]
            },
            'f': 99
        }

    compare_dicts(dict1, dict2)
