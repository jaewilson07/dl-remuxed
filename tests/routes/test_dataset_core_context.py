"""
Test RouteContext migration for dataset/core.py

Tests backward compatibility and new context parameter functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from domolibrary2.auth import DomoTokenAuth
from domolibrary2.client.context import RouteContext
from domolibrary2.routes.dataset import core as dataset_core


@pytest.fixture
def mock_auth():
    """Create a mock auth object."""
    auth = MagicMock(spec=DomoTokenAuth)
    auth.domo_instance = "test-instance"
    auth.auth_header = {"Authorization": "Bearer test-token"}
    return auth


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    from domolibrary2.client.response import ResponseGetData
    
    response = MagicMock(spec=ResponseGetData)
    response.is_success = True
    response.status = 200
    response.response = {"id": "test-dataset-id", "name": "Test Dataset"}
    return response


class TestRouteContextBackwardCompatibility:
    """Test that old parameter style still works."""

    @pytest.mark.asyncio
    async def test_get_dataset_by_id_old_style(self, mock_auth, mock_response):
        """Test get_dataset_by_id with old parameter style."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            # Call with old-style parameters (no context)
            result = await dataset_core.get_dataset_by_id(
                dataset_id="test-dataset-id",
                auth=mock_auth,
                debug_api=True,
                session=None,
                parent_class="TestClass",
                debug_num_stacks_to_drop=2,
            )
            
            # Verify the function was called
            assert mock_get_data.called
            assert result.is_success
            
            # Verify context was created internally
            call_kwargs = mock_get_data.call_args.kwargs
            assert 'context' in call_kwargs
            assert isinstance(call_kwargs['context'], RouteContext)
            assert call_kwargs['context'].debug_api is True
            assert call_kwargs['context'].parent_class == "TestClass"

    @pytest.mark.asyncio
    async def test_get_dataset_by_id_new_style(self, mock_auth, mock_response):
        """Test get_dataset_by_id with new context parameter."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            # Create context explicitly
            context = RouteContext(
                debug_api=True,
                parent_class="TestClass",
                debug_num_stacks_to_drop=2,
            )
            
            # Call with new-style context parameter
            result = await dataset_core.get_dataset_by_id(
                dataset_id="test-dataset-id",
                auth=mock_auth,
                context=context,
            )
            
            # Verify the function was called
            assert mock_get_data.called
            assert result.is_success
            
            # Verify context was passed through
            call_kwargs = mock_get_data.call_args.kwargs
            assert 'context' in call_kwargs
            assert call_kwargs['context'] is context

    @pytest.mark.asyncio
    async def test_create_old_style(self, mock_auth, mock_response):
        """Test create with old parameter style."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            # Call with old-style parameters (no context)
            result = await dataset_core.create(
                auth=mock_auth,
                dataset_name="Test Dataset",
                dataset_type="api",
                schema=None,
                debug_api=False,
                session=None,
            )
            
            # Verify the function was called
            assert mock_get_data.called
            assert result.is_success
            
            # Verify context was created internally
            call_kwargs = mock_get_data.call_args.kwargs
            assert 'context' in call_kwargs
            assert isinstance(call_kwargs['context'], RouteContext)

    @pytest.mark.asyncio
    async def test_delete_old_style(self, mock_auth, mock_response):
        """Test delete with old parameter style."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            # Call with old-style parameters (no context)
            result = await dataset_core.delete(
                auth=mock_auth,
                dataset_id="test-dataset-id",
                debug_api=False,
                session=None,
            )
            
            # Verify the function was called
            assert mock_get_data.called
            assert result.is_success
            
            # Verify context was created internally
            call_kwargs = mock_get_data.call_args.kwargs
            assert 'context' in call_kwargs
            assert isinstance(call_kwargs['context'], RouteContext)


class TestRouteContextIntegration:
    """Test RouteContext integration with get_data."""

    @pytest.mark.asyncio
    async def test_context_parameter_extraction(self, mock_auth, mock_response):
        """Test that get_data extracts parameters from context."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            # Create context with all parameters
            context = RouteContext(
                session=None,
                debug_api=True,
                parent_class="TestClass",
                debug_num_stacks_to_drop=3,
            )
            
            # Call function with context
            await dataset_core.get_dataset_by_id(
                dataset_id="test-dataset-id",
                auth=mock_auth,
                context=context,
            )
            
            # Verify context was passed to get_data
            call_kwargs = mock_get_data.call_args.kwargs
            assert 'context' in call_kwargs
            passed_context = call_kwargs['context']
            assert passed_context.debug_api is True
            assert passed_context.parent_class == "TestClass"
            assert passed_context.debug_num_stacks_to_drop == 3


class TestAllFunctionsMigrated:
    """Test that all 6 functions have been migrated."""

    @pytest.mark.asyncio
    async def test_all_functions_accept_context(self, mock_auth, mock_response):
        """Verify all 6 functions accept context parameter."""
        with patch('domolibrary2.routes.dataset.core.gd.get_data', new_callable=AsyncMock) as mock_get_data:
            mock_get_data.return_value = mock_response
            
            context = RouteContext()
            
            # Test all 6 functions
            functions_to_test = [
                ('get_dataset_by_id', {'dataset_id': 'test-id'}),
                ('create', {'dataset_name': 'Test Dataset'}),
                ('create_dataset_enterprise_tookit', {'payload': {}}),
                ('delete_partition_stage_1', {'dataset_id': 'test-id', 'dataset_partition_id': 'partition-id'}),
                ('delete_partition_stage_2', {'dataset_id': 'test-id', 'dataset_partition_id': 'partition-id'}),
                ('delete', {'dataset_id': 'test-id'}),
            ]
            
            for func_name, kwargs in functions_to_test:
                func = getattr(dataset_core, func_name)
                
                # Call with context parameter
                try:
                    await func(auth=mock_auth, context=context, **kwargs)
                except Exception as e:
                    pytest.fail(f"{func_name} failed to accept context parameter: {e}")
                
                # Verify get_data was called with context
                call_kwargs = mock_get_data.call_args.kwargs
                assert 'context' in call_kwargs, f"{func_name} did not pass context to get_data"
