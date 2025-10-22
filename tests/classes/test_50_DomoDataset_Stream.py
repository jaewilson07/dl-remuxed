"""
Test file generated from 50_DomoDataset_Stream.ipynb
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
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()


    res = await stream_routes.get_streams(auth=auth, maximum=5, loop_until_end=False)

    stream = res.response[0]
    stream_id = stream["id"]
    stream


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    data_provider_type = "aws-athena"
    StreamConfig_Mappings.search(data_provider_type)
    # StreamConfig_Mappings('hello world')


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await DomoStream.get_stream_by_id(auth=auth, stream_id=stream_id)
