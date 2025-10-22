"""
Test file generated from 50_DomoAccount_Default_Config.ipynb
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
    try:
        dc = DomoAccount_NoConfig_OAuth._from_dict(obj = {}, 
                                            data_provider_type='abc',
                                            parent = {}
                                            )

        dc

    except dmde.DomoError as e:
        print(e)


async def test_cell_2(token_auth=token_auth):
    """Test case from cell 2"""
    try:
        dnc = DomoAccount_NoConfig._from_dict(
            parent = None,
            obj = {},
            data_provider_type= 'ABC'
        )

        dnc

    except dmde.DomoError as e: 
        print(e)


async def test_cell_3(token_auth=token_auth):
    """Test case from cell 3"""
    dc = DomoAccount_Config_AbstractCredential._from_dict(
        obj={"credentials": "hello world", "allowExternalUse": False}
    )
    dc


async def test_cell_4(token_auth=token_auth):
    """Test case from cell 4"""
    dc.to_dict()


async def test_cell_5(token_auth=token_auth):
    """Test case from cell 5"""
    ts = DomoAccount_Config_DatasetCopy._from_dict(
        domo_instance='domo',
        obj =  {"accessToken" : '123', 'allowExternalUse' : False}
    )
    ts


async def test_cell_6(token_auth=token_auth):
    """Test case from cell 6"""
    ts.to_dict()


async def test_cell_7(token_auth=token_auth):
    """Test case from cell 7"""
    DomoAccount_Config_DomoAccessToken._from_dict(
        domo_instance='domo',
        obj =  {"domoAccessToken" : '123', 'username' : 'jae'}
    )


async def test_cell_8(token_auth=token_auth):
    """Test case from cell 8"""
    DomoAccount_Config_Governance._from_dict(domo_instance="domo", obj={"apikey": 123})


async def test_cell_9(token_auth=token_auth):
    """Test case from cell 9"""
    DomoAccount_Config_AmazonS3._from_dict(
        obj = {"access_key" : 'abc'}
    )


async def test_cell_10(token_auth=token_auth):
    """Test case from cell 10"""
    DomoAccount_Config_AwsAthena._from_dict(
        obj = {'abc' : 'abc'}
    )


async def test_cell_11(token_auth=token_auth):
    """Test case from cell 11"""
    DomoAccount_Config_AmazonS3._from_dict(
        obj = {'abc' : 'abc'}
    )


async def test_cell_12(token_auth=token_auth):
    """Test case from cell 12"""
    DomoAccount_Config_Snowflake._from_dict(
        obj = {"account": "abc", "username": "doge", "password": "test_me", "role": None}
    )


async def test_cell_13(token_auth=token_auth):
    """Test case from cell 13"""
    DomoAccount_Config_SnowflakeUnload_V2._from_dict(
        obj = {"account": "abc", "username": "doge", "password": "test_me", "role": None}
    )


async def test_cell_14(token_auth=token_auth):
    """Test case from cell 14"""
    DomoAccount_Config_SnowflakeUnloadAdvancedPartition._from_dict(
        obj = {"account": "abc", "username": "doge", "password": "test_me", "role": None}
    )


async def test_cell_15(token_auth=token_auth):
    """Test case from cell 15"""
    [member.name for member in AccountConfig]


async def test_cell_16(token_auth=token_auth):
    """Test case from cell 16"""
    domo_config = AccountConfig("ABSTRACT-CREDENTIAL-STORE").value
    domo_config._from_dict( 
        obj = {"credentials" : "abc123"})


async def test_cell_17(token_auth=token_auth):
    """Test case from cell 17"""
    AccountConfig("google-spreadsheets").value


async def test_cell_18(token_auth=token_auth):
    """Test case from cell 18"""
    AccountConfig("abc").value
