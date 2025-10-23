"""
Comprehensive tests for domolibrary2.client.auth using the test harness.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from dotenv import load_dotenv
import os

import domolibrary2.client.auth as dmda
from domolibrary2.client.response import ResponseGetData, RequestMetadata
from domolibrary2.client.exceptions import AuthError, InvalidCredentialsError
from tests.tools.test_harness import (
    RouteTestHarness,
    TestScenario,
    MockResponse,
    RouteTestBuilder,
    PytestRouteTestCase,
    IntegrationTestHarness,
)

load_dotenv()


async def test_domo_auth_who_am_i():
    """Test DomoAuth who_am_i method."""
    domo_auth = dmda.DomoTokenAuth(
        domo_access_token=os.getenv("DOMO_ACCESS_TOKEN"),
        domo_instance=os.getenv("DOMO_INSTANCE"),
    )

    res = await domo_auth.who_am_i()

    return res.is_success
