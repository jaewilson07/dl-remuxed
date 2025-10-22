"""
Test file generated from build.ipynb
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
    import domolibrary.client.DomoAuth as dmda
    import os


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    CARD_ID = 1952029522


    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


    CARD_ID = 1241065508
    token_auth = dmda.DomoTokenAuth(
        domo_instance="datacrew-space",
        domo_access_token=os.environ["DOMO_DATACREW_ACCESS_TOKEN"],
    )

    await token_auth.who_am_i()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    import domolibrary.classes.DomoCard as dmdc

    domo_card = await dmdc.DomoCard.get_by_id(card_id = CARD_ID, 
                                              auth = token_auth, 
                                              debug_api = False,
                                              return_raw= False)

    print(domo_card.display_url())
    domo_card.raw


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await domo_card.Lineage.get(debug_api = True)

    # print(len(domo_card.Lineage.lineage))
    # for lin in domo_card.Lineage.lineage:
    #     print(lin.entity.name)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    sub_dataset_relation = domo_card.Lineage.lineage[0]
    sub_dataset = sub_dataset_relation.entity
    # await sub_dataset.Lineage.get(debug_api = True)

    sub_dataset.raw
