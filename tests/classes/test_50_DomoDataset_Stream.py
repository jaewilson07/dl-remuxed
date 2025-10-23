"""
Test file generated from 50_DomoDataset_Stream.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.routes.stream as stream_routes
from domolibrary2.classes.DomoDataset.Stream import DomoStream, StreamConfig_Mappings

load_dotenv()

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

    if not auth.user_id:
        await auth.who_am_i()

    res = await stream_routes.get_streams(auth=auth, maximum=5, loop_until_end=False)

    stream = res.response[0]
    stream_id = stream["id"]
    return stream


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    data_provider_type = "aws-athena"
    result = StreamConfig_Mappings.search(data_provider_type)
    print(f"Mapping found: {result}")
    return result


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    # Get a stream ID first
    res = await stream_routes.get_streams(auth=token_auth, maximum=1, loop_until_end=False)
    if res.response:
        stream_id = res.response[0]["id"]
        domo_stream = await DomoStream.get_by_id(auth=token_auth, stream_id=stream_id)
        print(f"Retrieved stream: {domo_stream.id}")
        return domo_stream
    else:
        print("No streams found to test")
        return None
