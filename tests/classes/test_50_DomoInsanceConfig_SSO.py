"""
Tests for SSO (Single Sign-On) configuration classes.

Tests SSO, SSO_OIDC_Config, and SSO_SAML_Config classes following
domolibrary2 testing patterns.
"""

import os

import pytest
from dotenv import load_dotenv

import domolibrary2.client.auth as dmda
from domolibrary2.classes.DomoInstanceConfig.SSO import (
    SSO,
    SSO_OIDC_Config,
    SSO_SAML_Config,
    SSOConfig_InstantiationError,
)

load_dotenv()

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


@pytest.mark.asyncio
async def test_get_oidc_config():
    """Test retrieving OIDC SSO configuration."""
    oidc_config = await SSO_OIDC_Config.get(auth=token_auth, return_raw=False)
    
    assert oidc_config is not None
    assert isinstance(oidc_config, SSO_OIDC_Config)
    assert oidc_config.auth == token_auth
    assert hasattr(oidc_config, "idp_enabled")
    assert hasattr(oidc_config, "login_enabled")
    assert hasattr(oidc_config, "import_groups")
    
    return oidc_config


@pytest.mark.asyncio
async def test_get_oidc_config_raw():
    """Test retrieving OIDC SSO configuration with return_raw=True."""
    res = await SSO_OIDC_Config.get(auth=token_auth, return_raw=True)
    
    assert res is not None
    assert hasattr(res, "response")
    assert hasattr(res, "is_success")
    assert res.is_success is True
    
    return res


@pytest.mark.asyncio
async def test_get_saml_config():
    """Test retrieving SAML SSO configuration."""
    saml_config = await SSO_SAML_Config.get(auth=token_auth, return_raw=False)
    
    assert saml_config is not None
    assert isinstance(saml_config, SSO_SAML_Config)
    assert saml_config.auth == token_auth
    assert hasattr(saml_config, "idp_enabled")
    assert hasattr(saml_config, "is_enabled")
    assert hasattr(saml_config, "import_groups")
    
    return saml_config


@pytest.mark.asyncio
async def test_get_saml_config_raw():
    """Test retrieving SAML SSO configuration with return_raw=True."""
    res = await SSO_SAML_Config.get(auth=token_auth, return_raw=True)
    
    assert res is not None
    assert hasattr(res, "response")
    assert hasattr(res, "is_success")
    assert res.is_success is True
    
    return res


@pytest.mark.asyncio
async def test_oidc_from_dict():
    """Test OIDC config from_dict method."""
    # First get the raw response
    res = await SSO_OIDC_Config.get(auth=token_auth, return_raw=True)
    
    # Then use from_dict
    oidc_config = SSO_OIDC_Config.from_dict(auth=token_auth, obj=res.response)
    
    assert oidc_config is not None
    assert isinstance(oidc_config, SSO_OIDC_Config)
    assert oidc_config.auth == token_auth
    
    return oidc_config


@pytest.mark.asyncio
async def test_saml_from_dict():
    """Test SAML config from_dict method."""
    # First get the raw response
    res = await SSO_SAML_Config.get(auth=token_auth, return_raw=True)
    
    # Then use from_dict
    saml_config = SSO_SAML_Config.from_dict(auth=token_auth, obj=res.response)
    
    assert saml_config is not None
    assert isinstance(saml_config, SSO_SAML_Config)
    assert saml_config.auth == token_auth
    
    return saml_config


@pytest.mark.asyncio
async def test_display_url():
    """Test display_url property."""
    oidc_config = await SSO_OIDC_Config.get(auth=token_auth)
    saml_config = await SSO_SAML_Config.get(auth=token_auth)
    
    assert oidc_config.display_url is not None
    assert saml_config.display_url is not None
    assert token_auth.domo_instance in oidc_config.display_url
    assert token_auth.domo_instance in saml_config.display_url
    assert "admin/security/sso" in oidc_config.display_url
    assert "admin/security/sso" in saml_config.display_url


@pytest.mark.asyncio
async def test_sso_manager_get_oidc():
    """Test SSO manager class get_oidc method."""
    sso = SSO(auth=token_auth)
    
    oidc = await sso.get_oidc()
    
    assert oidc is not None
    assert isinstance(oidc, SSO_OIDC_Config)
    assert sso.OIDC is not None
    assert sso.OIDC == oidc
    
    return sso


@pytest.mark.asyncio
async def test_sso_manager_get_saml():
    """Test SSO manager class get_saml method."""
    sso = SSO(auth=token_auth)
    
    saml = await sso.get_saml()
    
    assert saml is not None
    assert isinstance(saml, SSO_SAML_Config)
    assert sso.SAML is not None
    assert sso.SAML == saml
    
    return sso


@pytest.mark.asyncio
async def test_sso_manager_get():
    """Test SSO manager class get method (retrieves both OIDC and SAML)."""
    sso = SSO(auth=token_auth)
    
    result = await sso.get()
    
    assert result is not None
    assert result == sso
    assert sso.OIDC is not None
    assert sso.SAML is not None
    assert isinstance(sso.OIDC, SSO_OIDC_Config)
    assert isinstance(sso.SAML, SSO_SAML_Config)
    
    return sso


@pytest.mark.asyncio
async def test_set_attribute_invalid():
    """Test set_attribute with invalid attribute raises error."""
    oidc_config = await SSO_OIDC_Config.get(auth=token_auth)
    
    with pytest.raises(SSOConfig_InstantiationError):
        oidc_config.set_attribute(invalid_attribute="test")


@pytest.mark.asyncio
async def test_to_dict():
    """Test to_dict method on config classes."""
    oidc_config = await SSO_OIDC_Config.get(auth=token_auth)
    saml_config = await SSO_SAML_Config.get(auth=token_auth)
    
    oidc_dict = oidc_config.to_dict()
    saml_dict = saml_config.to_dict()
    
    assert isinstance(oidc_dict, dict)
    assert isinstance(saml_dict, dict)
    assert "auth" not in oidc_dict
    assert "raw" not in oidc_dict
    assert "auth" not in saml_dict
    assert "raw" not in saml_dict
