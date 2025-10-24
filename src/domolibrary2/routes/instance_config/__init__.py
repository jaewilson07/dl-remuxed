"""
Instance Config Package

This package provides instance configuration management functionality including
API client management, MFA settings, SSO configuration, and other instance-level settings.

Modules:
    exceptions: Exception classes for instance config operations
    api_client: API client (developer token) management functions
"""

from .authorized_domains import (
    get_authorized_domains,
    set_authorized_domains,
    get_authorized_custom_app_domains,
    set_authorized_custom_app_domains,
)
from .toggle import (
    get_is_invite_social_users_enabled,
    get_is_user_invite_notifications_enabled,
    get_is_weekly_digest_enabled,
    toggle_is_weekly_digest_enabled,
    toggle_is_user_invite_enabled,
    toggle_is_left_nav_enabled,
    get_is_left_nav_enabled,
)
from .allowlist import (
    get_allowlist,
    set_allowlist,
)


__all__ = [
    "get_authorized_domains",
    "set_authorized_domains",
    "get_authorized_custom_app_domains",
    "set_authorized_custom_app_domains",
    "get_is_invite_social_users_enabled",
    "get_is_user_invite_notifications_enabled",
    "get_is_weekly_digest_enabled",
    "toggle_is_weekly_digest_enabled",
    "toggle_is_user_invite_enabled",
    "toggle_is_left_nav_enabled",
    "get_is_left_nav_enabled",
    "get_allowlist",
    "set_allowlist",
]
