"""
Test file generated from appstudio.ipynb
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
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    appstudio_id = 1196847240

    (await get_appstudio_by_id(appstudio_id=appstudio_id, auth=token_auth)).response


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    appstudio_id = 1196847240

    (
        await get_appstudio_access(
            appstudio_id=appstudio_id,
            auth=token_auth,
        )
    ).response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await get_appstudios_adminsummary(auth=token_auth, debug_loop=False, debug_api=False)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    appstudio_id = 1902414365

    try:
        user_id = "1893952720"
        print(
            (
                await add_page_owner(
                    appstudio_id_ls=[appstudio_id],
                    auth=token_auth,
                    group_id_ls=[],
                    user_id_ls=[user_id],
                )
            ).response
        )
    except:
        print("Error")


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    (
        await share(
            auth=token_auth,
            appstudio_ids=[1902414365],
            group_ids=[1227809530],
            message=None,
            debug_api=False,
        )
    ).response
