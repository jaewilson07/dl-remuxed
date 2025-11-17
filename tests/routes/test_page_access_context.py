"""
Test RouteContext migration for routes/page/access.py

This test verifies that:
1. Functions accept the new context parameter
2. Functions still work with old individual parameters (backward compatibility)
3. Context parameters properly override individual parameters
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from domolibrary2.auth import DomoAuth
from domolibrary2.client.context import RouteContext
from domolibrary2.client.response import ResponseGetData
from domolibrary2.routes.page import access as page_access


@pytest.fixture
def mock_auth():
    """Create a mock DomoAuth object."""
    auth = MagicMock(spec=DomoAuth)
    auth.domo_instance = "test-instance"
    auth.token = "mock-token"
    return auth


@pytest.fixture
def mock_response():
    """Create a mock successful response."""
    response = ResponseGetData(
        status=200,
        response={"id": "test-page-id", "access": "granted"},
        is_success=True,
    )
    return response


@pytest.mark.asyncio
async def test_get_page_access_test_with_context(mock_auth, mock_response):
    """Test get_page_access_test accepts context parameter."""
    with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = mock_response
        
        # Create a RouteContext
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=2,
            parent_class="TestClass"
        )
        
        # Call with context
        result = await page_access.get_page_access_test(
            auth=mock_auth,
            page_id="test-page-id",
            context=context,
        )
        
        # Verify the function was called with context
        assert mock_get_data.called
        call_kwargs = mock_get_data.call_args.kwargs
        assert "context" in call_kwargs
        assert call_kwargs["context"] == context
        assert result.is_success


@pytest.mark.asyncio
async def test_get_page_access_test_without_context(mock_auth, mock_response):
    """Test get_page_access_test still works with individual parameters."""
    with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = mock_response
        
        # Call with individual parameters (old style)
        result = await page_access.get_page_access_test(
            auth=mock_auth,
            page_id="test-page-id",
            debug_api=True,
            debug_num_stacks_to_drop=2,
            parent_class="TestClass"
        )
        
        # Verify the function creates a context internally
        assert mock_get_data.called
        call_kwargs = mock_get_data.call_args.kwargs
        assert "context" in call_kwargs
        assert isinstance(call_kwargs["context"], RouteContext)
        assert call_kwargs["context"].debug_api is True
        assert call_kwargs["context"].debug_num_stacks_to_drop == 2
        assert call_kwargs["context"].parent_class == "TestClass"
        assert result.is_success


@pytest.mark.asyncio
async def test_get_page_access_list_with_context(mock_auth, mock_response):
    """Test get_page_access_list accepts context parameter."""
    with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
        # Mock response with users and groups
        list_response = ResponseGetData(
            status=200,
            response={
                "users": [{"id": "user1", "name": "Test User"}],
                "groups": [{"id": "group1", "name": "Test Group", "users": []}]
            },
            is_success=True,
        )
        mock_get_data.return_value = list_response
        
        context = RouteContext(session=MagicMock(spec=httpx.AsyncClient))
        
        result = await page_access.get_page_access_list(
            auth=mock_auth,
            page_id="test-page-id",
            context=context,
        )
        
        assert mock_get_data.called
        call_kwargs = mock_get_data.call_args.kwargs
        assert "context" in call_kwargs
        assert result.is_success


@pytest.mark.asyncio
async def test_add_page_owner_with_context(mock_auth, mock_response):
    """Test add_page_owner accepts context parameter."""
    with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = mock_response
        
        context = RouteContext(debug_api=True)
        
        result = await page_access.add_page_owner(
            auth=mock_auth,
            page_id_ls=["page1", "page2"],
            user_id_ls=["user1"],
            context=context,
        )
        
        assert mock_get_data.called
        call_kwargs = mock_get_data.call_args.kwargs
        assert "context" in call_kwargs
        assert result.is_success


@pytest.mark.asyncio
async def test_context_parameters_override_individuals(mock_auth, mock_response):
    """Test that context parameters take precedence over individual parameters."""
    with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
        mock_get_data.return_value = mock_response
        
        # Create context with specific values
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=5,
            parent_class="ContextClass"
        )
        
        # Call with both context and individual parameters
        # Context should take precedence
        result = await page_access.get_page_access_test(
            auth=mock_auth,
            page_id="test-page-id",
            context=context,
            debug_api=False,  # Should be overridden by context
            debug_num_stacks_to_drop=1,  # Should be overridden by context
            parent_class="IndividualClass",  # Should be overridden by context
        )
        
        # Verify context was used
        assert mock_get_data.called
        call_kwargs = mock_get_data.call_args.kwargs
        assert call_kwargs["context"] == context
        assert result.is_success


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
