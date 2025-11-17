r"""
Test file for card route functions.
"""

import os

import pytest
import domolibrary2.auth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ.get('DOMO_INSTANCE', 'test-instance'),
    domo_access_token=os.environ.get('DOMO_ACCESS_TOKEN', 'test-token'),
)


@pytest.mark.asyncio
async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ.get('DOMO_INSTANCE', 'test-instance'),
        domo_access_token=os.environ.get("DOMO_ACCESS_TOKEN", 'test-token'),
    )
    assert auth is not None

