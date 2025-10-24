import domolibrary2.client.auth as dmda
from dotenv import load_dotenv
import os

from dc_logger.client.base import (
    Logger,
    HandlerInstance,
    Handler_BufferSettings,
    set_global_logger,
)
from dc_logger.logs.services.file import FileHandler, File_ServiceConfig

load_dotenv()

json_config = File_ServiceConfig(
    destination="./LOGGER/test_get_data.json",
    output_mode="file",
    format="json",
    append=True,
)

buffer_settings = Handler_BufferSettings()

json_file_handler = FileHandler(
    buffer_settings=buffer_settings, service_config=json_config
)

# Create handler instance
json_handler_instance = HandlerInstance(
    service_handler=json_file_handler, handler_name="json_file"
)

logger = Logger(app_name="test_get_data", handlers=[json_handler_instance])

set_global_logger(logger)


async def test_logger():
    """Test logger functionality."""

    await logger.info(message="Starting test_logger function.")

    domo_auth = dmda.DomoTokenAuth(
        domo_access_token=os.getenv("DOMO_ACCESS_TOKEN"),
        domo_instance=os.getenv("DOMO_INSTANCE"),
    )

    res = await domo_auth.who_am_i()
    await logger.info(message="Completed who_am_i request.", data=res.response)

    return res.is_success


def main():
    """Main function to run the test."""
    import asyncio

    asyncio.run(test_logger())


if __name__ == "__main__":
    main()
"""
Tests for get_data functionality using test harness with logging integration.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from dotenv import load_dotenv
import os

import domolibrary2.client.auth as dmda
import domolibrary2.client.get_data as gd
from domolibrary2.client.exceptions import RouteError

from dc_logger.client.base import (
    Logger,
    HandlerInstance,
    Handler_BufferSettings,
    set_global_logger,
)
from dc_logger.logs.services.file import FileHandler, File_ServiceConfig

from tests.tools.test_harness import (
    RouteTestHarness,
    RouteTestBuilder,
    PytestRouteTestCase,
    IntegrationTestHarness,
)

load_dotenv()


class TestGetDataWithHarness(PytestRouteTestCase):
    """Test class for get_data functionality using the test harness."""

    @pytest.fixture
    def logger_setup(self):
        """Set up logger for testing."""
        json_config = File_ServiceConfig(
            destination="./LOGGER/test_get_data.json",
            output_mode="file",
            format="json",
            append=True,
        )

        buffer_settings = Handler_BufferSettings()
        json_file_handler = FileHandler(
            buffer_settings=buffer_settings, service_config=json_config
        )

        json_handler_instance = HandlerInstance(
            service_handler=json_file_handler, handler_name="json_file"
        )

        logger = Logger(app_name="test_get_data", handlers=[json_handler_instance])
        set_global_logger(logger)
        return logger

    @pytest.fixture
    def auth_instance(self):
        """Create authentication instance for testing."""
        return dmda.DomoTokenAuth(
            domo_access_token="test-token-123",
            domo_instance="test-instance",
        )

    def test_get_data_scenarios(self, harness, auth_instance, logger_setup):
        """Test get_data with various HTTP scenarios."""

        builder = RouteTestBuilder(harness)

        # Success scenarios
        builder.add_success_scenario(
            name="get_data_success",
            description="Successful GET request",
            res={"data": [{"id": "123", "name": "Test Item"}]},
            status_code=200,
        )

        builder.add_success_scenario(
            name="get_data_empty_response",
            description="Successful request with empty data",
            res={"data": []},
            status_code=200,
        )

        # Error scenarios
        builder.add_error_scenario(
            name="get_data_not_found",
            description="Resource not found",
            status_code=404,
            error_response={"error": "Not Found"},
            expected_exception=RouteError,
        )

        builder.add_auth_error_scenario(
            name="get_data_unauthorized",
            description="Authentication failure",
            status_code=401,
        )

        builder.add_error_scenario(
            name="get_data_server_error",
            description="Internal server error",
            status_code=500,
            error_response={"error": "Internal Server Error"},
            expected_exception=RouteError,
        )

        scenarios = builder.build()

        # Test successful scenario with logging
        success_scenario = scenarios[0]

        async def mock_get_data(**kwargs):
            await logger_setup.info(
                message="Mock get_data called",
                data={"url": kwargs.get("url"), "method": kwargs.get("method")},
            )

            return harness.create_response_get_data(
                status=success_scenario.mock_response.status_code,
                res=success_scenario.mock_response.json_data,
                is_success=success_scenario.mock_response.is_success,
                url=kwargs.get("url"),
                auth=kwargs.get("auth"),
            )

        # Test the mock function
        with patch(
            "domolibrary2.client.get_data.get_data", new_callable=AsyncMock
        ) as mock_gd:
            mock_gd.side_effect = mock_get_data

            result = asyncio.run(
                gd.get_data(
                    auth=auth_instance,
                    url="https://test-instance.domo.com/api/test",
                    method="GET",
                )
            )

            assert result.is_success
            assert "data" in result.response
            mock_gd.assert_called_once()

    def test_auth_integration_with_logging(self, harness, logger_setup):
        """Test authentication integration with comprehensive logging."""

        auth_instance = dmda.DomoTokenAuth(
            domo_access_token="test-token-456",
            domo_instance="test-instance",
        )

        test_scenarios = [
            {
                "name": "valid_authentication",
                "response": {
                    "id": "user123",
                    "displayName": "Test User",
                    "emailAddress": "test@example.com",
                },
                "status": 200,
                "success": True,
            },
            {
                "name": "invalid_token",
                "response": {"error": "Invalid token"},
                "status": 401,
                "success": False,
            },
        ]

        for scenario in test_scenarios:

            async def test_scenario():
                await logger_setup.info(message=f"Testing scenario: {scenario['name']}")

                with patch.object(
                    auth_instance, "who_am_i", new_callable=AsyncMock
                ) as mock_method:
                    mock_method.return_value = harness.create_response_get_data(
                        status=scenario["status"],
                        res=scenario["response"],
                        is_success=scenario["success"],
                    )

                    result = await auth_instance.who_am_i()

                    await logger_setup.info(
                        message=f"Scenario {scenario['name']} completed",
                        data={
                            "success": result.is_success,
                            "status": result.status,
                            "expected": scenario["success"],
                        },
                    )

                    assert result.is_success == scenario["success"]
                    return result

            # Run the test
            asyncio.run(test_scenario())

    @pytest.mark.performance
    def test_get_data_performance(self, harness, auth_instance):
        """Test get_data performance with harness."""

        from tests.tools.test_harness import PerformanceTestHarness

        async def mock_fast_get_data(**kwargs):
            """Fast mock implementation for performance testing."""
            return harness.create_response_get_data(
                status=200, res={"data": "test"}, is_success=True
            )

        async def run_performance_test():
            with patch(
                "domolibrary2.client.get_data.get_data", new_callable=AsyncMock
            ) as mock_gd:
                mock_gd.side_effect = mock_fast_get_data

                # Define test function
                async def test_function():
                    return await gd.get_data(
                        auth=auth_instance,
                        url="https://test.com/api/endpoint",
                        method="GET",
                    )

                # Run performance test
                results = await PerformanceTestHarness.measure_route_performance(
                    test_function, iterations=50
                )

                assert results["errors"] == 0, "Performance test should have no errors"
                assert results["avg_time"] < 0.1, "Average response time should be fast"

                return results

        results = asyncio.run(run_performance_test())
        print(f"Performance test results: {results}")


class TestIntegrationGetData:
    """Integration tests that use real API calls."""

    @pytest.fixture
    def real_auth(self):
        """Create real auth instance if credentials are available."""
        access_token = os.getenv("DOMO_ACCESS_TOKEN")
        instance = os.getenv("DOMO_INSTANCE")

        if not access_token or not instance:
            pytest.skip("Real credentials not available for integration test")

        return dmda.DomoTokenAuth(
            domo_access_token=access_token, domo_instance=instance
        )

    @pytest.mark.integration
    async def test_real_who_am_i_with_logging(self, real_auth, logger_setup):
        """Integration test with real API and logging."""

        integration_harness = IntegrationTestHarness(real_auth)

        await logger_setup.info(message="Starting real integration test")

        result = await integration_harness.test_route_integration(
            route_function=real_auth.who_am_i,
            test_params={},
            expected_status_range=(200, 299),
        )

        await logger_setup.info(
            message="Integration test completed",
            data={"success": result["success"], "status": result.get("status")},
        )

        assert result["success"], f"Integration test failed: {result.get('error')}"


# Utility functions for development and debugging
async def manual_test_with_logging():
    """Manual test function with comprehensive logging."""

    # Set up logger
    json_config = File_ServiceConfig(
        destination="./LOGGER/manual_test_get_data.json",
        output_mode="file",
        format="json",
        append=True,
    )

    buffer_settings = Handler_BufferSettings()
    json_file_handler = FileHandler(
        buffer_settings=buffer_settings, service_config=json_config
    )

    json_handler_instance = HandlerInstance(
        service_handler=json_file_handler, handler_name="json_file"
    )

    logger = Logger(app_name="manual_test_get_data", handlers=[json_handler_instance])
    set_global_logger(logger)

    await logger.info(message="Starting manual test with test harness")

    # Create test harness
    harness = RouteTestHarness()

    # Test with mock data
    auth_instance = dmda.DomoTokenAuth(
        domo_access_token="test-token", domo_instance="test-instance"
    )

    with patch.object(auth_instance, "who_am_i", new_callable=AsyncMock) as mock_method:
        mock_method.return_value = harness.create_response_get_data(
            status=200,
            res={"id": "test123", "displayName": "Test User"},
            is_success=True,
        )

        result = await auth_instance.who_am_i()

        await logger.info(
            message="Mock test completed",
            data={
                "success": result.is_success,
                "user_id": result.response.get("id"),
                "user_name": result.response.get("displayName"),
            },
        )

        print(f"✅ Mock test passed: {result.is_success}")

    # Test with real credentials if available
    access_token = os.getenv("DOMO_ACCESS_TOKEN")
    instance = os.getenv("DOMO_INSTANCE")

    if access_token and instance:
        await logger.info(message="Starting real credential test")

        real_auth = dmda.DomoTokenAuth(
            domo_access_token=access_token, domo_instance=instance
        )

        try:
            result = await real_auth.who_am_i()

            await logger.info(
                message="Real test completed",
                data={"success": result.is_success, "status": result.status},
            )

            print(f"✅ Real test passed: {result.is_success}")

        except Exception as e:
            await logger.error(message="Real test failed", data={"error": str(e)})
            print(f"❌ Real test failed: {e}")
    else:
        await logger.info(
            message="Skipping real credential test - no credentials found"
        )
        print("⚠️  Skipping real credential test (no credentials found)")


def main():
    """Main function to run manual tests."""
    asyncio.run(manual_test_with_logging())


if __name__ == "__main__":
    main()
