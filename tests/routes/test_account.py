"""
Test file generated from account.ipynb
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


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    providers = (await get_available_data_providers(auth = token_auth)).response

    print(f"there are {len(providers)} available ")
    pd.DataFrame(providers)[0:5]


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    pd.DataFrame((await get_accounts(auth=token_auth)).response[0:5])


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    pd.DataFrame((await get_oauth_accounts(auth=token_auth, debug_api=False)).response[0:5])


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    (await get_account_by_id(auth=token_auth, account_id=71)).response


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    oauth_account_id = 1

    (
        await get_oauth_account_by_id(
            auth=token_auth,
            account_id=oauth_account_id,
        )
    ).response


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    account_id = 145

    (await get_account_config(
        auth=token_auth,
        account_id=account_id,
        debug_api=False,
        return_raw=False,
        is_unmask = True,
    )).response


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    oauth_account_id = 1

    res = await get_oauth_account_by_id(
        auth=token_auth,
        account_id=oauth_account_id,
        debug_api=False,
    )

    data_provider_type = res.response["dataProviderType"]

    (
        await get_oauth_account_config(
            auth=token_auth,
            account_id=oauth_account_id,
            data_provider_type=data_provider_type,
        )
    ).response


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    create_body = {
        "name": "test_api",
        "displayName": "test_dl",
        "dataProviderType": "snowflake-oauth-config",
        "origin": "OAUTH_CONFIGURATION",
        "configurations": {"client-id": "777", "client-secret": "777"},
    }

    res = await create_oauth_account(auth=token_auth, create_body=create_body)
    res


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    await delete_oauth_account(
        account_id = res.response['id'],
        auth = token_auth
    )


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    try:
        print((await update_account_config(
            auth=token_auth,
            account_id=71,
            config_body={"credentials": "abc123"},
            debug_api=False,
        )).response)

    except Exception as e:
        print(e)


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    try:
        print((await update_oauth_account_config(
            auth=token_auth,
            account_id=5,
            config_body={"client_id": str(dt.datetime.now().strftime('%Y-%m-%d-%H%M'))},
            debug_api=False,
        )).response)

    except Exception as e:
        print(e)


async def test_cell_13(token_auth=token_auth):
    """Test case from cell 13"""
    try:
        print((await update_account_name(
            auth=token_auth,
            account_id=71,
            account_name=f"domolibrary test account - updated {dt.date.today()}",
            debug_api=False,
        )).response)

    except Exception as e:
        print(e)


async def test_cell_14(token_auth=token_auth):
    """Test case from cell 14"""
    try:
        print((await update_oauth_account_name(
            auth=token_auth,
            account_id=5,
            account_name=f"domolibrary test account - updated {dt.date.today()}",
            debug_api=False,
        )).response)

    except Exception as e:
        print(e)


async def test_cell_15(token_auth=token_auth):
    """Test case from cell 15"""
    pd.DataFrame((await get_account_accesslist(auth=token_auth, account_id=71)).response)


async def test_cell_16(token_auth=token_auth):
    """Test case from cell 16"""
    pd.DataFrame((await get_oauth_account_accesslist(auth=token_auth, account_id=5, return_raw = False)).response)


async def test_cell_17(token_auth=token_auth):
    """Test case from cell 17"""
    ShareAccount_AccessLevel.NO_ACCESS


async def test_cell_18(token_auth=token_auth):
    """Test case from cell 18"""
    user_id = 929336557

    share_payloads = [
        ShareAccount_AccessLevel.CAN_VIEW.generate_payload(user_id=user_id),
        ShareAccount_AccessLevel.NO_ACCESS.generate_payload(user_id=user_id),
    ]

    account_id = 5

    for payload in share_payloads:
        print((await share_oauth_account(
            auth=token_auth,
            account_id=account_id,
            share_payload=payload,
            debug_api=False,
        )).response)
