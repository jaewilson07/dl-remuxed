"""
Test file generated from 50_DomoActivityLog.ipynb
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
    end_datetime = dt.datetime.today()
    start_datetime = end_datetime - dt.timedelta(days=100)

    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ['DOMO_INSTANCE'],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    al_res = await DomoActivityLog.get_activity_log(
        auth=token_auth,
        start_time=start_datetime,
        end_time=end_datetime,
        object_type=ActivityLog_ObjectType.ACTIVITY_LOG,
        maximum=5,
    )

    pd.DataFrame(al_res)
