"""
Test file generated from DomoInstanceConfig_Allowlist.ipynb
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
        domo_instance="domo-community",
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    dmal = DomoAllowlist(auth=token_auth)
    await dmal.get(return_raw = False)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    test_ips = ['0.0.0.0/0']
    await dmal.add_ips(test_ips)


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    test_ips = ['0.0.0.0/0']

    await dmal.remove_ips(ip_address_ls=test_ips, debug_api = False)


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    await dmal.set(ip_address_ls=[])


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    dmal = DomoAllowlist(auth=token_auth)

    await dmal.get_is_filter_all_traffic_enabled()


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    dmal = DomoAllowlist(auth=token_auth)

    await dmal.toggle_is_filter_all_traffic_enabled(
        is_enabled=False, debug_prn=True, return_raw=True
    )
