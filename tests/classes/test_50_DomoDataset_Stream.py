"""
Test file for DomoDataset Stream class
Tests validation of Stream class implementation following domolibrary2 standards
"""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
from domolibrary2.classes.DomoDataset.Stream import DomoStream, DomoStreams
from domolibrary2.classes.DomoDataset.stream_config import (
    StreamConfig_Mappings,
)
from domolibrary2.routes import stream as stream_routes

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


@pytest.mark.asyncio
async def test_get_streams(token_auth=token_auth):
    """Test getting a list of streams"""
    res = await stream_routes.get_streams(
        auth=token_auth, maximum=5, loop_until_end=False
    )

    assert res.is_success
    assert res.response is not None
    assert isinstance(res.response, list)

    if len(res.response) > 0:
        stream = res.response[0]
        assert "id" in stream
        return stream["id"]


@pytest.mark.asyncio
async def test_stream_config_mappings():
    """Test stream config mappings search"""
    data_provider_type = "aws-athena"
    mapping = StreamConfig_Mappings.search(data_provider_type)

    assert mapping is not None
    assert mapping == StreamConfig_Mappings.aws_athena


@pytest.mark.asyncio
async def test_get_stream_by_id(token_auth=token_auth):
    """Test getting a stream by ID"""
    # First get a stream ID
    stream_id = await test_get_streams(token_auth)

    if stream_id:
        stream = await DomoStream.get_by_id(auth=token_auth, stream_id=stream_id)

        assert stream is not None
        assert isinstance(stream, DomoStream)
        assert stream.id == stream_id
        assert stream.auth == token_auth

        return stream


@pytest.mark.asyncio
async def test_stream_display_url(token_auth=token_auth):
    """Test stream display URL generation"""
    stream = await test_get_stream_by_id(token_auth)

    if stream and stream.parent:
        url = stream.display_url
        assert url is not None
        assert "domo.com" in url
        assert stream.parent.id in url


@pytest.mark.asyncio
async def test_domo_streams_manager(token_auth=token_auth):
    """Test DomoStreams manager class"""
    streams = DomoStreams(auth=token_auth)

    # Note: This might be slow as it searches all datasets
    # Uncomment to test if needed
    # result = await streams.get(search_dataset_name="test")
    # assert isinstance(result, list)

    assert streams.auth == token_auth

