"""
Example tests demonstrating the route testing harness.

This file shows practical examples of how to test route functions
using the comprehensive testing framework.
"""

import pytest
import asyncio
from typing import Any, Dict

from test_harness import (
    RouteTestHarness,
    RouteTestBuilder,
    TestScenario,
    MockResponse,
    create_standard_route_tests,
    PytestRouteTestCase,
)

# Import your actual route functions here
# from ..src.routes.auth import get_full_auth, who_am_i
# from ..src.routes.user import get_all_users, get_by_id
# from ..src.routes.dataset import get_dataset_by_id


class TestAuthRoutes(PytestRouteTestCase):
    """Example tests for authentication routes."""

    @pytest.mark.asyncio
    async def test_get_full_auth_scenarios(self, harness, mock_auth):
        """Test get_full_auth with various scenarios."""

        # Build test scenarios
        builder = RouteTestBuilder(harness)

        # Success scenario
        builder.add_success_scenario(
            "valid_credentials",
            "Valid username and password",
            res={
                "sessionToken": "test-session-token-123",
                "userId": "user-123",
                "success": True,
            },
        )

        # Invalid credentials
        builder.add_auth_error_scenario(
            "invalid_credentials", "Invalid username or password", status_code=401
        )

        # Account locked
        builder.add_error_scenario(
            "account_locked",
            "Account is locked",
            status_code=403,
            error_response={"reason": "ACCOUNT_LOCKED"},
        )

        # Invalid instance
        builder.add_error_scenario(
            "invalid_instance",
            "Invalid Domo instance",
            status_code=403,
            error_response="Forbidden",
        )

        scenarios = builder.build()

        # Mock route function for demonstration
        async def mock_get_full_auth(**kwargs):
            # This would be your actual route function
            return harness.create_response_get_data(
                status=200, res={"sessionToken": "test-token"}
            )

        # Run tests
        results = harness.run_test_scenarios(
            mock_get_full_auth,
            scenarios,
            domo_instance="test-instance",
            domo_username="test@example.com",
            domo_password="password123",
        )

        # Verify results
        assert results["passed"] > 0
        assert results["failed"] == 0

    @pytest.mark.asyncio
    async def test_who_am_i_scenarios(self, harness):
        """Test who_am_i endpoint with various scenarios."""

        scenarios = [
            TestScenario(
                name="valid_auth",
                description="Valid authentication token",
                mock_response=MockResponse(
                    status_code=200,
                    json_data={
                        "id": "user-123",
                        "emailAddress": "test@example.com",
                        "displayName": "Test User",
                    },
                ),
                expected_success=True,
            ),
            TestScenario(
                name="invalid_token",
                description="Invalid or expired token",
                mock_response=MockResponse(
                    status_code=401,
                    json_data={"error": "Unauthorized"},
                    is_success=False,
                ),
                expected_success=False,
            ),
            TestScenario(
                name="forbidden_instance",
                description="Forbidden instance access",
                mock_response=MockResponse(
                    status_code=403, json_data={"error": "Forbidden"}, is_success=False
                ),
                expected_success=False,
            ),
        ]

        # Mock route function
        async def mock_who_am_i(**kwargs):
            return harness.create_response_get_data(
                status=200, res={"id": "user-123", "displayName": "Test User"}
            )

        results = harness.run_test_scenarios(mock_who_am_i, scenarios)
        assert results["passed"] >= 1


class TestUserRoutes(PytestRouteTestCase):
    """Example tests for user routes."""

    @pytest.mark.asyncio
    async def test_get_all_users_standard_scenarios(self, harness):
        """Test get_all_users with standard scenarios."""

        # Use the convenience function for standard tests
        scenarios = create_standard_route_tests(
            harness,
            entity_name="users",
            sample_data=[
                {
                    "id": "user-1",
                    "displayName": "User 1",
                    "emailAddress": "user1@example.com",
                },
                {
                    "id": "user-2",
                    "displayName": "User 2",
                    "emailAddress": "user2@example.com",
                },
            ],
        )

        # Mock route function
        async def mock_get_all_users(**kwargs):
            return harness.create_response_get_data(
                status=200, res=[{"id": "user-1", "displayName": "User 1"}]
            )

        results = harness.run_test_scenarios(mock_get_all_users, scenarios)
        assert results["passed"] > 0

    @pytest.mark.asyncio
    async def test_get_user_by_id_custom_scenarios(self, harness):
        """Test get_user_by_id with custom scenarios."""

        builder = RouteTestBuilder(harness)

        # Valid user ID
        builder.add_success_scenario(
            "valid_user_id",
            "Retrieve user with valid ID",
            res={
                "id": "user-123",
                "displayName": "John Doe",
                "emailAddress": "john.doe@example.com",
                "role": {"id": 1, "name": "Admin"},
            },
            user_id="user-123",
        )

        # Non-existent user
        builder.add_not_found_scenario(
            "nonexistent_user", "User ID does not exist", entity_id="user-999"
        )

        # Invalid user ID format
        builder.add_error_scenario(
            "invalid_user_id_format",
            "Invalid user ID format",
            status_code=400,
            error_response={"error": "Invalid user ID format"},
            user_id="invalid-id-format",
        )

        scenarios = builder.build()

        # Mock route function
        async def mock_get_user_by_id(**kwargs):
            user_id = kwargs.get("user_id")
            if user_id == "user-123":
                return harness.create_response_get_data(
                    status=200, res={"id": user_id, "displayName": "John Doe"}
                )
            else:
                return harness.create_response_get_data(
                    status=404,
                    res={"error": "User not found"},
                    is_success=False,
                )

        results = harness.run_test_scenarios(mock_get_user_by_id, scenarios)
        assert results["passed"] > 0


class TestDatasetRoutes(PytestRouteTestCase):
    """Example tests for dataset routes."""

    @pytest.mark.asyncio
    async def test_get_dataset_by_id_comprehensive(self, harness):
        """Comprehensive test for dataset retrieval."""

        scenarios = [
            # Success cases
            TestScenario(
                name="valid_dataset",
                description="Retrieve existing dataset",
                mock_response=MockResponse(
                    status_code=200,
                    json_data={
                        "id": "dataset-123",
                        "name": "Sales Data",
                        "description": "Monthly sales figures",
                        "rows": 1000,
                        "columns": 15,
                        "schema": {
                            "columns": [
                                {"name": "date", "type": "DATE"},
                                {"name": "sales", "type": "DOUBLE"},
                            ]
                        },
                    },
                ),
                expected_success=True,
                function_kwargs={"dataset_id": "dataset-123"},
            ),
            # Permission denied
            TestScenario(
                name="no_permission",
                description="User lacks permission to view dataset",
                mock_response=MockResponse(
                    status_code=403,
                    json_data={"error": "Access denied"},
                    is_success=False,
                ),
                expected_success=False,
                function_kwargs={"dataset_id": "restricted-dataset"},
            ),
            # Dataset not found
            TestScenario(
                name="dataset_not_found",
                description="Dataset does not exist",
                mock_response=MockResponse(
                    status_code=404,
                    json_data={"error": "Dataset not found"},
                    is_success=False,
                ),
                expected_success=False,
                function_kwargs={"dataset_id": "nonexistent-dataset"},
            ),
            # Server error
            TestScenario(
                name="server_error",
                description="Internal server error",
                mock_response=MockResponse(
                    status_code=500,
                    json_data={"error": "Internal server error"},
                    is_success=False,
                ),
                expected_success=False,
                function_kwargs={"dataset_id": "any-dataset"},
            ),
        ]

        # Mock route function
        async def mock_get_dataset_by_id(**kwargs):
            dataset_id = kwargs.get("dataset_id")
            if dataset_id == "dataset-123":
                return harness.create_response_get_data(
                    status=200, res={"id": dataset_id, "name": "Sales Data"}
                )
            elif dataset_id == "restricted-dataset":
                return harness.create_response_get_data(
                    status=403,
                    res={"error": "Access denied"},
                    is_success=False,
                )
            else:
                return harness.create_response_get_data(
                    status=404,
                    res={"error": "Dataset not found"},
                    is_success=False,
                )

        results = harness.run_test_scenarios(mock_get_dataset_by_id, scenarios)
        assert results["passed"] > 0


class TestRoutePerformance:
    """Performance testing examples."""

    @pytest.mark.asyncio
    async def test_route_performance(self):
        """Test route function performance."""
        from test_harness import PerformanceTestHarness

        # Mock a simple route function
        async def mock_fast_route(**kwargs):
            await asyncio.sleep(0.001)  # Simulate 1ms response time
            return {"status": 200, "data": "success"}

        # Measure performance
        performance = await PerformanceTestHarness.measure_route_performance(
            mock_fast_route, iterations=50, auth=RouteTestHarness().default_auth
        )

        # Assert performance expectations
        assert performance["errors"] == 0
        assert performance["avg_time"] < 0.1  # Should be fast
        assert performance["iterations"] == 50


# Integration test examples (commented out as they require real credentials)
"""
class TestIntegrationRoutes:
    \"\"\"Integration tests with real API calls.\"\"\"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_auth_endpoint(self):
        \"\"\"Test against real Domo API (requires credentials).\"\"\"
        from test_harness import IntegrationTestHarness
        from ..src.client.auth import DomoAuth
        
        # This would require real credentials
        real_auth = DomoAuth(
            domo_instance="your-instance",
            session_token="your-token"
        )
        
        integration_harness = IntegrationTestHarness(real_auth)
        
        # Test real route function
        result = await integration_harness.test_route_integration(
            route_function=who_am_i,
            test_params={},
            expected_status_range=(200, 299)
        )
        
        assert result["success"] is True
"""


# Utility functions for test data generation


def generate_test_user_data(count: int = 5) -> list:
    """Generate test user data for scenarios."""
    return [
        {
            "id": f"user-{i}",
            "displayName": f"Test User {i}",
            "emailAddress": f"user{i}@example.com",
            "role": {"id": 1, "name": "Standard"},
        }
        for i in range(1, count + 1)
    ]


def generate_test_dataset_data(count: int = 3) -> list:
    """Generate test dataset data for scenarios."""
    return [
        {
            "id": f"dataset-{i}",
            "name": f"Test Dataset {i}",
            "description": f"Test dataset number {i}",
            "rows": 1000 * i,
            "columns": 10 + i,
        }
        for i in range(1, count + 1)
    ]


if __name__ == "__main__":
    """
    Example of running tests programmatically.
    For pytest, use: pytest test_examples.py -v
    """

    async def run_example_tests():
        harness = RouteTestHarness()

        # Example of running a single test
        scenarios = create_standard_route_tests(
            harness,
            entity_name="test_entity",
            sample_data={"id": "test-123", "name": "Test"},
        )

        async def mock_route(**kwargs):
            return harness.create_response_get_data(status=200, res={"success": True})

        results = harness.run_test_scenarios(mock_route, scenarios)
        print(f"Test results: {results['passed']} passed, {results['failed']} failed")

        if results["errors"]:
            print("Errors:")
            for error in results["errors"]:
                print(f"  - {error['scenario']}: {error['error']}")

    # Run example
    asyncio.run(run_example_tests())
