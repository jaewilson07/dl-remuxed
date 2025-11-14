r"""
Test file generated from 50_DomoCard.ipynb
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
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )



async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_card = await DomoCard.get_by_id(card_id=CARD_ID, auth=auth, return_raw=False)
    pprint(domo_card)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await domo_card.get_datasets(return_raw=False)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    domo_group = await dmgr.DomoGroup.get_by_id(group_id=1324037627, auth=auth)
    domo_group

    domo_card = await DomoCard.get_by_id(card_id=1766265020, auth=auth)

    await domo_card.share(
        auth=auth,
        domo_groups=[domo_group],
        message=None,
        debug_api=False,
    )


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    domo_card = await DomoCard.get_by_id(card_id=CARD_ID_APP, auth=auth, return_raw=False)

    pprint(await domo_card.get_source_code())


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    domo_card = await DomoCard.get_by_id(card_id=CARD_ID_APP, auth=auth, return_raw=False)

    pprint(await domo_card.download_source_code(download_folder="../../test/ddx/"))


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await domo_card.Lineage.get()

    domo_card.Lineage


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    class FederatedDomoCard(DomoCard, DomoFederatedEntity):
        pass
