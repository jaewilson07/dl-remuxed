"""
Test file generated from beastmode.ipynb
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
    import os


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    bms = (await search_beastmodes(auth=auth)).response
    bms[0:1]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await lock_beastmode(beastmode_id=bms[0]["id"], auth=auth, is_locked=True)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await get_beastmode_by_id(beastmode_id=88, auth=auth)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    card_id = 2056437956
    res = await get_card_beastmodes(card_id=card_id, auth=auth, return_raw=True)
    all_bms = res.response


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await get_dataset_beastmodes(
        dataset_id="d40a70b1-d9a2-4145-b361-18ccf1fb3978", auth=auth
    )


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    page_id = 1845973736
    (await get_page_beastmodes(page_id = page_id, auth = auth))


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    async def page_toggle_beastmode_lock(page_id, is_locked,  auth):
        bms = await get_page_beastmodes(page_id = page_id, auth = auth)

        await dmce.gather_with_concurrency(*[ lock_beastmode(beastmode_id = bm['id'], auth = auth, is_locked = True) for bm in bms], n = 10)

        return f"{'locked' if is_locked else 'unlocked'} beast modes on {page_id}"

    await page_toggle_beastmode_lock(page_id = page_id, is_locked = False, auth = auth)
