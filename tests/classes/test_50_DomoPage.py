"""
Test file generated from 50_DomoPage.ipynb
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
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    page_id = 384424178
    page_id = 790951325


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await DomoPage.get_by_id(auth = token_auth, page_id = page_id)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    dmic_pages = DomoPages(auth = token_auth)
    (await dmic_pages.get())[0:5]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_page = await DomoPage.get_by_id(
        page_id=1222214176,
        auth=token_auth,
        return_raw=False,
        include_layout=True,
    )


    await domo_page.get_parents()


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    show_doc(DomoPage.test_page_access)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_page = await DomoPage.get_by_id(page_id=page_id, auth=token_auth)

    (await domo_page.get_accesslist(return_raw=False, debug_api=False))['domo_users'][0:5]


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    try:
        print((await domo_page.get_cards()))
    except dmde.DomoError as e:
        print(e)


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    try:
        print((await domo_page.get_datasets()))

    except dmde.DomoError as e:

        print(e)


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    await token_auth.who_am_i()
    domo_users = await dmdu.DomoUsers.all_users(auth = token_auth)

    await domo_page.add_owner( group_id_ls=[], user_id_ls=[token_auth.user_id]
    )


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    await domo_page.Lineage.get()
