---
applies-to: tests/**/*
title: Domo Library Testing Standards
---
# Testing Standards

## Test Structure

### Test File Organization

```
tests/
├── classes/          # Class tests (test_50_*.py)
├── routes/           # Route tests
├── client/           # Client tests
├── integrations/     # Integration tests
├── tools/            # Tool tests
└── utils/            # Utility tests
```

### Test File Naming

- **Class tests**: `tests/classes/test_50_ClassName.py`
- **Route tests**: `tests/routes/module_name.py` or `test_module_name.py`
- **Client tests**: `tests/client/test_component.py`

## Standard Test Pattern

All tests follow a consistent async pattern with environment-based configuration:

```python
import os
from dotenv import load_dotenv
import domolibrary2.client.auth as dmda
import domolibrary2.classes.DomoUser as dmdu

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)

# Test data from environment
TEST_USER_ID_1 = os.environ.get("USER_ID_1")

async def test_cell_1(token_auth=token_auth):
    """Test description of what this validates."""
    # Test implementation
    result = await dmdu.DomoUser.get_by_id(
        auth=token_auth,
        user_id=TEST_USER_ID_1
    )
    assert result is not None
    assert result.id == TEST_USER_ID_1
    return result
```

## Test Requirements

### Essential Elements

1. **Async Functions**: All test functions must be async
2. **Environment Variables**: Use `.env` file for test configuration
3. **Type Hints**: Include type hints on test functions where helpful
4. **Docstrings**: Document what each test validates
5. **Assertions**: Include clear assertions for validation
6. **Return Values**: Optionally return results for inspection

### Environment Variables

Store sensitive data in `.env` (never commit):

```bash
DOMO_INSTANCE="your-instance"
DOMO_ACCESS_TOKEN="your-developer-token"
USER_ID_1="test-user-id"
DATASET_ID_1="test-dataset-id"
ACCOUNT_CREDENTIAL_ID_1="123"
# Add more as needed
```

Update `.env_sample` with new variables (without actual values).

## Running Tests

### Using Scripts

```powershell
# Run all tests with coverage
.\scripts\test.ps1

# Run specific test file
uv run pytest tests/classes/test_50_DomoUser.py -v

# Run specific test function
uv run pytest tests/classes/test_50_DomoUser.py::test_cell_1 -v

# Run with coverage report
uv run pytest tests/ --cov=src --cov-report=html
```

### Using pytest directly

```powershell
# All tests
pytest tests/ -v

# Specific module
pytest tests/classes/ -v

# With markers
pytest tests/ -m "not integration" -v

# Stop on first failure
pytest tests/ -x
```

## Test Markers

Use pytest markers to categorize tests:

```python
import pytest

@pytest.mark.unit
async def test_basic_functionality():
    """Unit test for basic functionality."""
    pass

@pytest.mark.integration
async def test_api_integration():
    """Integration test requiring real API calls."""
    pass

@pytest.mark.slow
async def test_large_dataset():
    """Test that takes significant time."""
    pass
```

Run specific markers:
```powershell
pytest -m unit  # Only unit tests
pytest -m "not integration"  # Skip integration tests
```

## Test Patterns

### Testing Class Methods

```python
async def test_get_by_id():
    """Test retrieving entity by ID."""
    entity = await DomoEntity.get_by_id(
        auth=token_auth,
        entity_id=TEST_ENTITY_ID
    )
    assert entity is not None
    assert entity.id == TEST_ENTITY_ID
    assert entity.auth.domo_instance == token_auth.domo_instance
```

### Testing Route Functions

```python
from domolibrary2.routes import user as user_routes

async def test_route_get_user():
    """Test user route returns valid response."""
    res = await user_routes.get_by_id(
        auth=token_auth,
        user_id=TEST_USER_ID
    )
    assert res.is_success
    assert res.status == 200
    assert res.response.get("id") == TEST_USER_ID
```

### Testing Error Handling

```python
from domolibrary2.routes.user.exceptions import User_GET_Error

async def test_invalid_user_id():
    """Test that invalid user ID raises appropriate error."""
    with pytest.raises(User_GET_Error) as exc_info:
        await user_routes.get_by_id(
            auth=token_auth,
            user_id="invalid-id-12345"
        )
    assert "not found" in str(exc_info.value).lower()
```

### Testing with Mocks (when needed)

```python
from unittest.mock import AsyncMock, patch

async def test_with_mock():
    """Test using mocked API responses."""
    mock_response = {"id": "123", "name": "Test User"}

    with patch('domolibrary2.routes.user.get_by_id') as mock_get:
        mock_get.return_value.response = mock_response
        mock_get.return_value.is_success = True

        result = await user_routes.get_by_id(
            auth=token_auth,
            user_id="123"
        )
        assert result.response == mock_response
```

## Test Organization Best Practices

### 1. Group Related Tests

```python
class TestUserCRUD:
    """Group of tests for user CRUD operations."""

    async def test_create_user(self):
        """Test user creation."""
        pass

    async def test_update_user(self):
        """Test user update."""
        pass

    async def test_delete_user(self):
        """Test user deletion."""
        pass
```

### 2. Use Fixtures for Common Setup

```python
import pytest

@pytest.fixture
async def test_user(token_auth):
    """Create a test user for multiple tests."""
    user = await create_test_user(auth=token_auth)
    yield user
    # Cleanup
    await delete_test_user(auth=token_auth, user_id=user.id)

async def test_with_fixture(test_user):
    """Test using the fixture."""
    assert test_user.id is not None
```

### 3. Skip Tests Conditionally

```python
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Integration tests disabled"
)
async def test_integration():
    """Integration test."""
    pass
```

## Coverage Requirements

- Aim for >80% code coverage
- All public methods should have tests
- Critical paths must be tested
- Error scenarios should be tested

View coverage report:
```powershell
.\scripts\test.ps1
# Open htmlcov/index.html in browser
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Pre-release checks

Ensure all tests pass before submitting PRs.

## Debugging Tests

### Run with verbose output

```powershell
pytest tests/ -vv --tb=long
```

### Run with logging

```powershell
pytest tests/ -v --log-cli-level=DEBUG
```

### Debug specific test

```powershell
pytest tests/classes/test_50_DomoUser.py::test_cell_1 -vv -s
```

## Reference

- Full test examples: `tests/classes/test_50_DomoUser.py`
- Route tests: `tests/routes/access_token.py`
- Testing guide: `docs/testing-guide.md`
