"""
Comprehensive testing harness for Domo Library route functions.

This module provides utilities for testing route functions with mock responses,
authentication, and various error scenarios.
"""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from domolibrary2.client.auth import DomoAuth
from domolibrary2.base.exceptions import AuthError, RouteError
from domolibrary2.client.response import RequestMetadata, ResponseGetData


@dataclass
class MockResponse:
    """Mock response for testing route functions."""

    status_code: int
    json_data: Optional[dict[str, Any]] = None
    text_data: Optional[str] = None
    headers: dict[str, str] = field(
        default_factory=lambda: {"Content-Type": "application/json"}
    )
    is_success: bool = True

    def json(self):
        """Mock JSON response."""
        if self.json_data is not None:
            return self.json_data
        raise ValueError("No JSON data available")

    @property
    def text(self):
        """Mock text response."""
        return self.text_data or json.dumps(self.json_data) if self.json_data else ""

    @property
    def ok(self):
        """Check if response is successful."""
        return 200 <= self.status_code < 400


@dataclass
class TestScenario:
    """Test scenario configuration for route testing."""

    name: str
    description: str
    mock_response: MockResponse
    expected_success: bool = True
    expected_exception: Optional[type[Exception]] = None
    auth_config: Optional[dict[str, Any]] = None
    function_kwargs: dict[str, Any] = field(default_factory=dict)


class RouteTestHarness:
    """
    Comprehensive testing harness for route functions.

    Provides utilities for:
    - Mocking HTTP responses
    - Testing various authentication scenarios
    - Validating error handling
    - Performance testing
    - Integration testing
    """

    def __init__(self, base_instance: str = "test-instance"):
        self.base_instance = base_instance
        self.default_auth = self._create_mock_auth()

    def _create_mock_auth(self, auth_type: str = "full", **kwargs) -> DomoAuth:
        """Create a mock authentication object."""
        mock_auth = MagicMock(spec=DomoAuth)
        mock_auth.domo_instance = kwargs.get("domo_instance", self.base_instance)
        mock_auth.auth_header = {"Authorization": "Bearer test-token"}

        if auth_type == "developer":
            mock_auth.client_id = "test-client-id"
            mock_auth.client_secret = "test-client-secret"
        elif auth_type == "full":
            mock_auth.session_token = "test-session-token"
            mock_auth.user_id = "test-user-id"

        return mock_auth

    def create_response_get_data(
        self,
        status: int = 200,
        res: Any = None,
        is_success: bool = True,
        url: str = None,
        auth: DomoAuth = None,
    ) -> ResponseGetData:
        """Create a ResponseGetData object for testing."""

        if res is None:
            res = {"success": True, "data": []}

        # Create request metadata
        request_metadata = RequestMetadata(
            url=url or f"https://{self.base_instance}.domo.com/api/test",
            headers={"Authorization": "Bearer test-token"},
            body=None,
            params=None,
        )

        return ResponseGetData(
            status=status,
            response=res,
            is_success=is_success,
            request_metadata=request_metadata,
        )

    async def mock_get_data(
        self, mock_response: MockResponse, **kwargs
    ) -> ResponseGetData:
        """Mock the get_data function with specified response."""

        return self.create_response_get_data(
            status=mock_response.status_code,
            res=mock_response.json_data or mock_response.text_data,
            is_success=mock_response.is_success,
            url=kwargs.get("url"),
            auth=kwargs.get("auth"),
        )

    def run_test_scenarios(
        self, route_function: Callable, scenarios: list[TestScenario], **default_kwargs
    ) -> dict[str, Any]:
        """
        Run multiple test scenarios against a route function.

        Args:
            route_function: The route function to test
            scenarios: list of test scenarios to run
            **default_kwargs: Default arguments for the route function

        Returns:
            Dictionary with test results
        """
        results = {"passed": 0, "failed": 0, "errors": [], "scenario_results": {}}

        for scenario in scenarios:
            try:
                result = asyncio.run(
                    self._run_single_scenario(
                        route_function, scenario, **default_kwargs
                    )
                )
                results["scenario_results"][scenario.name] = result

                if result["passed"]:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        {"scenario": scenario.name, "error": result.get("error")}
                    )

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "scenario": scenario.name,
                        "error": f"Test execution error: {str(e)}",
                    }
                )

        return results

    async def _run_single_scenario(
        self, route_function: Callable, scenario: TestScenario, **default_kwargs
    ) -> dict[str, Any]:
        """Run a single test scenario."""

        # Prepare function arguments
        kwargs = {**default_kwargs, **scenario.function_kwargs}
        if "auth" not in kwargs:
            auth_config = scenario.auth_config or {}
            kwargs["auth"] = self._create_mock_auth(**auth_config)

        # Mock the get_data function
        with patch(
            "domolibrary2.client.get_data.get_data", new_callable=AsyncMock
        ) as mock_get_data:
            mock_get_data.return_value = await self.mock_get_data(
                scenario.mock_response
            )

            try:
                # Execute the route function
                result = await route_function(**kwargs)

                # Check if we expected success
                if scenario.expected_success:
                    return {
                        "passed": True,
                        "result": result,
                        "message": f"Scenario '{scenario.name}' passed as expected",
                    }
                else:
                    return {
                        "passed": False,
                        "error": f"Expected failure but function succeeded: {result}",
                    }

            except Exception as e:
                # Check if we expected an exception
                if scenario.expected_exception and isinstance(
                    e, scenario.expected_exception
                ):
                    return {
                        "passed": True,
                        "exception": str(e),
                        "message": f"Scenario '{scenario.name}' raised expected exception",
                    }
                elif not scenario.expected_success:
                    return {
                        "passed": True,
                        "exception": str(e),
                        "message": f"Scenario '{scenario.name}' failed as expected",
                    }
                else:
                    return {"passed": False, "error": f"Unexpected exception: {str(e)}"}


class RouteTestBuilder:
    """Builder class for creating comprehensive route tests."""

    def __init__(self, harness: RouteTestHarness):
        self.harness = harness
        self.scenarios: list[TestScenario] = []

    def add_success_scenario(
        self,
        name: str,
        description: str,
        res: Any = None,
        status_code: int = 200,
        **kwargs,
    ) -> "RouteTestBuilder":
        """Add a successful response scenario."""

        mock_response = MockResponse(
            status_code=status_code,
            json_data=res or {"success": True},
            is_success=True,
        )

        scenario = TestScenario(
            name=name,
            description=description,
            mock_response=mock_response,
            expected_success=True,
            function_kwargs=kwargs,
        )

        self.scenarios.append(scenario)
        return self

    def add_error_scenario(
        self,
        name: str,
        description: str,
        status_code: int = 400,
        error_response: Any = None,
        expected_exception: type[Exception] = RouteError,
        **kwargs,
    ) -> "RouteTestBuilder":
        """Add an error response scenario."""

        mock_response = MockResponse(
            status_code=status_code,
            json_data=error_response or {"error": "Test error"},
            is_success=False,
        )

        scenario = TestScenario(
            name=name,
            description=description,
            mock_response=mock_response,
            expected_success=False,
            expected_exception=expected_exception,
            function_kwargs=kwargs,
        )

        self.scenarios.append(scenario)
        return self

    def add_auth_error_scenario(
        self, name: str, description: str, status_code: int = 401, **kwargs
    ) -> "RouteTestBuilder":
        """Add an authentication error scenario."""

        return self.add_error_scenario(
            name=name,
            description=description,
            status_code=status_code,
            error_response={"error": "Unauthorized"},
            expected_exception=AuthError,
            **kwargs,
        )

    def add_not_found_scenario(
        self, name: str, description: str, entity_id: str = "nonexistent", **kwargs
    ) -> "RouteTestBuilder":
        """Add a not found error scenario."""

        return self.add_error_scenario(
            name=name,
            description=description,
            status_code=404,
            error_response={"error": "Not Found"},
            expected_exception=RouteError,
            **{**kwargs, "entity_id": entity_id},
        )

    def build(self) -> list[TestScenario]:
        """Build and return the test scenarios."""
        return self.scenarios


# Convenience functions for common test patterns


def create_standard_route_tests(
    harness: RouteTestHarness,
    entity_name: str = "entity",
    sample_data: dict[str, Any] = None,
) -> list[TestScenario]:
    """Create standard test scenarios for most route functions."""

    if sample_data is None:
        sample_data = {"id": "test-123", "name": "Test Entity"}

    builder = RouteTestBuilder(harness)

    # Success scenarios
    builder.add_success_scenario(
        f"get_{entity_name}_success",
        f"Successfully retrieve {entity_name}",
        res=sample_data,
    )

    builder.add_success_scenario(
        f"get_{entity_name}_empty_list",
        f"Successfully retrieve empty {entity_name} list",
        res=[],
    )

    # Error scenarios
    builder.add_not_found_scenario(
        f"get_{entity_name}_not_found", f"{entity_name.title()} not found"
    )

    builder.add_auth_error_scenario(
        f"get_{entity_name}_unauthorized", f"Unauthorized access to {entity_name}"
    )

    builder.add_error_scenario(
        f"get_{entity_name}_server_error",
        f"Server error when retrieving {entity_name}",
        status_code=500,
        error_response={"error": "Internal Server Error"},
    )

    builder.add_error_scenario(
        f"get_{entity_name}_forbidden",
        f"Forbidden access to {entity_name}",
        status_code=403,
        error_response={"error": "Forbidden"},
    )

    return builder.build()


# Pytest integration utilities


class PytestRouteTestCase:
    """Base class for pytest-based route testing."""

    @pytest.fixture
    def harness(self):
        """Provide a test harness instance."""
        return RouteTestHarness()

    @pytest.fixture
    def mock_auth(self, harness):
        """Provide a mock authentication object."""
        return harness.default_auth

    def run_route_test_scenarios(
        self, route_function: Callable, scenarios: list[TestScenario], **kwargs
    ):
        """Run test scenarios and assert results."""
        harness = RouteTestHarness()
        results = harness.run_test_scenarios(route_function, scenarios, **kwargs)

        # Assert all tests passed
        assert results["failed"] == 0, f"Failed scenarios: {results['errors']}"
        assert results["passed"] > 0, "No tests were executed"

        return results


# Performance testing utilities


class PerformanceTestHarness:
    """Performance testing utilities for route functions."""

    @staticmethod
    async def measure_route_performance(
        route_function: Callable, iterations: int = 100, **kwargs
    ) -> dict[str, Any]:
        """Measure route function performance."""
        import time

        times = []
        errors = 0

        for _ in range(iterations):
            start_time = time.time()
            try:
                await route_function(**kwargs)
                end_time = time.time()
                times.append(end_time - start_time)
            except Exception:
                errors += 1

        if times:
            return {
                "iterations": iterations,
                "errors": errors,
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
                "total_time": sum(times),
            }
        else:
            return {
                "iterations": iterations,
                "errors": errors,
                "message": "All iterations failed",
            }


# Integration testing utilities


class IntegrationTestHarness:
    """Integration testing utilities that use real network calls."""

    def __init__(self, real_auth: DomoAuth):
        self.auth = real_auth

    async def test_route_integration(
        self,
        route_function: Callable,
        test_params: dict[str, Any],
        expected_status_range: tuple = (200, 299),
    ) -> dict[str, Any]:
        """Test route function with real API calls."""

        try:
            result = await route_function(auth=self.auth, **test_params)

            # Check if result is successful
            if hasattr(result, "status"):
                success = (
                    expected_status_range[0]
                    <= result.status
                    <= expected_status_range[1]
                )
            else:
                success = True  # Assume success if no status

            return {
                "success": success,
                "result": result,
                "status": getattr(result, "status", None),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "exception_type": type(e).__name__,
            }
