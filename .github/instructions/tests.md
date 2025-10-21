---
applies-to: tests/test_harness.py
title: Domo Library Route Testing Harness
---
# Route Testing Harness Guide

## Overview

This testing framework provides comprehensive tools for testing Domo Library route functions with:
- **Mock responses** for isolated unit testing
- **Error scenario testing** for robust error handling validation
- **Performance testing** for optimization
- **Integration testing** for real API validation
- **Async support** for modern Python patterns

## Quick Start

### Basic Route Test

```python
import pytest
from tests.test_harness import RouteTestHarness, RouteTestBuilder

@pytest.mark.asyncio
async def test_my_route():
    # Create test harness
    harness = RouteTestHarness()
    
    # Build test scenarios
    builder = RouteTestBuilder(harness)
    builder.add_success_scenario(
        "valid_request",
        "Test successful route call",
        res={"id": "123", "name": "Test Entity"}
    )
    
    scenarios = builder.build()
    
    # Your route function (example)
    async def my_route_function(auth, entity_id):
        return harness.create_response_get_data(
            status=200,
            res={"id": entity_id, "status": "success"}
        )
    
    # Run tests
    results = harness.run_test_scenarios(
        my_route_function, 
        scenarios,
        entity_id="123"
    )
    
    assert results["passed"] > 0
```

### Standard Test Patterns

Use the convenience function for common CRUD operations:

```python
from tests.test_harness import create_standard_route_tests

def test_user_route_standard():
    harness = RouteTestHarness()
    
    # Automatically creates success, error, not found, auth error scenarios
    scenarios = create_standard_route_tests(
        harness,
        entity_name="user",
        sample_data={"id": "user-123", "name": "John Doe"}
    )
    
    # Test your route function
    results = harness.run_test_scenarios(get_user_by_id, scenarios)
    assert results["failed"] == 0
```

## Test Scenario Types

### 1. Success Scenarios

```python
builder.add_success_scenario(
    "get_entity_success",
    "Successfully retrieve entity",
    res={"id": "123", "name": "Test"},
    status_code=200,
    entity_id="123"  # Function parameters
)
```

### 2. Error Scenarios

```python
# Generic error
builder.add_error_scenario(
    "server_error",
    "Internal server error",
    status_code=500,
    error_response={"error": "Internal error"},
    expected_exception=RouteError
)

# Authentication error
builder.add_auth_error_scenario(
    "unauthorized",
    "Invalid or expired token",
    status_code=401
)

# Not found error
builder.add_not_found_scenario(
    "entity_not_found",
    "Entity does not exist",
    entity_id="nonexistent-id"
)
```

### 3. Custom Scenarios

```python
scenario = TestScenario(
    name="custom_test",
    description="Custom test scenario",
    mock_response=MockResponse(
        status_code=202,
        json_data={"message": "Accepted"},
        headers={"Location": "/status/123"}
    ),
    expected_success=True,
    function_kwargs={"custom_param": "value"}
)
```

## Error Testing Patterns

### Test Exception Handling

```python
async def test_route_error_handling():
    harness = RouteTestHarness()
    
    # Test that route raises correct exception
    scenario = TestScenario(
        name="auth_error",
        description="Should raise AuthError for 401",
        mock_response=MockResponse(
            status_code=401,
            json_data={"error": "Unauthorized"},
            is_success=False
        ),
        expected_success=False,
        expected_exception=AuthError  # Verify correct exception type
    )
    
    results = harness.run_test_scenarios(my_route, [scenario])
    assert results["passed"] == 1
```

### Test Error Messages

```python
from src.client.exceptions import RouteError

async def test_error_message_context():
    harness = RouteTestHarness()
    
    try:
        # Simulate route that should fail
        error = RouteError.for_entity(
            "dataset-123",
            "Dataset {entity_id} not found",
            "dataset"
        )
        raise error
    except RouteError as e:
        assert "dataset-123" in str(e)
        assert "not found" in str(e)
```

## Performance Testing

```python
from tests.test_harness import PerformanceTestHarness

@pytest.mark.performance
async def test_route_performance():
    # Measure route execution time
    performance = await PerformanceTestHarness.measure_route_performance(
        route_function=my_fast_route,
        iterations=100,
        auth=harness.default_auth,
        entity_id="test-123"
    )
    
    # Assert performance requirements
    assert performance["avg_time"] < 0.1  # Under 100ms average
    assert performance["errors"] == 0     # No failures
    assert performance["max_time"] < 0.5  # No request over 500ms
```

## Integration Testing

For testing against real APIs (use sparingly):

```python
@pytest.mark.integration
async def test_real_api_integration():
    from tests.test_harness import IntegrationTestHarness
    
    # Requires real auth credentials
    real_auth = get_real_auth_from_env()
    integration = IntegrationTestHarness(real_auth)
    
    result = await integration.test_route_integration(
        route_function=get_user_by_id,
        test_params={"user_id": "real-user-id"},
        expected_status_range=(200, 299)
    )
    
    assert result["success"] is True
```

## Mock Responses

### JSON Responses

```python
MockResponse(
    status_code=200,
    json_data={
        "users": [
            {"id": "1", "name": "User 1"},
            {"id": "2", "name": "User 2"}
        ],
        "total": 2
    }
)
```

### Text Responses

```python
MockResponse(
    status_code=200,
    text_data="Plain text response",
    headers={"Content-Type": "text/plain"}
)
```

### Error Responses

```python
MockResponse(
    status_code=404,
    json_data={"error": "Not Found", "message": "Entity does not exist"},
    is_success=False
)
```

## Authentication Testing

### Different Auth Types

```python
# Full auth (session token)
full_auth = harness._create_mock_auth(auth_type="full")

# Developer auth (client credentials)
dev_auth = harness._create_mock_auth(
    auth_type="developer",
    domo_instance="my-instance"
)

# Custom auth configuration
custom_auth = harness._create_mock_auth(
    domo_instance="custom-instance",
    custom_field="custom_value"
)
```

### Auth Error Scenarios

```python
# Test various auth failures
auth_scenarios = [
    TestScenario(
        name="invalid_token",
        description="Invalid session token",
        mock_response=MockResponse(401, {"error": "Invalid token"}),
        expected_exception=InvalidCredentialsError
    ),
    TestScenario(
        name="expired_token", 
        description="Expired session token",
        mock_response=MockResponse(401, {"error": "Token expired"}),
        expected_exception=InvalidCredentialsError
    ),
    TestScenario(
        name="insufficient_permissions",
        description="Valid token but no permission", 
        mock_response=MockResponse(403, {"error": "Forbidden"}),
        expected_exception=AuthError
    )
]
```

## Best Practices

### 1. Test Structure

```python
class TestEntityRoutes:
    """Group related route tests together."""
    
    @pytest.fixture
    def entity_data(self):
        return {"id": "123", "name": "Test Entity"}
    
    @pytest.mark.asyncio
    async def test_get_entity(self, entity_data):
        # Test implementation
        pass
    
    @pytest.mark.asyncio  
    async def test_create_entity(self, entity_data):
        # Test implementation
        pass
```

### 2. Parameterized Tests

```python
@pytest.mark.parametrize("status_code,expected_exception", [
    (400, RouteError),
    (401, AuthError), 
    (403, AuthError),
    (404, RouteError),
    (500, RouteError)
])
async def test_error_status_codes(status_code, expected_exception):
    # Test different error status codes
    pass
```

### 3. Fixture Reuse

```python
@pytest.fixture
def common_scenarios(harness):
    """Reusable scenarios across multiple tests."""
    return create_standard_route_tests(harness, "entity")

def test_route_a(common_scenarios):
    # Use shared scenarios
    pass
    
def test_route_b(common_scenarios):
    # Reuse same scenarios for different route
    pass
```

### 4. Error Message Testing

```python
async def test_error_messages_are_helpful():
    """Ensure error messages provide useful debugging information."""
    
    error = RouteError.for_entity(
        "user-123", 
        "User {entity_id} not found in instance {domo_instance}",
        domo_instance="test-instance"
    )
    
    error_str = str(error)
    assert "user-123" in error_str
    assert "test-instance" in error_str
    assert "not found" in error_str
```

## Running Tests

### Command Line Examples

```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_user_routes.py

# Run integration tests (requires credentials)
pytest -m integration --run-integration

# Run performance tests
pytest -m performance --run-performance

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run tests in parallel
pytest -n auto
```

### Environment Variables

```bash
# For integration tests
export DOMO_INSTANCE="your-instance"
export DOMO_TOKEN="your-token"

# Test configuration
export TESTING=true
export PYTEST_CURRENT_TEST=true
```

## Advanced Usage

### Custom Mock Responses

```python
class CustomMockResponse:
    """Custom response handler for complex scenarios."""
    
    def __init__(self, scenario_data):
        self.scenario_data = scenario_data
    
    async def handle_request(self, **kwargs):
        # Custom logic based on request parameters
        if kwargs.get("entity_id") == "special":
            return special_response()
        return standard_response()
```

### Test Data Factories

```python
def create_user_list(count=5):
    """Generate test user data."""
    return [
        {
            "id": f"user-{i}",
            "name": f"User {i}", 
            "email": f"user{i}@example.com"
        }
        for i in range(count)
    ]

def create_dataset_schema():
    """Generate test dataset schema."""
    return {
        "columns": [
            {"name": "id", "type": "STRING"},
            {"name": "value", "type": "DOUBLE"},
            {"name": "date", "type": "DATE"}
        ]
    }
```

This testing harness provides comprehensive coverage for route function testing while maintaining simplicity and flexibility for various testing scenarios.