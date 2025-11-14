r"""
Test file generated from instance_config_sso.ipynb
Auto-generated - excludes cells starting with #
Generated on: C:\GitHub\domolibrary
"""

import os

import domolibrary.client.DomoAuth as dmda

# Setup authentication for tests
token_auth = dmda.DomoTokenAuth(
    domo_instance=os.environ['DOMO_INSTANCE'],
    domo_access_token=os.environ['DOMO_ACCESS_TOKEN'],
)


async def test_cell_1(token_auth=token_auth):
    """Test case from cell 1"""
    auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    await auth.print_is_token()

    dmda.DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_user = await dmdu.DomoUsers.by_email(
        auth= auth,
        email_ls= ['jae@datacrew.space']
    )

    await toggle_user_direct_signon_access(
        auth = auth,
        user_id_ls = [domo_user.id],
        debug_api = False,
    )


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    (await get_sso_saml_config(auth=auth)).response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    (await get_sso_saml_certificate(auth = auth)).response


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    body_sso = generate_sso_saml_body(
        is_include_undefined = False,

        is_enabled=True,
        auth_request_endpoint = "",
        issuer = "",
        idp_certificate  = "",
        import_groups  = False,
        require_invitation = False,
        enforce_allowlist =True,
        relay_state = False,
        redirect_url = "",
        idp_enabled = True,
        skip_to_idp = False,
        custom_attributes  = False
    )

    body_sso
