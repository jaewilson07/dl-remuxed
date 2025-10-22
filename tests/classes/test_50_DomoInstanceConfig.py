"""
Test file generated from 50_DomoInstanceConfig.ipynb
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
        domo_instance="domo-alpha",
        domo_access_token=os.environ["ALPHA_ACCESS_TOKEN"],
    )

    community_token_auth = dmda.DomoTokenAuth(
        domo_instance="domo-community",
        domo_access_token=os.environ["DOMO_DOJO_ACCESS_TOKEN"],
    )

    full_auth = dmda.DomoFullAuth(
        domo_instance=os.environ["DOMO_INSTANCE"],
        domo_username=os.environ["DOMO_USERNAME"],
        domo_password=os.environ["DOMO_PASSWORD"],
    )

    domo_users = await dmdu.DomoUsers.all_users(auth=token_auth)
    domo_user = next(
        (domo_user for domo_user in domo_users if "test" in domo_user.display_name.lower())
    )


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    domo_config = DomoInstanceConfig(auth=token_auth)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    (await domo_config.Accounts.get())[0:5]


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    (await domo_config.AccessTokens.get())[0:5]


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    token = await domo_config.AccessTokens.generate(
        owner=domo_user, duration_in_days=15, token_name=f"DL test {dt.date.today()}"
    )

    print(token.token)

    await token.revoke()


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    await domo_config.Allowlist.get()


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    domo_config = DomoInstanceConfig(auth=community_token_auth)

    (await domo_config.ApiClients.get())[0:5]


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    (await domo_config.generate_applications_report())[0:5]


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    (await domo_config.Connectors.get())[0:5]


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    (
        await domo_config.Connectors.get(
            search_text="snowflake", return_raw=False, debug_api=False
        )
    )[0:5]


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    dmdic = DomoInstanceConfig(auth=token_auth)

    await dmdic.get_authorized_domains(return_raw=False)


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    dmdic = DomoInstanceConfig(auth=token_auth)

    await dmdic.get_authorized_custom_app_domains(return_raw=False)


async def test_cell_13(token_auth=token_auth):
    """Test case from cell 13"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    pd.DataFrame((await domo_config.Grants.get())[0:5])


async def test_cell_14(token_auth=token_auth):
    """Test case from cell 14"""
    domo_config = DomoInstanceConfig(auth=community_token_auth)

    await domo_config.MFA.get()


async def test_cell_15(token_auth=token_auth):
    """Test case from cell 15"""
    (await domo_config.Everywhere.get_publications())[0:5]


async def test_cell_16(token_auth=token_auth):
    """Test case from cell 16"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    (await domo_config.Roles.get())[0:5]


async def test_cell_17(token_auth=token_auth):
    """Test case from cell 17"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    await domo_config.get_sandbox_is_same_instance_promotion_enabled(
        debug_api=False, return_raw=False
    )


async def test_cell_18(token_auth=token_auth):
    """Test case from cell 18"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    await domo_config.toggle_sandbox_allow_same_instance_promotion(
        is_enabled=True,
        debug_api=False,
        return_raw=False,
    )


async def test_cell_19(token_auth=token_auth):
    """Test case from cell 19"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    await domo_config.get_is_user_invite_notification_enabled(
        debug_api=False, return_raw=False
    )


async def test_cell_20(token_auth=token_auth):
    """Test case from cell 20"""
    domo_config = DomoInstanceConfig(auth=token_auth)

    await domo_config.toggle_is_user_invite_notification_enabled(is_enabled=True)


async def test_cell_21(token_auth=token_auth):
    """Test case from cell 21"""
    domo_config = DomoInstanceConfig(auth=full_auth)

    try:
        await domo_config.get_is_invite_social_users_enabled(
            debug_api=False, return_raw=False
        )

    except InstanceConfig_ClassError as e:
        print(e)


async def test_cell_22(token_auth=token_auth):
    """Test case from cell 22"""
    await domo_config.toggle_is_invite_social_users_enabled(is_enabled=True)


async def test_cell_23(token_auth=token_auth):
    """Test case from cell 23"""
    domo_config = DomoInstanceConfig(auth=token_auth)



    await domo_config.SSO.get()


async def test_cell_24(token_auth=token_auth):
    """Test case from cell 24"""
    (await domo_config.UserAttributes.get())[0:5]


async def test_cell_25(token_auth=token_auth):
    """Test case from cell 25"""
    domo_config = DomoInstanceConfig(auth=full_auth)

    try:
        print(await domo_config.get_is_weekly_digest_enabled(return_raw=True))

    except InstanceConfig_Error as e:
        print(e)


async def test_cell_26(token_auth=token_auth):
    """Test case from cell 26"""
    try:
        print(await domo_config.toggle_is_weekly_digest_enabled(is_enabled=False))
    except InstanceConfig_Error as e:
        print(e)


async def test_cell_27(token_auth=token_auth):
    """Test case from cell 27"""
    await domo_config.get_is_left_nav_enabled()


async def test_cell_28(token_auth=token_auth):
    """Test case from cell 28"""
    await domo_config.get_is_left_nav_enabled()
