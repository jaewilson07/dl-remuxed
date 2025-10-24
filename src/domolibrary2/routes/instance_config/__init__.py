"""
Instance Config Package

This package provides instance configuration management functionality including
API client management, MFA settings, SSO configuration, and other instance-level settings.

Modules:
    exceptions: Exception classes for instance config operations
    api_client: API client (developer token) management functions
"""

from .authorized_domains import (
    get_authorized_custom_app_domains,
    get_authorized_domains,
    set_authorized_custom_app_domains,
    set_authorized_domains,
)
from .allowlist import (
    get_allowlist,
    set_allowlist,
    get_allowlist_is_filter_all_traffic_enabled,
    toggle_allowlist_is_filter_all_traffic_enabled,
)
from .instance_switcher import (
    get_instance_switcher_mapping,
    set_instance_switcher_mapping,
)
from .mfa import (
    get_mfa_config,
    toggle_enable_mfa,
    set_mfa_max_code_attempts,
    set_mfa_num_days_valid,
)
from .toggle import (
    get_is_invite_social_users_enabled,
    get_is_left_nav_enabled,
    get_is_user_invite_notifications_enabled,
    get_is_weekly_digest_enabled,
    toggle_is_left_nav_enabled,
    toggle_is_user_invite_enabled,
    toggle_is_weekly_digest_enabled,
)
from .scheduler_policies import (
    get_scheduler_policies,
    create_scheduler_policy,
    update_scheduler_policy,
    delete_scheduler_policy,
)

__all__ = [
    # Authorized Domains
    "get_authorized_domains",
    "set_authorized_domains",
    "get_authorized_custom_app_domains",
    "set_authorized_custom_app_domains",
    # Allowlist
    "get_allowlist",
    "set_allowlist",
    "get_allowlist_is_filter_all_traffic_enabled",
    "toggle_allowlist_is_filter_all_traffic_enabled",
    # Instance Switcher
    "get_instance_switcher_mapping",
    "set_instance_switcher_mapping",
    # MFA
    "get_mfa_config",
    "toggle_enable_mfa",
    "set_mfa_max_code_attempts",
    "set_mfa_num_days_valid",
    # Toggle
    "get_is_invite_social_users_enabled",
    "get_is_user_invite_notifications_enabled",
    "get_is_weekly_digest_enabled",
    "toggle_is_weekly_digest_enabled",
    "toggle_is_user_invite_enabled",
    "toggle_is_left_nav_enabled",
    "get_is_left_nav_enabled",
    # Scheduler Policies
    "get_scheduler_policies",
    "create_scheduler_policy",
    "update_scheduler_policy",
    "delete_scheduler_policy",
]
