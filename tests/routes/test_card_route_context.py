"""
Test file for RouteContext pattern in card route functions.
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import domolibrary2.auth as dmda
from domolibrary2.client.context import RouteContext
from domolibrary2.client.response import ResponseGetData
from domolibrary2.routes import card as card_routes


@pytest.fixture
def mock_auth():
    """Create a mock DomoAuth object for testing."""
    auth = MagicMock(spec=dmda.DomoAuth)
    auth.domo_instance = "test-instance"
    auth.auth_header = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def mock_response():
    """Create a mock successful response."""
    response = ResponseGetData(
        status=200,
        response=[{"id": "test-card-123", "title": "Test Card"}],
        is_success=True,
    )
    return response


class TestRouteContext:
    """Test RouteContext integration with card route functions."""

    @pytest.mark.asyncio
    async def test_get_card_by_id_with_context(self, mock_auth, mock_response):
        """Test get_card_by_id with RouteContext parameter."""
        with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            context = RouteContext(
                debug_api=True,
                debug_num_stacks_to_drop=2,
                parent_class="TestClass",
            )
            
            result = await card_routes.get_card_by_id(
                card_id="test-card-123",
                auth=mock_auth,
                context=context,
            )
            
            assert result is not None
            assert result.is_success
            mock_get_data.assert_called_once()
            
            # Verify context was passed to get_data
            call_kwargs = mock_get_data.call_args.kwargs
            assert "context" in call_kwargs
            assert call_kwargs["context"] == context

    @pytest.mark.asyncio
    async def test_get_card_by_id_without_context(self, mock_auth, mock_response):
        """Test get_card_by_id without RouteContext (backward compatibility)."""
        with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            result = await card_routes.get_card_by_id(
                card_id="test-card-123",
                auth=mock_auth,
                debug_api=True,
                debug_num_stacks_to_drop=2,
                parent_class="TestClass",
            )
            
            assert result is not None
            assert result.is_success
            mock_get_data.assert_called_once()
            
            # Verify individual parameters were used to create context
            call_kwargs = mock_get_data.call_args.kwargs
            assert "context" in call_kwargs
            assert isinstance(call_kwargs["context"], RouteContext)

    @pytest.mark.asyncio
    async def test_get_kpi_definition_with_context(self, mock_auth):
        """Test get_kpi_definition with RouteContext parameter."""
        kpi_response = ResponseGetData(
            status=200,
            response={"urn": "test-card-123", "kpi": "value"},
            is_success=True,
        )
        
        with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = kpi_response
            
            context = RouteContext(
                debug_api=True,
                debug_num_stacks_to_drop=3,
            )
            
            result = await card_routes.get_kpi_definition(
                auth=mock_auth,
                card_id="test-card-123",
                context=context,
            )
            
            assert result is not None
            assert result.is_success
            mock_get_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_card_metadata_with_context(self, mock_auth, mock_response):
        """Test get_card_metadata with RouteContext parameter."""
        with patch("domolibrary2.client.get_data.get_data", new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            context = RouteContext(
                debug_api=False,
                parent_class="MetadataTest",
            )
            
            result = await card_routes.get_card_metadata(
                auth=mock_auth,
                card_id="test-card-123",
                context=context,
            )
            
            assert result is not None
            assert result.is_success
            mock_get_data.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_cards_admin_summary_with_context(self, mock_auth):
        """Test search_cards_admin_summary with RouteContext parameter."""
        search_response = ResponseGetData(
            status=200,
            response={
                "cardAdminSummaries": [
                    {"id": "card1", "title": "Card 1"},
                    {"id": "card2", "title": "Card 2"},
                ]
            },
            is_success=True,
        )
        
        with patch("domolibrary2.client.get_data.looper", new_callable=AsyncMock) as mock_looper:
            mock_looper.return_value = search_response
            
            context = RouteContext(
                debug_api=True,
                debug_num_stacks_to_drop=1,
                parent_class="SearchTest",
            )
            
            result = await card_routes.search_cards_admin_summary(
                auth=mock_auth,
                body={"cardTitleSearchText": "test"},
                maximum=10,
                context=context,
            )
            
            assert result is not None
            assert result.is_success
            mock_looper.assert_called_once()
            
            # Verify context was passed to looper
            call_kwargs = mock_looper.call_args.kwargs
            assert "context" in call_kwargs
            assert call_kwargs["context"] == context


class TestRouteContextClass:
    """Test the RouteContext class itself."""

    def test_route_context_creation(self):
        """Test creating a RouteContext instance."""
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=2,
            parent_class="TestClass",
        )
        
        assert context.debug_api is True
        assert context.debug_num_stacks_to_drop == 2
        assert context.parent_class == "TestClass"
        assert context.session is None

    def test_route_context_to_dict(self):
        """Test converting RouteContext to dictionary."""
        context = RouteContext(
            debug_api=True,
            debug_num_stacks_to_drop=3,
            parent_class="DictTest",
        )
        
        context_dict = context.to_dict()
        
        assert context_dict["debug_api"] is True
        assert context_dict["debug_num_stacks_to_drop"] == 3
        assert context_dict["parent_class"] == "DictTest"
        assert context_dict["session"] is None

    def test_route_context_from_params(self):
        """Test creating RouteContext from individual parameters."""
        context = RouteContext.from_params(
            debug_api=False,
            debug_num_stacks_to_drop=5,
            parent_class="FromParamsTest",
        )
        
        assert context.debug_api is False
        assert context.debug_num_stacks_to_drop == 5
        assert context.parent_class == "FromParamsTest"
