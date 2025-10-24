"""
Test file generated from instance_config.ipynb
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
    token_auth = dmda.DomoTokenAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_access_token=os.environ["DOMO_ACCESS_TOKEN"],
    )

    full_auth = dmda.DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    ip_address_ls = []


    await set_allowlist(auth=full_auth, ip_address_ls=ip_address_ls, return_raw = False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    res = await get_allowlist_is_filter_all_traffic_enabled(auth=token_auth, debug_api=False)
    res.response


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    await toggle_allowlist_is_filter_all_traffic_enabled(auth=full_auth, is_enabled=False, debug_api=False)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await get_authorized_custom_app_domains(auth=token_auth, debug_api=False)


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    authorized_app_domains = (await get_authorized_custom_app_domains(auth=token_auth, debug_api=False)).response

    await set_authorized_custom_app_domains(
        auth=token_auth, authorized_custom_app_domain_ls=authorized_app_domains
    )


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    await toggle_is_left_nav_enabled(
        is_use_left_nav = True,
        auth=token_auth, return_raw=False, debug_api=False
    )
