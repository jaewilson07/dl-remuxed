"""
Test file generated from 50_DomoInstanceConfig_Scheduler_Policies.ipynb
Auto-generated - excludes cells starting with #
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
from domolibrary2.client.auth import DomoTokenAuth
from domolibrary2.classes.DomoInstanceConfig.scheduler_policies import (
    DomoScheduler_Policies,
    DomoScheduler_Policy_Restrictions,
)

# Setup authentication for tests
token_auth = DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)
scheduler_policies = DomoScheduler_Policies(auth=token_auth, parent=None, parent_id="")  # type: ignore
SCHEDULER_POLICY_ID = "f6bd6eee-e5e9-4082-b43d-147b2b75f90d"


async def test_get_scheduler_policies(token_auth=token_auth):
    """Test case from cell 2"""
    policies = await scheduler_policies.get()
    return policies


async def test_upsert_scheduler_policy(token_auth=token_auth):
    """Test case from cell 3"""
    policy = scheduler_policies.policies[0]
    policy.id = None
    policy.name = "copy of " + policy.name
    policy.frequencies.connector_frequency = DomoScheduler_Policy_Restrictions.HOURLY
    policy.frequencies.dataflow_frequency = (
        DomoScheduler_Policy_Restrictions.NO_RESTRICTIONS
    )
    await scheduler_policies.upsert(policy)
    await scheduler_policies.get()


async def test_delete_scheduler_policy(token_auth=token_auth):
    """Test case from cell 4"""

    await scheduler_policies.delete(str(scheduler_policies.policies[-1].id))
    await scheduler_policies.get()


if __name__ == "__main__":
    r = asyncio.run(test_get_scheduler_policies(token_auth=token_auth))
    print(r)
    r = asyncio.run(test_upsert_scheduler_policy(token_auth=token_auth))
    print(r)
    r = asyncio.run(test_delete_scheduler_policy(token_auth=token_auth))
    print(r)
