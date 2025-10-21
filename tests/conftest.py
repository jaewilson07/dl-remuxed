"""
pytest configuration for route testing.
"""

import pytest
import asyncio
from typing import Generator
import os
from unittest.mock import MagicMock

from .tools.test_harness import RouteTestHarness


# Configure pytest for async testing
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def route_harness() -> RouteTestHarness:
    """Provide a fresh route test harness for each test."""
    return RouteTestHarness(base_instance="test-instance")


@pytest.fixture
def mock_auth(route_harness):
    """Provide a mock authentication object."""
    return route_harness.default_auth


@pytest.fixture
def mock_developer_auth(route_harness):
    """Provide a mock developer authentication object."""
    return route_harness._create_mock_auth(auth_type="developer")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables and configurations."""
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["DOMO_TEST_INSTANCE"] = "test-instance"

    yield

    # Cleanup after tests
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
    if "DOMO_TEST_INSTANCE" in os.environ:
        del os.environ["DOMO_TEST_INSTANCE"]


@pytest.fixture
def mock_httpx_client():
    """Provide a mock httpx client for testing."""
    mock_client = MagicMock()
    mock_client.get = MagicMock()
    mock_client.post = MagicMock()
    mock_client.put = MagicMock()
    mock_client.delete = MagicMock()
    return mock_client


# Test data fixtures
@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "id": "user-123",
        "displayName": "Test User",
        "emailAddress": "test@example.com",
        "role": {"id": 1, "name": "Admin"},
        "department": "Engineering",
        "title": "Software Engineer",
    }


@pytest.fixture
def sample_dataset_data():
    """Provide sample dataset data for testing."""
    return {
        "id": "dataset-123",
        "name": "Test Dataset",
        "description": "A test dataset for unit testing",
        "rows": 1000,
        "columns": 5,
        "schema": {
            "columns": [
                {"name": "id", "type": "STRING"},
                {"name": "name", "type": "STRING"},
                {"name": "value", "type": "DOUBLE"},
                {"name": "date", "type": "DATE"},
                {"name": "active", "type": "BOOLEAN"},
            ]
        },
    }


@pytest.fixture
def sample_account_data():
    """Provide sample account data for testing."""
    return {
        "id": 123,
        "name": "Test Account",
        "type": "mysql",
        "displayType": "MySQL",
        "isConfigured": True,
        "isValid": True,
    }


# Markers for different test types
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (requires real API access)",
    )
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "slow: mark test as slow running")


# Custom pytest collection modifying hook
def pytest_collection_modifyitems(config, items):
    """Automatically add markers based on test names and locations."""
    for item in items:
        # Add integration marker for integration tests
        if "integration" in item.nodeid.lower():
            item.add_marker(pytest.mark.integration)

        # Add performance marker for performance tests
        if "performance" in item.nodeid.lower():
            item.add_marker(pytest.mark.performance)

        # Add slow marker for tests that take longer
        if "slow" in item.nodeid.lower():
            item.add_marker(pytest.mark.slow)


# Skip integration tests by default unless explicitly requested
def pytest_runtest_setup(item):
    """Skip integration tests unless specifically requested."""
    if "integration" in item.keywords and not item.config.getoption(
        "--run-integration"
    ):
        pytest.skip("Integration tests skipped (use --run-integration to run)")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="Run integration tests (requires real API credentials)",
    )
    parser.addoption(
        "--run-performance",
        action="store_true",
        default=False,
        help="Run performance tests",
    )


# Fixtures for integration testing (when credentials are available)
@pytest.fixture
def real_auth():
    """Provide real authentication for integration tests."""
    # This would load real credentials from environment or config
    # Only use for integration tests with proper credentials
    instance = os.getenv("DOMO_INSTANCE")
    token = os.getenv("DOMO_TOKEN")

    if not instance or not token:
        pytest.skip("Real credentials not available for integration test")

    # Import your real auth class here
    # from ..src.client.auth import DomoAuth
    # return DomoAuth(domo_instance=instance, session_token=token)

    # For now, return a mock
    mock_auth = MagicMock()
    mock_auth.domo_instance = instance
    mock_auth.session_token = token
    return mock_auth
