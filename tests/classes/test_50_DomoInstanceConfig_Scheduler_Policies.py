"""
Test file generated from 50_DomoInstanceConfig_Scheduler_Policies.ipynb
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
    load_dotenv(override = True)
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    SCHEDULER_POLICY_ID = "f6bd6eee-e5e9-4082-b43d-147b2b75f90d"


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    policies = DomoScheduler_Policies(auth = token_auth)
    await policies.get()


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    policy = policies.policies[0]
    policy.id = None
    policy.name = "copy of " + policy.name
    policy.frequencies.connector_frequency = DomoScheduler_Policy_Restrictions.HOURLY
    policy.frequencies.dataflow_frequency = DomoScheduler_Policy_Restrictions.NO_RESTRICTIONS
    await policies.upsert(policy)
    await policies.get()


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await policies.delete(str(policies.policies[-1].id))
    await policies.get()
