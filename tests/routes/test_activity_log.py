r"""
Test file generated from activity_log.ipynb
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
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
        domo_instance=os.environ['DOMO_INSTANCE'],
    )

    page_res = await search_activity_log(
        object_type="PAGE",
        start_time=convert.convert_datetime_to_epoch_millisecond(start_datetime),
        end_time=convert.convert_datetime_to_epoch_millisecond(end_datetime),
        auth=token_auth,
        # maximum=16,
        debug_loop=False,
        debug_api=False,
    )
    page_res
    # pd.DataFrame(page_res.response[0:5])
