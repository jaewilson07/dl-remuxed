r"""
Test file generated from publish.ipynb
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
    dmda.DomoTokenAuth(
        domo_instance= 'domo-community',
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    res = await search_publications(auth=token_auth,
                                    debug_loop = True,
                                    )

    res.response[0]
    pd.DataFrame(res.response[0:5])


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    res = await get_publish_subscriptions(auth=token_auth, publish_id=publication['id'])
    res.response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    (await get_publish_subscriptions(auth=token_auth, publish_id=publication['id'])).response
