r"""
Test file generated from 50_DomoApplication_Job_Watchdog.ipynb
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
        domo_instance="domo-alpha",
        domo_access_token=os.environ["ALPHA_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    obj = {
        "entityIds": [
            "39ee901e-ab22-4c7c-aab2-010c80da8d52",
            "384ef8ba-0782-4062-be99-671fa46badd7",
        ],
        "type": "custom_query",
        "entityType": "DATA_SOURCE",
        "sqlQuery": "SELECT * FROM TABLE",
    }

    s = Watchdog_ConfigFactory[obj["type"].upper()].value._from_dict(obj)

    s.to_dict()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await test_job.execute()
