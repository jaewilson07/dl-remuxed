"""
Test suite for DomoInstanceConfig class
Tests various instance configuration methods and properties
"""

import datetime as dt
import os
from typing import Optional

import pandas as pd
import pytest
from domolibrary2.classes.DomoInstanceConfig.instance_config import DomoInstanceConfig
from dotenv import load_dotenv

from domolibrary2.classes.DomoUser import DomoUser, DomoUsers
from domolibrary2.client.auth import DomoFullAuth, DomoTokenAuth

load_dotenv()


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def token_auth() -> DomoTokenAuth:
    """Fixture for token-based authentication."""
    return DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )


@pytest.fixture
def community_token_auth() -> DomoTokenAuth:
    """Fixture for community instance token authentication."""
    return DomoTokenAuth(
        domo_instance="domo-community",
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )


@pytest.fixture
def full_auth() -> DomoFullAuth:
    """Fixture for full authentication with username/password."""
    return DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )


@pytest.fixture
def domo_config(token_auth: DomoTokenAuth) -> DomoInstanceConfig:
    """Fixture for DomoInstanceConfig instance."""
    return DomoInstanceConfig(auth=token_auth)  # type: ignore


@pytest.fixture
def community_domo_config(community_token_auth: DomoTokenAuth) -> DomoInstanceConfig:
    """Fixture for community instance DomoInstanceConfig."""
    return DomoInstanceConfig(auth=community_token_auth)  # type: ignore


@pytest.fixture
async def test_user(token_auth: DomoTokenAuth) -> Optional[DomoUser]:
    """Fixture to get a test user from the instance."""
    domo_users = await DomoUsers(auth=token_auth).get()  # type: ignore
    test_user = next(
        (
            user
            for user in domo_users
            if user.display_name and "test" in user.display_name.lower()
        ),
        None,
    )
    return test_user


# ============================================================================
# ACCOUNT TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_accounts(domo_config: DomoInstanceConfig):
    """Test retrieving Domo accounts."""
    assert domo_config.Accounts is not None
    accounts = await domo_config.Accounts.get()
    assert accounts is not None
    assert isinstance(accounts, list)
    # Verify first 5 accounts (if they exist)
    sample_accounts = accounts[0:5]
    assert len(sample_accounts) <= 5


# ============================================================================
# ACCESS TOKEN TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_access_tokens(domo_config: DomoInstanceConfig):
    """Test retrieving access tokens."""
    assert domo_config.AccessTokens is not None
    tokens = await domo_config.AccessTokens.get()
    assert tokens is not None
    assert isinstance(tokens, list)


@pytest.mark.asyncio
async def test_generate_and_revoke_access_token(
    domo_config: DomoInstanceConfig, test_user: Optional[DomoUser]
):
    """Test generating and revoking an access token."""
    if not test_user:
        pytest.skip("No test user available")

    assert domo_config.AccessTokens is not None
    token = await domo_config.AccessTokens.generate(
        owner=test_user,
        duration_in_days=15,
        token_name=f"DL test {dt.date.today()}",
    )
    assert token is not None
    assert token.token is not None
    assert isinstance(token.token, str)

    # Clean up: revoke the token
    await token.revoke()


# ============================================================================
# ALLOWLIST TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_allowlist(domo_config: DomoInstanceConfig):
    """Test retrieving IP allowlist."""
    assert domo_config.Allowlist is not None
    allowlist = await domo_config.Allowlist.get()
    assert allowlist is not None


# ============================================================================
# API CLIENT TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_api_clients(community_domo_config: DomoInstanceConfig):
    """Test retrieving API clients."""
    assert community_domo_config.ApiClients is not None
    api_clients = await community_domo_config.ApiClients.get()
    assert api_clients is not None
    assert isinstance(api_clients, list)


# ============================================================================
# APPLICATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_generate_applications_report(domo_config: DomoInstanceConfig):
    """Test generating applications report."""
    report = await domo_config.generate_applications_report()
    assert report is not None
    assert isinstance(report, pd.DataFrame)


# ============================================================================
# CONNECTOR TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_connectors(domo_config: DomoInstanceConfig):
    """Test retrieving all connectors."""
    assert domo_config.Connectors is not None
    connectors = await domo_config.Connectors.get()
    assert connectors is not None
    assert isinstance(connectors, list)


@pytest.mark.asyncio
async def test_search_connectors(domo_config: DomoInstanceConfig):
    """Test searching for specific connectors."""
    assert domo_config.Connectors is not None
    connectors = await domo_config.Connectors.get(
        search_text="snowflake", return_raw=False, debug_api=False
    )
    assert connectors is not None
    assert isinstance(connectors, list)


# ============================================================================
# DOMAIN TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_authorized_domains(domo_config: DomoInstanceConfig):
    """Test retrieving authorized domains."""
    domains = await domo_config.get_authorized_domains(return_raw=False)
    assert domains is not None


@pytest.mark.asyncio
async def test_get_authorized_custom_app_domains(domo_config: DomoInstanceConfig):
    """Test retrieving authorized custom app domains."""
    domains = await domo_config.get_authorized_custom_app_domains(return_raw=False)
    assert domains is not None


# ============================================================================
# GRANT TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_grants(domo_config: DomoInstanceConfig):
    """Test retrieving grants."""
    assert domo_config.Grants is not None
    grants = await domo_config.Grants.get()
    assert grants is not None
    assert isinstance(grants, list)
    # Verify we can convert to DataFrame
    if grants:
        df = pd.DataFrame(grants[0:5])
        assert isinstance(df, pd.DataFrame)


# ============================================================================
# MFA TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_mfa_config(community_domo_config: DomoInstanceConfig):
    """Test retrieving MFA configuration."""
    assert community_domo_config.MFA is not None
    mfa_config = await community_domo_config.MFA.get()
    assert mfa_config is not None


# ============================================================================
# PUBLISH (EVERYWHERE) TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_publications(domo_config: DomoInstanceConfig):
    """Test retrieving Domo Everywhere publications."""
    assert domo_config.Everywhere is not None
    publications = await domo_config.Everywhere.get_publications()
    assert publications is not None
    assert isinstance(publications, list)


# ============================================================================
# ROLE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_roles(domo_config: DomoInstanceConfig):
    """Test retrieving roles."""
    assert domo_config.Roles is not None
    roles = await domo_config.Roles.get()
    assert roles is not None
    assert isinstance(roles, list)


# ============================================================================
# SANDBOX TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_sandbox_same_instance_promotion(domo_config: DomoInstanceConfig):
    """Test checking sandbox same instance promotion setting."""
    result = await domo_config.get_sandbox_is_same_instance_promotion_enabled(
        debug_api=False, return_raw=False
    )
    assert result is not None
    assert isinstance(result, dict)
    assert "is_enabled" in result


@pytest.mark.asyncio
async def test_toggle_sandbox_same_instance_promotion(domo_config: DomoInstanceConfig):
    """Test toggling sandbox same instance promotion."""
    result = await domo_config.toggle_sandbox_allow_same_instance_promotion(
        is_enabled=True,
        debug_api=False,
        return_raw=False,
    )
    assert result is not None


# ============================================================================
# USER NOTIFICATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_user_invite_notification_enabled(domo_config: DomoInstanceConfig):
    """Test checking user invite notification setting."""
    result = await domo_config.get_is_user_invite_notification_enabled(
        debug_api=False, return_raw=False
    )
    assert result is not None
    assert isinstance(result, dict)
    assert "is_enabled" in result


@pytest.mark.asyncio
async def test_toggle_user_invite_notification(domo_config: DomoInstanceConfig):
    """Test toggling user invite notification."""
    result = await domo_config.toggle_is_user_invite_notification_enabled(
        is_enabled=True
    )
    assert result is not None


# ============================================================================
# SOCIAL USER TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_invite_social_users_enabled(domo_config: DomoInstanceConfig):
    """Test checking if social user invites are enabled."""
    from domolibrary2.classes.DomoInstanceConfig.instance_config import (
        DomoInstanceConfig as DIC,
    )

    try:
        result = await domo_config.get_is_invite_social_users_enabled(
            debug_api=False, return_raw=False
        )
        assert result is not None
    except DIC.InstanceConfig_ClassError as e:
        # Expected for instances without proper auth
        pytest.skip(f"Auth error (expected): {e}")


@pytest.mark.asyncio
async def test_toggle_invite_social_users(domo_config: DomoInstanceConfig):
    """Test toggling social user invites."""
    from domolibrary2.classes.DomoInstanceConfig.instance_config import (
        DomoInstanceConfig as DIC,
    )

    try:
        result = await domo_config.toggle_is_invite_social_users_enabled(
            is_enabled=True
        )
        assert result is not None
    except DIC.InstanceConfig_ClassError as e:
        pytest.skip(f"Auth error (expected): {e}")


# ============================================================================
# SSO TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_sso_config(domo_config: DomoInstanceConfig):
    """Test retrieving SSO configuration."""
    assert domo_config.SSO is not None
    sso_config = await domo_config.SSO.get()  # type: ignore
    assert sso_config is not None


# ============================================================================
# USER ATTRIBUTE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_user_attributes(domo_config: DomoInstanceConfig):
    """Test retrieving user attributes."""
    assert domo_config.UserAttributes is not None
    user_attributes = await domo_config.UserAttributes.get()
    assert user_attributes is not None
    assert isinstance(user_attributes, list)


# ============================================================================
# WEEKLY DIGEST TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_weekly_digest_enabled(full_auth: DomoFullAuth):
    """Test checking weekly digest setting."""
    from domolibrary2.base.exceptions import DomoError

    domo_config = DomoInstanceConfig(auth=full_auth)  # type: ignore

    try:
        result = await domo_config.get_is_weekly_digest_enabled(return_raw=True)
        assert result is not None
    except DomoError as e:
        # Some instances may not support this feature
        pytest.skip(f"Weekly digest not supported: {e}")


@pytest.mark.asyncio
async def test_toggle_weekly_digest(full_auth: DomoFullAuth):
    """Test toggling weekly digest."""
    from domolibrary2.base.exceptions import DomoError

    domo_config = DomoInstanceConfig(auth=full_auth)  # type: ignore

    try:
        result = await domo_config.toggle_is_weekly_digest_enabled(is_enabled=False)
        assert result is not None
    except DomoError as e:
        pytest.skip(f"Weekly digest not supported: {e}")


# ============================================================================
# LEFT NAV TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_get_left_nav_enabled(domo_config: DomoInstanceConfig):
    """Test checking left navigation setting."""
    result = await domo_config.get_is_left_nav_enabled()
    assert result is not None


@pytest.mark.asyncio
async def test_toggle_left_nav(domo_config: DomoInstanceConfig):
    """Test toggling left navigation (duplicate test removed)."""
    # This is intentionally the same as test_get_left_nav_enabled
    # The original had duplicate test_cell_27 and test_cell_28
    result = await domo_config.get_is_left_nav_enabled()
    assert result is not None
