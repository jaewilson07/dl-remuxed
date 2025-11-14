r"""
Test file generated from 50_DomoInsanceConfig_SSO.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os

from domolibrary2.classes.DomoInstanceConfig.sso import (
    SSO,
    SSO_OIDC_Config,
    SSO_SAML_Config,
    SSOConfig_InstantiationError,
)
from domolibrary2.classes.DomoUser import DomoUsers
from domolibrary2.auth import DomoFullAuth, DomoTokenAuth

# Setup authentication for tests
token_auth = DomoTokenAuth(
    domo_instance=os.environ["DOMO_INSTANCE"],
    domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    token_auth = DomoTokenAuth(
        domo_instance="domo-alpha",
        domo_access_token=os.environ["ALPHA_ACCESS_TOKEN"],
    )

    # token_auth = dmda.DomoTokenAuth(
    #     domo_instance=os.environ['DOMO_INSTANCE'],
    #     domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    # )

    # token_auth = dmda.DomoTokenAuth(
    #     domo_instance= "domo-community",
    #     domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    # )

    DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )

    domo_users = await DomoUsers.all_users(auth=token_auth)
    next(

            domo_user
            for domo_user in domo_users
            if "test" in domo_user.display_name.lower()

    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    await SSO_OIDC_Config.get(auth=token_auth, return_raw=False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    await SSO_SAML_Config.get(auth=token_auth, debug_prn=False, return_raw=False)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    sso_config = await SSO_SAML_Config.get(auth=token_auth, return_raw=False)

    try:
        sso_config.set_attribute(
            require_invitation=True,
            override_embed="abc",
        )

        await sso_config.update(
            debug_api=False,
        )
    except SSOConfig_InstantiationError as e:
        print(e)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    show_doc(SSO)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    sso = SSO(auth=token_auth)
    await sso.get()
