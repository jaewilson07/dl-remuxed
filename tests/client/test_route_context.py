"""
Tests for RouteContext class
"""

import pytest
import httpx
from domolibrary2.client.context import RouteContext


def test_route_context_creation():
    """Test basic RouteContext creation with default values"""
    context = RouteContext()
    
    assert context.session is None
    assert context.debug_api is False
    assert context.debug_num_stacks_to_drop == 1
    assert context.parent_class is None


def test_route_context_with_values():
    """Test RouteContext creation with custom values"""
    session = httpx.AsyncClient()
    context = RouteContext(
        session=session,
        debug_api=True,
        debug_num_stacks_to_drop=2,
        parent_class="TestClass",
    )
    
    assert context.session is session
    assert context.debug_api is True
    assert context.debug_num_stacks_to_drop == 2
    assert context.parent_class == "TestClass"


def test_route_context_from_kwargs():
    """Test RouteContext.from_kwargs() class method"""
    session = httpx.AsyncClient()
    context = RouteContext.from_kwargs(
        session=session,
        debug_api=True,
        debug_num_stacks_to_drop=3,
        parent_class="FromKwargs",
    )
    
    assert context.session is session
    assert context.debug_api is True
    assert context.debug_num_stacks_to_drop == 3
    assert context.parent_class == "FromKwargs"


def test_route_context_with_parent_class():
    """Test RouteContext.with_parent_class() method"""
    context = RouteContext(
        debug_api=True,
        debug_num_stacks_to_drop=2,
        parent_class="OriginalClass",
    )
    
    new_context = context.with_parent_class("NewClass")
    
    # Original context unchanged
    assert context.parent_class == "OriginalClass"
    
    # New context has updated parent_class but same other values
    assert new_context.parent_class == "NewClass"
    assert new_context.debug_api is True
    assert new_context.debug_num_stacks_to_drop == 2


def test_route_context_to_dict():
    """Test RouteContext.to_dict() method"""
    session = httpx.AsyncClient()
    context = RouteContext(
        session=session,
        debug_api=True,
        debug_num_stacks_to_drop=4,
        parent_class="DictTest",
    )
    
    context_dict = context.to_dict()
    
    assert isinstance(context_dict, dict)
    assert context_dict["session"] is session
    assert context_dict["debug_api"] is True
    assert context_dict["debug_num_stacks_to_drop"] == 4
    assert context_dict["parent_class"] == "DictTest"
    assert len(context_dict) == 4  # Should only have these 4 keys
