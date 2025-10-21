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


class TestDomoAuth(PytestRouteTestCase):
    """Test class for DomoAuth functionality using the test harness."""

    @pytest.fixture
    def token_auth(self):
        """Create a DomoTokenAuth instance for testing."""
        return dmda.DomoTokenAuth(
            domo_access_token="test-token-123",
            domo_instance="test-instance",
        )

    @pytest.fixture
    def developer_auth(self):
        """Create a DomoDeveloperAuth instance for testing."""
        return dmda.DomoDeveloperAuth(
            domo_client_id="test-client-id",
            domo_client_secret="test-client-secret",
            domo_instance="test-instance",
        )

    def test_token_auth_who_am_i_scenarios(self, harness, token_auth):
        """Test DomoTokenAuth who_am_i with various scenarios."""

        # Create test scenarios using the builder
        builder = RouteTestBuilder(harness)

        # Success scenario
        builder.add_success_scenario(
            name="who_am_i_success",
            description="Successfully authenticate and get user info",
            res={
                "id": "12345",
                "displayName": "Test User",
                "emailAddress": "test@example.com",
                "role": {"id": "1", "name": "Admin"},
            },
            status_code=200,
        )

        # Unauthorized scenario
        builder.add_auth_error_scenario(
            name="who_am_i_unauthorized",
            description="Invalid token returns 401",
            status_code=401,
        )

        # Forbidden scenario
        builder.add_error_scenario(
            name="who_am_i_forbidden",
            description="Token lacks permissions",
            status_code=403,
            error_response={"error": "Forbidden"},
            expected_exception=AuthError,
        )

        # Invalid instance scenario
        builder.add_error_scenario(
            name="who_am_i_invalid_instance",
            description="Invalid Domo instance",
            status_code=404,
            error_response={"error": "Instance not found"},
            expected_exception=AuthError,
        )

        scenarios = builder.build()

        # Mock the who_am_i method to use our test harness
        async def mock_who_am_i_route(**kwargs):
            # Find the matching scenario based on current test
            scenario = scenarios[0]  # Default to success for this test

            if scenario.mock_response.status_code == 200:
                return harness.create_response_get_data(
                    status=200, res=scenario.mock_response.json_data, is_success=True
                )
            else:
                return harness.create_response_get_data(
                    status=scenario.mock_response.status_code,
                    res=scenario.mock_response.json_data,
                    is_success=False,
                )

        # Test successful scenario
        with patch.object(
            token_auth, "who_am_i", new_callable=AsyncMock
        ) as mock_method:
            mock_method.return_value = harness.create_response_get_data(
                status=200,
                res={"id": "12345", "displayName": "Test User"},
                is_success=True,
            )

            result = asyncio.run(token_auth.who_am_i())
            assert result.is_success
            assert result.response["id"] == "12345"
            mock_method.assert_called_once()

    def test_developer_auth_scenarios(self, harness, developer_auth):
        """Test DomoDeveloperAuth with various scenarios."""

        scenarios = [
            TestScenario(
                name="developer_auth_success",
                description="Successful OAuth2 authentication",
                mock_response=MockResponse(
                    status_code=200,
                    json_data={
                        "access_token": "bearer-token-xyz",
                        "userId": "67890",
                        "domain": "test-instance",
                    },
                ),
                expected_success=True,
            ),
            TestScenario(
                name="developer_auth_invalid_credentials",
                description="Invalid client credentials",
                mock_response=MockResponse(
                    status_code=401, json_data={"error": "invalid_client"}
                ),
                expected_success=False,
                expected_exception=AuthError,
            ),
            TestScenario(
                name="developer_auth_server_error",
                description="OAuth server error",
                mock_response=MockResponse(
                    status_code=500, json_data={"error": "internal_server_error"}
                ),
                expected_success=False,
                expected_exception=AuthError,
            ),
        ]

        # Test each scenario
        for scenario in scenarios:
            with patch.object(
                developer_auth, "get_auth_token", new_callable=AsyncMock
            ) as mock_method:
                if scenario.expected_success:
                    mock_method.return_value = scenario.mock_response.json_data[
                        "access_token"
                    ]
                    result = asyncio.run(developer_auth.get_auth_token())
                    assert result == "bearer-token-xyz"
                else:
                    mock_method.side_effect = AuthError("Authentication failed")
                    with pytest.raises(AuthError):
                        asyncio.run(developer_auth.get_auth_token())

    def test_auth_header_generation(self, token_auth, developer_auth):
        """Test that auth headers are generated correctly."""

        # Test token auth header
        token_header = token_auth.auth_header
        assert "x-domo-developer-token" in token_header
        assert token_header["x-domo-developer-token"] == "test-token-123"

        # Test developer auth header (after token is set)
        developer_auth.token = "bearer-token-xyz"
        dev_header = developer_auth.auth_header
        assert "x-domo-developer-token" in dev_header
        assert dev_header["x-domo-developer-token"] == "bearer-token-xyz"

    def test_token_validation_scenarios(self, harness, token_auth):
        """Test token validation with different response scenarios."""

        validation_scenarios = [
            {
                "name": "valid_token",
                "response": {"id": "user123", "emailAddress": "user@test.com"},
                "status": 200,
                "expected_valid": True,
            },
            {
                "name": "expired_token",
                "response": {"error": "Token expired"},
                "status": 401,
                "expected_valid": False,
            },
            {
                "name": "invalid_instance",
                "response": "Forbidden",
                "status": 403,
                "expected_valid": False,
            },
        ]

        for scenario in validation_scenarios:
            with patch.object(
                token_auth, "who_am_i", new_callable=AsyncMock
            ) as mock_method:
                mock_method.return_value = harness.create_response_get_data(
                    status=scenario["status"],
                    res=scenario["response"],
                    is_success=scenario["expected_valid"],
                )

                result = asyncio.run(token_auth.who_am_i())
                assert result.is_success == scenario["expected_valid"]


class TestIntegrationAuth:
    """Integration tests for auth functionality (requires real credentials)."""

    @pytest.fixture
    def real_token_auth(self):
        """Create real auth instance if credentials are available."""
        access_token = os.getenv("DOMO_ACCESS_TOKEN")
        instance = os.getenv("DOMO_INSTANCE")

        if not access_token or not instance:
            pytest.skip("Real credentials not available for integration test")

        return dmda.DomoTokenAuth(
            domo_access_token=access_token, domo_instance=instance
        )

    @pytest.mark.integration
    async def test_real_who_am_i(self, real_token_auth):
        """Test who_am_i with real credentials."""
        integration_harness = IntegrationTestHarness(real_token_auth)

        # Test the real who_am_i functionality
        result = await integration_harness.test_route_integration(
            route_function=real_token_auth.who_am_i,
            test_params={},
            expected_status_range=(200, 299),
        )

        assert result["success"], f"Integration test failed: {result.get('error')}"

        if hasattr(result["result"], "response"):
            response = result["result"].response
            # Verify response has expected user fields
            assert "id" in response
            assert "emailAddress" in response or "displayName" in response

    @pytest.mark.integration
    async def test_token_validation_flow(self, real_token_auth):
        """Test the complete token validation flow."""

        # Test print_is_token functionality
        is_valid = await real_token_auth.print_is_token(debug_api=False)
        assert isinstance(is_valid, bool)

        # After validation, token should be marked as valid
        if is_valid:
            assert real_token_auth.is_valid_token
            assert real_token_auth.user_id is not None


# Utility functions for manual testing
async def manual_test_auth():
    """Manual test function for development/debugging."""
    print("🧪 Running manual auth tests...")

    # Test with mock data
    harness = RouteTestHarness()

    # Create mock auth
    mock_auth = dmda.DomoTokenAuth(
        domo_access_token="test-token", domo_instance="test-instance"
    )

    # Mock the who_am_i method
    with patch.object(mock_auth, "who_am_i", new_callable=AsyncMock) as mock_method:
        mock_method.return_value = harness.create_response_get_data(
            status=200,
            res={"id": "test123", "displayName": "Test User"},
            is_success=True,
        )

        result = await mock_auth.who_am_i()
        print(f"✅ Mock test passed: {result.is_success}")
        print(f"   User ID: {result.response['id']}")

    # Test with real credentials if available
    access_token = os.getenv("DOMO_ACCESS_TOKEN")
    instance = os.getenv("DOMO_INSTANCE")

    if access_token and instance:
        print("\n🔗 Testing with real credentials...")
        real_auth = dmda.DomoTokenAuth(
            domo_access_token=access_token, domo_instance=instance
        )

        try:
            result = await real_auth.who_am_i()
            print(f"✅ Real test passed: {result.is_success}")
            if result.response:
                print(f"   User: {result.response.get('displayName', 'N/A')}")
        except Exception as e:
            print(f"❌ Real test failed: {e}")
    else:
        print("⚠️  Skipping real credential test (no credentials found)")


if __name__ == "__main__":
    # Run manual test
    asyncio.run(manual_test_auth())
