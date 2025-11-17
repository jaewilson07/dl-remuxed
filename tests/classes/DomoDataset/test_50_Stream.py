"""
Test file for DomoStream class
Tests the Stream class functionality including get_by_id and from_dict methods
"""

import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.routes.stream as stream_routes
from domolibrary2.classes.DomoDataset.Stream import DomoStream, Stream_GET_Error, Stream_CRUD_Error

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test stream IDs - these should be set in your .env file
TEST_STREAM_ID_1 = os.environ.get("STREAM_ID_1", None)
TEST_STREAM_ID_2 = os.environ.get("STREAM_ID_2", None)


async def test_cell_0(token_auth=token_auth) -> bool:
    """Helper function to test authentication."""
    if not token_auth.user_id:
        await token_auth.who_am_i()
    return bool(token_auth.user_id)


async def test_cell_1(token_auth=token_auth) -> DomoStream:
    """Test get_by_id method - retrieve a stream by its ID."""
    if not TEST_STREAM_ID_1:
        print("WARNING: STREAM_ID_1 not set in .env file - test will be skipped")
        return None

    domo_stream = await DomoStream.get_by_id(
        auth=token_auth,
        stream_id=TEST_STREAM_ID_1,
        return_raw=False,
        debug_api=False
    )

    print(f"Stream ID: {domo_stream.id}")
    print(f"Dataset ID: {domo_stream.dataset_id}")
    print(f"Data Provider: {domo_stream.data_provider_name}")
    print(f"Display URL: {domo_stream.display_url}")

    return domo_stream


async def test_cell_2(token_auth=token_auth):
    """Test from_dict method - create DomoStream from dictionary."""
    # Sample stream response data
    sample_stream_data = {
        "id": "test-stream-123",
        "dataProvider": {
            "name": "Snowflake",
            "key": "snowflake"
        },
        "transport": {
            "description": "Transport Description",
            "version": 1
        },
        "dataSource": {
            "id": "test-dataset-456"
        },
        "updateMethod": "REPLACE",
        "configuration": [
            {
                "name": "query",
                "type": "TEXT",
                "value": "SELECT * FROM test_table"
            }
        ]
    }

    domo_stream = DomoStream.from_dict(auth=token_auth, obj=sample_stream_data)

    assert domo_stream.id == "test-stream-123"
    assert domo_stream.dataset_id == "test-dataset-456"
    assert domo_stream.data_provider_name == "Snowflake"
    assert domo_stream.data_provider_key == "snowflake"
    assert len(domo_stream.configuration) == 1

    print("from_dict test passed!")
    print(f"Stream ID: {domo_stream.id}")
    print(f"Dataset ID: {domo_stream.dataset_id}")

    return domo_stream


async def test_cell_3(token_auth=token_auth):
    """Test return_raw parameter - should return ResponseGetData object."""
    if not TEST_STREAM_ID_1:
        print("WARNING: STREAM_ID_1 not set in .env file - test will be skipped")
        return None

    res = await DomoStream.get_by_id(
        auth=token_auth,
        stream_id=TEST_STREAM_ID_1,
        return_raw=True
    )

    # Should be ResponseGetData, not DomoStream
    assert hasattr(res, 'is_success')
    assert hasattr(res, 'response')

    print(f"Raw response returned successfully")
    print(f"Status: {res.status}")

    return res


async def test_cell_4(token_auth=token_auth):
    """Test legacy get_stream_by_id method - should still work for backwards compatibility."""
    if not TEST_STREAM_ID_1:
        print("WARNING: STREAM_ID_1 not set in .env file - test will be skipped")
        return None

    # Test deprecated method
    domo_stream = await DomoStream.get_stream_by_id(
        auth=token_auth,
        stream_id=TEST_STREAM_ID_1,
        return_raw=False
    )

    assert domo_stream.id == TEST_STREAM_ID_1
    print("Legacy get_stream_by_id method works correctly")

    return domo_stream


async def test_cell_5(token_auth=token_auth):
    """Test error handling - invalid stream ID should raise Stream_GET_Error."""
    try:
        await DomoStream.get_by_id(
            auth=token_auth,
            stream_id="invalid-stream-id-12345",
            return_raw=False
        )
        print("ERROR: Should have raised Stream_GET_Error")
        assert False, "Expected Stream_GET_Error but no exception was raised"
    except Stream_GET_Error as e:
        print(f"Expected error caught: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        return True


async def test_cell_6(token_auth=token_auth):
    """Test stream configuration mapping."""
    if not TEST_STREAM_ID_1:
        print("WARNING: STREAM_ID_1 not set in .env file - test will be skipped")
        return None

    domo_stream = await DomoStream.get_by_id(
        auth=token_auth,
        stream_id=TEST_STREAM_ID_1,
        return_raw=False
    )

    # Test configuration report generation
    config_report = domo_stream.generate_config_rpt()

    print(f"Has mapping: {domo_stream.has_mapping}")
    print(f"Configuration count: {len(domo_stream.configuration)}")
    print(f"Configuration report: {config_report}")

    if domo_stream.configuration_query:
        print(f"Query detected: {domo_stream.configuration_query[:100]}...")

    if domo_stream.configuration_tables:
        print(f"Tables: {domo_stream.configuration_tables}")

    return config_report


async def main(token_auth=token_auth):
    """Run all test functions."""
    fn_ls = [
        test_cell_0,
        test_cell_1,
        test_cell_2,
        test_cell_3,
        test_cell_4,
        test_cell_5,
        test_cell_6,
    ]
    for fn in fn_ls:
        print(f"\n{'='*60}")
        print(f"Running {fn.__name__}: {fn.__doc__}")
        print('='*60)
        try:
            await fn(token_auth=token_auth)
        except Exception as e:
            print(f"Test failed with error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main(token_auth=token_auth))
