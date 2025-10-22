"""
Test file generated from 50_DomoApplication.ipynb
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
        domo_instance="domo-alpha",
        domo_access_token=os.environ["ALPHA_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    res = await application_routes.get_applications(auth = token_auth)

    pprint([app.get('name') for app in res.response])

    rds_app = next((obj for obj in res.response if "Remote Domo Stats" in obj['name']))


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await test_application.get_jobs()
