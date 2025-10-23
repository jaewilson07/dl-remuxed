"""
Test file generated from instance_config_scheduler_policies.ipynb
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
    load_dotenv(override=True)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    # await token_auth.who_am_i()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    try:
        res = await get_scheduler_policies(
            auth = token_auth
        )
        print(f"Found {len(res.response)} policies")

    except dmde.DomoError as e:
        print(e)

    policy_id = res.response[0]['id']
    policy_id
