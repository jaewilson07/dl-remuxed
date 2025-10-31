# Type Hints Implementation Guide

This guide provides specific suggestions for adding type hints to your codebase.

## Classes Directory

### CodeEngineManifest.py

**Line 116: `CodeEngineManifest.from_api`**

Parameter type hints:
- `obj: Any`

Return type: `None`

**Suggested signature:**
```python
def from_api(
    self,
    obj: Any,
) -> None:
    pass
```

**Line 132: `CodeEngineManifest.download_source_code`**

Return type: `bytes`

**Suggested signature:**
```python
def download_source_code(
    self,
) -> bytes:
    pass
```


### CodeEngineManifest_Argument.py

**Add these imports:**
```python
from typing import Optional
```

**Line 51: `extract_ast_arg_name`**

Return type: `None`

**Suggested signature:**
```python
def extract_ast_arg_name(
) -> None:
    pass
```

**Line 55: `extract_ast_arg_default_value`**

Parameter type hints:
- `arg: Any`

**Suggested signature:**
```python
def extract_ast_arg_default_value(
    arg: Any,
) -> None:
    pass
```

**Line 106: `PythonTypeToSchemaType.code_engine_schema_type`**

Return type: `None`

**Suggested signature:**
```python
def code_engine_schema_type(
    self,
) -> None:
    pass
```

**Line 126: `PythonTypeToSchemaType.get`**

Parameter type hints:
- `type_str: Any`
- `default: Any`

Return type: `None`

**Suggested signature:**
```python
def get(
    self,
    type_str: Any,
    default: Any,
) -> None:
    pass
```

**Line 136: `PythonTypeToSchemaType.map_python_type_to_schema`**

Parameter type hints:
- `default: Any`

**Suggested signature:**
```python
def map_python_type_to_schema(
    self,
    default: Any,
) -> None:
    pass
```

**Line 276: `extract_last_return_node_from_ast_fn`**

Return type: `None`

**Suggested signature:**
```python
def extract_last_return_node_from_ast_fn(
) -> None:
    pass
```

**Line 283: `extract_return_variable_name`**

Return type: `None`

**Suggested signature:**
```python
def extract_return_variable_name(
) -> None:
    pass
```

**Line 310: `CodeEngineManifest_Argument.process_has_default_value`**

Return type: `None`

**Suggested signature:**
```python
def process_has_default_value(
    self,
) -> None:
    pass
```

**Line 317: `CodeEngineManifest_Argument.from_ast_arg`**

Return type: `None`

**Suggested signature:**
```python
def from_ast_arg(
    self,
) -> None:
    pass
```

**Line 330: `CodeEngineManifest_Argument.process_display_name`**

Parameter type hints:
- `display_name: str`

Return type: `None`

**Suggested signature:**
```python
def process_display_name(
    self,
    display_name: str,
) -> None:
    pass
```

**Line 348: `CodeEngineManifest_Argument.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 365: `CodeEngineManifest_Argument.from_ast_function_return_arg`**

Return type: `None`

**Suggested signature:**
```python
def from_ast_function_return_arg(
    self,
) -> None:
    pass
```


### CodeEngineManifest_Function.py

**Line 113: `CodeEngineManifest_Function.from_ast_function_def`**

Parameter type hints:
- `original_module_string: Any`

**Suggested signature:**
```python
def from_ast_function_def(
    self,
    original_module_string: Any,
) -> None:
    pass
```

**Line 204: `CodeEngineManifest_Function.validate_json_to_manifest`**

Parameter type hints:
- `test_obj: Any`
- `is_suppress_none: bool`

**Suggested signature:**
```python
def validate_json_to_manifest(
    self,
    test_obj: Any,
    is_suppress_none: bool,
) -> None:
    pass
```

**Line 228: `CodeEngineManifest_Function.download_source_code`**

Parameter type hints:
- `file_name: str`

Return type: `bytes`

**Suggested signature:**
```python
def download_source_code(
    self,
    file_name: str,
) -> bytes:
    pass
```


### DomoAccess.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 62: `DomoAccess.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```

**Line 67: `DomoAccess.get_all_users`**

Return type: `Optional[DomoAccess]`

**Suggested signature:**
```python
async def get_all_users(
    self,
) -> Optional[DomoAccess]:
    pass
```

**Line 101: `DomoAccess.share`**

Parameter type hints:
- `user_id: str`
- `group_id: str`
- `domo_group: Any`
- `domo_user: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share(
    self,
    user_id: str,
    group_id: str,
    domo_group: Any,
    domo_user: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 140: `DomoAccess.upsert_share`**

Parameter type hints:
- `user_id: str`
- `group_id: str`
- `domo_group: Any`
- `domo_user: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_share(
    self,
    user_id: str,
    group_id: str,
    domo_group: Any,
    domo_user: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 198: `DomoAccess_Account.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoAccess_Account, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoAccess_Account, ResponseGetData, None]:
    pass
```

**Line 246: `DomoAccess_OAuth.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoAccess_OAuth, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoAccess_OAuth, ResponseGetData, None]:
    pass
```


### DomoAccessToken.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 33: `DomoAccessToken.days_till_expiration`**

Return type: `None`

**Suggested signature:**
```python
def days_till_expiration(
    self,
) -> None:
    pass
```

**Line 37: `DomoAccessToken.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 61: `DomoAccessToken.get_by_id`**

Return type: `Optional[DomoAccessToken]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoAccessToken]:
    pass
```

**Line 86: `DomoAccessToken.generate`**

Parameter type hints:
- `owner: Any`

Return type: `Union[DomoAccessToken, ResponseGetData, None]`

**Suggested signature:**
```python
async def generate(
    self,
    owner: Any,
) -> Union[DomoAccessToken, ResponseGetData, None]:
    pass
```

**Line 114: `DomoAccessToken.revoke`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def revoke(
    self,
) -> ResponseGetData:
    pass
```

**Line 129: `DomoAccessToken.regenerate`**

Return type: `Union[DomoAccessToken, ResponseGetData, None]`

**Suggested signature:**
```python
async def regenerate(
    self,
) -> Union[DomoAccessToken, ResponseGetData, None]:
    pass
```

**Line 168: `DomoAccessTokens.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoAcceToken, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoAcceToken, ResponseGetData, None]:
    pass
```

**Line 194: `DomoAccessTokens.generate`**

Parameter type hints:
- `owner: Any`

Return type: `Union[DomoAcceToken, ResponseGetData, None]`

**Suggested signature:**
```python
async def generate(
    self,
    owner: Any,
) -> Union[DomoAcceToken, ResponseGetData, None]:
    pass
```


### DomoAccount.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 71: `DomoAccounts.get_accounts_accountsapi`**

Return type: `Optional[DomoAccounts]`

**Suggested signature:**
```python
async def get_accounts_accountsapi(
    self,
) -> Optional[DomoAccounts]:
    pass
```

**Line 109: `DomoAccounts.get_accounts_queryapi`**

Parameter type hints:
- `additional_filters_ls: list[str]`

Return type: `Optional[DomoAccounts]`

**Suggested signature:**
```python
async def get_accounts_queryapi(
    self,
    additional_filters_ls: list[str],
) -> Optional[DomoAccounts]:
    pass
```

**Line 148: `DomoAccounts.get`**

Return type: `Union[DomoAccount, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoAccount, ResponseGetData, None]:
    pass
```

**Line 185: `get_oauths`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_oauths(
) -> Optional[Any]:
    pass
```

**Line 214: `upsert_account`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def upsert_account(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 314: `upsert_target_account`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_target_account(
) -> ResponseGetData:
    pass
```


### DomoAccount_Config.py

**Line 58: `DomoAccount_Config.extract_allow_external_use_from_raw`**

Return type: `None`

**Suggested signature:**
```python
def extract_allow_external_use_from_raw(
    self,
) -> None:
    pass
```

**Line 78: `DomoAccount_Config.to_dict`**

Parameter type hints:
- `obj: Any`

**Suggested signature:**
```python
def to_dict(
    self,
    obj: Any,
) -> None:
    pass
```

**Line 114: `DomoAccount_NoConfig_OAuth.raise_exception`**

Return type: `None`

**Suggested signature:**
```python
def raise_exception(
    self,
) -> None:
    pass
```

**Line 138: `DomoAccount_NoConfig.raise_exception`**

Return type: `None`

**Suggested signature:**
```python
def raise_exception(
    self,
) -> None:
    pass
```

**Line 159: `DomoAccount_Config_AbstractCredential.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 182: `DomoAccount_Config_DatasetCopy.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 210: `DomoAccount_Config_DomoAccessToken.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 238: `DomoAccount_Config_Governance.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 267: `DomoAccount_Config_AmazonS3.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 308: `DomoAccount_Config_AmazonS3Advanced.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 352: `DomoAccount_Config_AwsAthena.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 392: `DomoAccount_Config_HighBandwidthConnector.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 429: `DomoAccount_Config_Snowflake.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 475: `DomoAccount_Config_SnowflakeUnload_V2.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 511: `DomoAccount_Config_SnowflakeUnloadAdvancedPartition.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 545: `DomoAccount_Config_SnowflakeWriteback.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 582: `DomoAccount_Config_SnowflakeUnload.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 620: `DomoAccount_Config_SnowflakeFederated.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 654: `DomoAccount_Config_SnowflakeInternalUnload.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 688: `DomoAccount_Config_SnowflakeKeyPairAuthentication.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 702: `generate_alt_search_str`**

Parameter type hints:
- `raw_value: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_alt_search_str(
    raw_value: Any,
) -> None:
    pass
```


### DomoAccount_Credential.py

**Line 117: `DomoAccount_Credential.set_password`**

Return type: `bool`

**Suggested signature:**
```python
def set_password(
    self,
) -> bool:
    pass
```

**Line 121: `DomoAccount_Credential.set_username`**

Return type: `bool`

**Suggested signature:**
```python
def set_username(
    self,
) -> bool:
    pass
```

**Line 125: `DomoAccount_Credential.set_access_token`**

Return type: `bool`

**Suggested signature:**
```python
def set_access_token(
    self,
) -> bool:
    pass
```

**Line 129: `DomoAccount_Credential.test_full_auth`**

Return type: `bool`

**Suggested signature:**
```python
async def test_full_auth(
    self,
) -> bool:
    pass
```

**Line 164: `DomoAccount_Credential.test_token_auth`**

Return type: `bool`

**Suggested signature:**
```python
async def test_token_auth(
    self,
) -> bool:
    pass
```

**Line 223: `DomoAccount_Credential.test_auths`**

Return type: `bool`

**Suggested signature:**
```python
async def test_auths(
    self,
) -> bool:
    pass
```

**Line 252: `DomoAccount_Credential.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 263: `get_target_user`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_target_user(
) -> Optional[Any]:
    pass
```

**Line 297: `update_target_user_password`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_target_user_password(
) -> ResponseGetData:
    pass
```

**Line 338: `get_target_access_token`**

Parameter type hints:
- `token_name: str`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_target_access_token(
    token_name: str,
) -> Optional[Any]:
    pass
```

**Line 385: `regenerate_target_access_token`**

Parameter type hints:
- `token_name: str`
- `duration_in_days: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def regenerate_target_access_token(
    token_name: str,
    duration_in_days: Any,
) -> ResponseGetData:
    pass
```


### DomoAccount_Default.py

**Add these imports:**
```python
from typing import Optional
```

**Line 81: `DomoAccount_Default.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 190: `DomoAccount_Default.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `is_use_default_account_class: bool`
- `is_unmask: bool`

Return type: `Optional[DomoAccount_Default]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
    is_use_default_account_class: bool,
    is_unmask: bool,
) -> Optional[DomoAccount_Default]:
    pass
```

**Line 239: `DomoAccount_Default.get_entity_by_id`**

Parameter type hints:
- `entity_id: str`

Return type: `Optional[DomoAccount_Default]`

**Suggested signature:**
```python
async def get_entity_by_id(
    self,
    entity_id: str,
) -> Optional[DomoAccount_Default]:
    pass
```

**Line 245: `create_account`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def create_account(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 276: `update_name`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_name(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 308: `delete_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_account(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 339: `update_config`**

Parameter type hints:
- `is_suppress_no_config: bool`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_config(
    is_suppress_no_config: bool,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```


### DomoAccount_OAuth.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 24: `generate_alt_search_str`**

Parameter type hints:
- `raw_value: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_alt_search_str(
    raw_value: Any,
) -> None:
    pass
```

**Line 45: `DomoAccountOAuth_Config_SnowflakeOauth.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 66: `DomoAccountOAuth_Config_JiraOnPremOauth.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 158: `DomoAccount_OAuth.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoAccount_OAuth]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoAccount_OAuth]:
    pass
```

**Line 202: `DomoAccount_OAuth.create`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `DomoAccount_OAuth`

**Suggested signature:**
```python
async def create(
    self,
    debug_num_stacks_to_drop: int,
) -> DomoAccount_OAuth:
    pass
```

**Line 231: `DomoAccount_OAuth.delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 246: `DomoAccount_OAuth.update_name`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_name(
    self,
) -> ResponseGetData:
    pass
```

**Line 266: `DomoAccount_OAuth.update_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_config(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### DomoActivityLog.py

**Line 101: `DomoActivityLog.get_activity_log`**

Return type: `Optional[DomoActivityLog]`

**Suggested signature:**
```python
async def get_activity_log(
    self,
) -> Optional[DomoActivityLog]:
    pass
```


### DomoAllowlist.py

**Add these imports:**
```python
from typing import Optional
```

**Line 13: `validate_ip_or_cidr`**

Return type: `bool`

**Suggested signature:**
```python
def validate_ip_or_cidr(
) -> bool:
    pass
```

**Line 33: `DomoAllowlist.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 60: `DomoAllowlist.set`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### DomoAppDb.py

**Add these imports:**
```python
from typing import Optional
```

**Line 18: `to_dict`**

Parameter type hints:
- `value: Any`

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    value: Any,
) -> None:
    pass
```

**Line 50: `AppDbDocument.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 131: `AppDbDocument.from_json`**

Return type: `None`

**Suggested signature:**
```python
def from_json(
    self,
) -> None:
    pass
```

**Line 146: `AppDbDocument.update_config`**

Return type: `None`

**Suggested signature:**
```python
def update_config(
    self,
) -> None:
    pass
```

**Line 155: `AppDbDocument.get_by_id`**

Parameter type hints:
- `identity_columns: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[AppDbDocument]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    identity_columns: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[AppDbDocument]:
    pass
```

**Line 187: `create_document`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def create_document(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 216: `update_document`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_document(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 267: `AppDbCollection.get_by_id`**

Parameter type hints:
- `collection_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[AppDbCollection]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    collection_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[AppDbCollection]:
    pass
```

**Line 299: `share_collection`**

Parameter type hints:
- `domo_user: Any`
- `domo_group: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_collection(
    domo_user: Any,
    domo_group: Any,
) -> ResponseGetData:
    pass
```

**Line 323: `query_documents`**

Parameter type hints:
- `try_auto_share: Any`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def query_documents(
    try_auto_share: Any,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 375: `upsert`**

Parameter type hints:
- `collection_id: str`
- `debug_api: bool`
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def upsert(
    collection_id: str,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 419: `AppDbCollections.get_collections`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[AppDbCollections]`

**Suggested signature:**
```python
async def get_collections(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[AppDbCollections]:
    pass
```


### DomoAppStudio.py

**Add these imports:**
```python
from typing import Optional
```

**Line 53: `DomoAppStudio.get_by_id`**

Return type: `Optional[DomoAppStudio]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoAppStudio]:
    pass
```

**Line 81: `DomoAppStudio.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 157: `DomoAppStudios.get_appstudios`**

Parameter type hints:
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoAppStudios]`

**Suggested signature:**
```python
async def get_appstudios(
    self,
    auth: dmda.DomoAuth,
) -> Optional[DomoAppStudios]:
    pass
```

**Line 197: `get_accesslist`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_accesslist(
) -> Optional[Any]:
    pass
```

**Line 255: `share`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share(
) -> ResponseGetData:
    pass
```

**Line 284: `add_appstudio_owner`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_appstudio_owner(
) -> ResponseGetData:
    pass
```


### DomoApplication.py

**Line 33: `DomoJob_Types.get_from_api_name`**

Parameter type hints:
- `api_name: str`

Return type: `Optional[DomoJob_Types]`

**Suggested signature:**
```python
def get_from_api_name(
    self,
    api_name: str,
) -> Optional[DomoJob_Types]:
    pass
```

**Line 78: `get_by_id`**

Parameter type hints:
- `application_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_id(
    application_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 102: `get_jobs`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_jobs(
) -> Optional[Any]:
    pass
```


### DomoApplication_Job_Base.py

**Line 48: `DomoTrigger_Schedule.to_obj`**

Return type: `None`

**Suggested signature:**
```python
def to_obj(
    self,
) -> None:
    pass
```

**Line 51: `DomoTrigger_Schedule.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 201: `get_by_id`**

Parameter type hints:
- `application_id: str`
- `job_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_id(
    application_id: str,
    job_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 257: `to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
) -> None:
    pass
```


### DomoApplication_Job_RemoteDomoStats.py

**Line 28: `RemoteDomoStats_Config_Policy.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 65: `RemoteDomoStats_Config.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 98: `DomoJob_RemoteDomoStats.get_by_id`**

Parameter type hints:
- `application_id: str`
- `job_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoJob_RemoteDomoStats]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    application_id: str,
    job_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoJob_RemoteDomoStats]:
    pass
```

**Line 121: `DomoJob_RemoteDomoStats.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 137: `create`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```


### DomoApplication_Job_Watchdog.py

**Line 50: `Watchdog_Config.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 68: `Watchdog_Config_MaxIndexingTime.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 86: `Watchdog_Config__Variance.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 110: `Watchdog_Config_ErrorDetection.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 126: `Watchdog_Config_LastDataUpdated.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 146: `Watchdog_Config_CustomQuery.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 203: `DomoJob_Watchdog.get_by_id`**

Parameter type hints:
- `application_id: str`
- `job_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoJob_Watchdog]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    application_id: str,
    job_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoJob_Watchdog]:
    pass
```

**Line 226: `DomoJob_Watchdog.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 242: `update`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 264: `execute`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def execute(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 285: `create`**

Parameter type hints:
- `execution_timeout: Optional[dt.datetime]`
- `remote_instance: Any`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    execution_timeout: Optional[dt.datetime] = None,
    remote_instance: Any,
) -> Any:
    pass
```


### DomoBootstrap.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 49: `DomoBootstrap.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoBootstrap, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoBootstrap, ResponseGetData, None]:
    pass
```

**Line 75: `get_customer_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_customer_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 100: `get_pages`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_pages(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 134: `get_features`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_features(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 162: `is_feature_accountsv2_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `bool`

**Suggested signature:**
```python
async def is_feature_accountsv2_enabled(
    debug_num_stacks_to_drop: int,
) -> bool:
    pass
```


### DomoCard.py

**Add these imports:**
```python
from typing import Optional
```

**Line 101: `DomoCard.get_by_id`**

Return type: `Optional[DomoCard]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoCard]:
    pass
```

**Line 146: `get_datasets`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_datasets(
) -> Optional[Any]:
    pass
```

**Line 181: `share`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share(
) -> ResponseGetData:
    pass
```

**Line 217: `get_collections`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_collections(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 247: `get_source_code`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_source_code(
) -> Optional[Any]:
    pass
```

**Line 285: `download_source_code`**

Parameter type hints:
- `download_folder: Any`
- `file_name: str`

Return type: `bytes`

**Suggested signature:**
```python
async def download_source_code(
    download_folder: Any,
    file_name: str,
) -> bytes:
    pass
```


### DomoCodeEngine.py

**Add these imports:**
```python
from typing import Optional
```

**Line 185: `DomoCodeEngine_PackageVersion.get_by_id_and_version`**

Parameter type hints:
- `package_id: str`
- `version: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoCodeEngine_PackageVersion]`

**Suggested signature:**
```python
async def get_by_id_and_version(
    self,
    package_id: str,
    version: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoCodeEngine_PackageVersion]:
    pass
```

**Line 226: `DomoCodeEngine_PackageVersion.download_source_code`**

Return type: `bytes`

**Suggested signature:**
```python
async def download_source_code(
    self,
) -> bytes:
    pass
```

**Line 267: `export`**

Return type: `None`

**Suggested signature:**
```python
def export(
) -> None:
    pass
```

**Line 322: `DomoCodeEngine_Package.from_packages_api`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `None`

**Suggested signature:**
```python
def from_packages_api(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> None:
    pass
```

**Line 348: `DomoCodeEngine_Package.get_by_id`**

Parameter type hints:
- `package_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoCodeEngine_Package]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    package_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoCodeEngine_Package]:
    pass
```

**Line 382: `get_current_version_by_id`**

Parameter type hints:
- `package_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_current_version_by_id(
    package_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```


### DomoDatacenter.py

**Add these imports:**
```python
from typing import Optional
```

**Line 27: `search_datacenter`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def search_datacenter(
    search_text: Any,
    additional_filters_ls: list[str],
) -> None:
    pass
```

**Line 58: `search_datasets`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def search_datasets(
    search_text: Any,
    additional_filters_ls: list[str],
) -> None:
    pass
```

**Line 98: `get_accounts`**

Parameter type hints:
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def get_accounts(
    additional_filters_ls: list[str],
) -> None:
    pass
```

**Line 153: `search_cards`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def search_cards(
    search_text: Any,
    additional_filters_ls: list[str],
) -> None:
    pass
```

**Line 198: `get_cards_admin_summary`**

Parameter type hints:
- `auth: dmda.DomoAuth`

**Suggested signature:**
```python
async def get_cards_admin_summary(
    auth: dmda.DomoAuth,
) -> None:
    pass
```

**Line 247: `search_codeengine`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def search_codeengine(
    search_text: Any,
    additional_filters_ls: list[str],
) -> None:
    pass
```


### DomoDataflow.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 79: `DomoDataflow.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 83: `DomoDataflow.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `id: Any`

Return type: `Optional[DomoDataflow]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
    id: Any,
) -> Optional[DomoDataflow]:
    pass
```

**Line 119: `get_definition`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_definition(
) -> Optional[Any]:
    pass
```

**Line 147: `update_dataflow_definition`**

Parameter type hints:
- `new_dataflow_definition: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_dataflow_definition(
    new_dataflow_definition: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 167: `get_jupyter_config`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_jupyter_config(
) -> Optional[Any]:
    pass
```

**Line 200: `execute`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def execute(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 216: `get_by_version_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_version_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 250: `get_versions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_versions(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 294: `DomoDataflows.get`**

Return type: `Union[DomoDataflow, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoDataflow, ResponseGetData, None]:
    pass
```


### DomoDataflow_Action.py

**Line 68: `get_parents`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
def get_parents(
) -> Optional[Any]:
    pass
```


### DomoDataflow_History.py

**Add these imports:**
```python
from typing import Optional
```

**Line 81: `get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 110: `get_actions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_actions(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 154: `get_execution_history`**

Parameter type hints:
- `maximum: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_execution_history(
    maximum: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```


### DomoDataset.py

**Line 95: `DomoDataset_Default.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 149: `DomoDataset_Default.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoDataset_Default]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoDataset_Default]:
    pass
```

**Line 189: `query_dataset_private`**

Parameter type hints:
- `limit: Any`
- `skip: Any`
- `maximum: Any`
- `timeout: Optional[dt.datetime]`

**Suggested signature:**
```python
async def query_dataset_private(
    limit: Any,
    skip: Any,
    maximum: Any,
    timeout: Optional[dt.datetime] = None,
) -> None:
    pass
```

**Line 252: `delete`**

Parameter type hints:
- `dataset_id: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    dataset_id: str,
) -> ResponseGetData:
    pass
```

**Line 271: `share`**

Parameter type hints:
- `member: Any`
- `is_send_email: bool`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share(
    member: Any,
    is_send_email: bool,
) -> ResponseGetData:
    pass
```

**Line 301: `index_dataset`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def index_dataset(
) -> ResponseGetData:
    pass
```

**Line 317: `upload_data`**

Parameter type hints:
- `dataset_upload_id: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upload_data(
    dataset_upload_id: str,
) -> ResponseGetData:
    pass
```

**Line 445: `list_partitions`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def list_partitions(
) -> ResponseGetData:
    pass
```

**Line 466: `create`**

Parameter type hints:
- `dataset_type: Any`
- `schema: Any`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    dataset_type: Any,
    schema: Any,
) -> Any:
    pass
```

**Line 501: `delete_partition`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def delete_partition(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 572: `reset_dataset`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def reset_dataset(
) -> ResponseGetData:
    pass
```

**Line 632: `upsert_connector`**

Parameter type hints:
- `cnfg_body: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_connector(
    cnfg_body: Any,
) -> ResponseGetData:
    pass
```

**Line 680: `FederatedDomoDataset.get_federated_parent`**

Return type: `Optional[FederatedDomoDataset]`

**Suggested signature:**
```python
async def get_federated_parent(
    self,
) -> Optional[FederatedDomoDataset]:
    pass
```

**Line 688: `FederatedDomoDataset.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[FederatedDomoDataset]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[FederatedDomoDataset]:
    pass
```

**Line 726: `DomoPublishDataset.get_subscription`**

Return type: `Optional[DomoPublishDataset]`

**Suggested signature:**
```python
async def get_subscription(
    self,
) -> Optional[DomoPublishDataset]:
    pass
```

**Line 729: `DomoPublishDataset.get_parent_publication`**

Return type: `Optional[DomoPublishDataset]`

**Suggested signature:**
```python
async def get_parent_publication(
    self,
) -> Optional[DomoPublishDataset]:
    pass
```


### DomoDataset_Connector.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 53: `DomoConnectors.get`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoConnector, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    search_text: Any,
    additional_filters_ls: list[str],
    debug_num_stacks_to_drop: int,
) -> Union[DomoConnector, ResponseGetData, None]:
    pass
```


### DomoDataset_PDP.py

**Line 34: `generate_parameter_simple`**

Parameter type hints:
- `obj: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_parameter_simple(
    obj: Any,
) -> None:
    pass
```

**Line 46: `generate_body_from_parameter`**

Return type: `None`

**Suggested signature:**
```python
def generate_body_from_parameter(
) -> None:
    pass
```

**Line 107: `PDP_Policy.upsert_policy`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_policy(
    self,
) -> ResponseGetData:
    pass
```

**Line 143: `generate_body_from_policy`**

Return type: `None`

**Suggested signature:**
```python
def generate_body_from_policy(
) -> None:
    pass
```

**Line 178: `get_policies`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_policies(
) -> Optional[Any]:
    pass
```

**Line 226: `search_pdp_policies`**

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
async def search_pdp_policies(
) -> Union[Any, list[Any], None]:
    pass
```

**Line 291: `delete_policy`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_policy(
) -> ResponseGetData:
    pass
```

**Line 310: `toggle_dataset_pdp`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_dataset_pdp(
) -> ResponseGetData:
    pass
```


### DomoDataset_Schema.py

**Line 45: `DomoDataset_Schema_Column.replace_tag`**

Parameter type hints:
- `tag_prefix: Any`
- `new_tag: Any`

Return type: `bool`

**Suggested signature:**
```python
def replace_tag(
    self,
    tag_prefix: Any,
    new_tag: Any,
) -> bool:
    pass
```

**Line 68: `DomoDataset_Schema_Column.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 102: `DomoDataset_Schema.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 173: `reset_col_order`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def reset_col_order(
) -> ResponseGetData:
    pass
```

**Line 190: `add_col`**

Return type: `None`

**Suggested signature:**
```python
def add_col(
) -> None:
    pass
```

**Line 206: `remove_col`**

Return type: `None`

**Suggested signature:**
```python
def remove_col(
) -> None:
    pass
```

**Line 233: `alter_schema`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def alter_schema(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 262: `alter_schema_descriptions`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def alter_schema_descriptions(
) -> Union[Any, ResponseGetData, None]:
    pass
```


### DomoDataset_Stream.py

**Line 217: `StreamConfig_Mappings.search`**

Parameter type hints:
- `value: Any`

**Suggested signature:**
```python
def search(
    self,
    value: Any,
) -> None:
    pass
```

**Line 249: `StreamConfig.process_sql`**

Return type: `None`

**Suggested signature:**
```python
def process_sql(
    self,
) -> None:
    pass
```

**Line 268: `StreamConfig.from_json`**

Return type: `None`

**Suggested signature:**
```python
def from_json(
    self,
) -> None:
    pass
```

**Line 289: `StreamConfig.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 363: `DomoStream.generate_config_rpt`**

Return type: `None`

**Suggested signature:**
```python
def generate_config_rpt(
    self,
) -> None:
    pass
```

**Line 374: `DomoStream.get_stream_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoStream]`

**Suggested signature:**
```python
async def get_stream_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoStream]:
    pass
```

**Line 402: `DomoStream.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```

**Line 416: `DomoStream.create_stream`**

Parameter type hints:
- `cnfg_body: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_stream(
    self,
    cnfg_body: Any,
) -> ResponseGetData:
    pass
```

**Line 428: `DomoStream.update_stream`**

Parameter type hints:
- `cnfg_body: Any`
- `stream_id: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_stream(
    self,
    cnfg_body: Any,
    stream_id: str,
) -> ResponseGetData:
    pass
```

**Line 446: `DomoStream.upsert_connector`**

Parameter type hints:
- `cnfg_body: Any`
- `match_name: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_connector(
    self,
    cnfg_body: Any,
    match_name: str,
) -> ResponseGetData:
    pass
```


### DomoGrant.py

**Add these imports:**
```python
from typing import Union
```

**Line 54: `DomoGrants.get`**

Return type: `Union[DomoGrant, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoGrant, ResponseGetData, None]:
    pass
```


### DomoGroup.py

**Add these imports:**
```python
from typing import Optional
```

**Line 103: `DomoGroup.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 107: `DomoGroup.get_by_id`**

Return type: `Optional[DomoGroup]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoGroup]:
    pass
```

**Line 143: `create_from_name`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_from_name(
) -> ResponseGetData:
    pass
```

**Line 175: `update_metadata`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_metadata(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 227: `delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 261: `DomoGroups.get_is_system_groups_visible`**

Return type: `Optional[DomoGroups]`

**Suggested signature:**
```python
async def get_is_system_groups_visible(
    self,
) -> Optional[DomoGroups]:
    pass
```

**Line 283: `DomoGroups.toggle_show_system_groups`**

Return type: `Union[DomoGroup, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_show_system_groups(
    self,
) -> Union[DomoGroup, ResponseGetData, None]:
    pass
```

**Line 313: `get`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 401: `upsert`**

Return type: `Any`

**Suggested signature:**
```python
async def upsert(
) -> Any:
    pass
```


### DomoInstanceConfig.py

**Add these imports:**
```python
from typing import Optional
```

**Line 79: `get_applications`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_applications(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 105: `generate_applications_report`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def generate_applications_report(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 160: `set_authorized_domains`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_authorized_domains(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 181: `upsert_authorized_domains`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_authorized_domains(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 206: `get_authorized_custom_app_domains`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_authorized_custom_app_domains(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 231: `set_authorized_custom_app_domains`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_authorized_custom_app_domains(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 251: `upsert_authorized_custom_app_domains`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_authorized_custom_app_domains(
) -> ResponseGetData:
    pass
```

**Line 275: `get_sandbox_is_same_instance_promotion_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_sandbox_is_same_instance_promotion_enabled(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 300: `toggle_sandbox_allow_same_instance_promotion`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_sandbox_allow_same_instance_promotion(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 328: `get_is_user_invite_notification_enabled`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_user_invite_notification_enabled(
) -> Optional[Any]:
    pass
```

**Line 357: `toggle_is_user_invite_notification_enabled`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_user_invite_notification_enabled(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 398: `get_is_invite_social_users_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_invite_social_users_enabled(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 439: `toggle_is_invite_social_users_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_invite_social_users_enabled(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 472: `get_is_weekly_digest_enabled`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_weekly_digest_enabled(
) -> Optional[Any]:
    pass
```

**Line 498: `toggle_is_weekly_digest_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_weekly_digest_enabled(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 541: `toggle_is_left_nav_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_left_nav_enabled(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 569: `get_is_left_nav_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_left_nav_enabled(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 595: `toggle_is_left_nav_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_left_nav_enabled(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 623: `get_is_left_nav_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_left_nav_enabled(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```


### DomoInstanceConfig_ApiClient.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 38: `ApiClient.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 67: `ApiClient.get_by_id`**

Return type: `Optional[ApiClient]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[ApiClient]:
    pass
```

**Line 93: `ApiClient.revoke`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def revoke(
    self,
) -> ResponseGetData:
    pass
```

**Line 126: `ApiClients.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[ApiClient, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[ApiClient, ResponseGetData, None]:
    pass
```

**Line 155: `ApiClients.get_by_name`**

Return type: `Optional[ApiClients]`

**Suggested signature:**
```python
async def get_by_name(
    self,
) -> Optional[ApiClients]:
    pass
```

**Line 185: `create_for_authorized_user`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def create_for_authorized_user(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 220: `upsert_client`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_client(
) -> ResponseGetData:
    pass
```


### DomoInstanceConfig_InstanceSwitcher.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 41: `DomoInstanceConfig_InstanceSwitcher_Mapping.from_obj`**

Return type: `None`

**Suggested signature:**
```python
def from_obj(
    self,
) -> None:
    pass
```

**Line 47: `DomoInstanceConfig_InstanceSwitcher_Mapping.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 71: `DomoInstanceConfig_InstanceSwitcher.get_mapping`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoInstanceConfig_InstanceSwitcher]`

**Suggested signature:**
```python
async def get_mapping(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoInstanceConfig_InstanceSwitcher]:
    pass
```

**Line 98: `DomoInstanceConfig_InstanceSwitcher.set_mapping`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoInstanceConfig_InstanceSwitcher, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_mapping(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoInstanceConfig_InstanceSwitcher, ResponseGetData, None]:
    pass
```

**Line 136: `DomoInstanceConfig_InstanceSwitcher.add_mapping`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_mapping(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### DomoInstanceConfig_MFA.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 39: `MFA_Config.get_instance_config`**

Return type: `Optional[MFA_Config]`

**Suggested signature:**
```python
async def get_instance_config(
    self,
) -> Optional[MFA_Config]:
    pass
```

**Line 73: `MFA_Config.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[MFA_Config, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[MFA_Config, ResponseGetData, None]:
    pass
```

**Line 119: `toggle_mfa`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_mfa(
) -> ResponseGetData:
    pass
```

**Line 155: `enable`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def enable(
) -> ResponseGetData:
    pass
```

**Line 173: `disable`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def disable(
) -> ResponseGetData:
    pass
```

**Line 191: `set_max_code_attempts`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_max_code_attempts(
) -> ResponseGetData:
    pass
```

**Line 227: `set_num_days_valid`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_num_days_valid(
) -> ResponseGetData:
    pass
```

**Line 262: `update`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
) -> ResponseGetData:
    pass
```


### DomoInstanceConfig_SSO.py

**Add these imports:**
```python
from typing import list, Optional, Union
```

**Line 53: `SSO_Config.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 56: `SSO_Config.set_attribute`**

Return type: `None`

**Suggested signature:**
```python
def set_attribute(
    self,
) -> None:
    pass
```

**Line 114: `SSO_Config.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```

**Line 133: `SSO_Config.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 236: `SSO_OIDC_Config.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 243: `SSO_OIDC_Config.get`**

Return type: `Union[SSO_OIDC_Config, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[SSO_OIDC_Config, ResponseGetData, None]:
    pass
```

**Line 264: `SSO_OIDC_Config.update`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 323: `SSO_SAML_Config.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 330: `SSO_SAML_Config.get`**

Return type: `Union[SSO_SAML_Config, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[SSO_SAML_Config, ResponseGetData, None]:
    pass
```

**Line 353: `SSO_SAML_Config.update`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    self,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 385: `SSO.get_oidc`**

Return type: `Optional[SSO]`

**Suggested signature:**
```python
async def get_oidc(
    self,
) -> Optional[SSO]:
    pass
```

**Line 402: `SSO.get_saml`**

Return type: `Optional[SSO]`

**Suggested signature:**
```python
async def get_saml(
    self,
) -> Optional[SSO]:
    pass
```

**Line 419: `SSO.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```


### DomoInstanceConfig_Scheduler_Policies.py

**Add these imports:**
```python
from typing import Union
```

**Line 109: `DomoScheduler_Policies.get`**

Return type: `Union[DomoScheduler_Policie, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoScheduler_Policie, ResponseGetData, None]:
    pass
```

**Line 128: `DomoScheduler_Policies.upsert`**

Return type: `DomoScheduler_Policie`

**Suggested signature:**
```python
async def upsert(
    self,
) -> DomoScheduler_Policie:
    pass
```

**Line 168: `DomoScheduler_Policies.delete`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    self,
) -> ResponseGetData:
    pass
```


### DomoInstanceConfig_UserAttribute.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 44: `UserAttribute.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 65: `UserAttribute.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[UserAttribute]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[UserAttribute]:
    pass
```

**Line 89: `update`**

Parameter type hints:
- `name: Any`
- `description: Any`
- `security_voter: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    name: Any,
    description: Any,
    security_voter: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 127: `UserAttributes.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[UerAttribute, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[UerAttribute, ResponseGetData, None]:
    pass
```

**Line 158: `create`**

Parameter type hints:
- `name: Any`
- `description: Any`
- `security_voter: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    name: Any,
    description: Any,
    security_voter: Any,
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 198: `upsert`**

Parameter type hints:
- `attribute_id: str`
- `name: Any`
- `description: Any`
- `security_voter: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def upsert(
    attribute_id: str,
    name: Any,
    description: Any,
    security_voter: Any,
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 264: `delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### DomoIntegration.py

**Line 29: `CloudAmplifier_PollingSchedule.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 40: `CloudAmplifier_PollingSchedule.from_dict`**

Return type: `None`

**Suggested signature:**
```python
def from_dict(
    self,
) -> None:
    pass
```

**Line 62: `CloudAmplifier_Warehouse.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 75: `CloudAmplifier_Warehouse.from_dict`**

Return type: `None`

**Suggested signature:**
```python
def from_dict(
    self,
) -> None:
    pass
```

**Line 93: `DomoIntegration_OwnerEntity.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 97: `DomoIntegration_OwnerEntity.from_dict`**

Return type: `None`

**Suggested signature:**
```python
def from_dict(
    self,
) -> None:
    pass
```

**Line 107: `DomoIntegration_PropertyConfig.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 111: `DomoIntegration_PropertyConfig.from_dict`**

Return type: `None`

**Suggested signature:**
```python
def from_dict(
    self,
) -> None:
    pass
```

**Line 164: `DomoIntegration.from_dict`**

Return type: `None`

**Suggested signature:**
```python
def from_dict(
    self,
) -> None:
    pass
```

**Line 194: `DomoIntegration.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```


### DomoJupyter.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 112: `DomoJupyterWorkspace.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 115: `DomoJupyterWorkspace.update_auth_to_jupyter_auth`**

Return type: `None`

**Suggested signature:**
```python
def update_auth_to_jupyter_auth(
    self,
) -> None:
    pass
```

**Line 209: `DomoJupyterWorkspace.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 230: `DomoJupyterWorkspace.get_by_id`**

Parameter type hints:
- `workspace_id: str`
- `jupyter_token: Any`

Return type: `Optional[DomoJupyterWorkspace]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    workspace_id: str,
    jupyter_token: Any,
) -> Optional[DomoJupyterWorkspace]:
    pass
```

**Line 267: `get_current_workspace`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_current_workspace(
) -> Optional[Any]:
    pass
```

**Line 287: `get_account_configuration`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_account_configuration(
) -> Optional[Any]:
    pass
```

**Line 308: `get_input_configuration`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_input_configuration(
) -> Optional[Any]:
    pass
```

**Line 327: `get_output_configuration`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_output_configuration(
) -> Optional[Any]:
    pass
```

**Line 363: `add_config_input_datasource`**

Return type: `None`

**Suggested signature:**
```python
def add_config_input_datasource(
) -> None:
    pass
```

**Line 373: `add_config_output_datasource`**

Return type: `None`

**Suggested signature:**
```python
def add_config_output_datasource(
) -> None:
    pass
```

**Line 383: `add_config_account`**

Return type: `None`

**Suggested signature:**
```python
def add_config_account(
) -> None:
    pass
```

**Line 402: `DomoJupyterWorkspaces.get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoJupyterWorkpace, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoJupyterWorkpace, ResponseGetData, None]:
    pass
```

**Line 438: `DomoJupyterWorkspaces.search_workspace_by_name`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoJupyterWorkpace, list[DomoJupyterWorkpace], None]`

**Suggested signature:**
```python
async def search_workspace_by_name(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoJupyterWorkpace, list[DomoJupyterWorkpace], None]:
    pass
```

**Line 494: `update_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_config(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 521: `add_account`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def add_account(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 585: `add_input_dataset`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_input_dataset(
) -> ResponseGetData:
    pass
```

**Line 636: `add_output_dataset`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_output_dataset(
) -> ResponseGetData:
    pass
```

**Line 685: `get_content`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_content(
) -> Optional[Any]:
    pass
```

**Line 712: `download_workspace_content`**

Parameter type hints:
- `base_export_folder: Any`

**Suggested signature:**
```python
async def download_workspace_content(
    base_export_folder: Any,
) -> None:
    pass
```


### DomoJupyter_Account.py

**Add these imports:**
```python
from typing import Optional
```

**Line 35: `read_domo_jupyter_account`**

Parameter type hints:
- `account_name: str`

Return type: `None`

**Suggested signature:**
```python
def read_domo_jupyter_account(
    account_name: str,
) -> None:
    pass
```

**Line 100: `DomoJupyter_Account.get_account`**

Return type: `Optional[DomoJupyter_Account]`

**Suggested signature:**
```python
async def get_account(
    self,
) -> Optional[DomoJupyter_Account]:
    pass
```

**Line 177: `DomoJupyter_Account.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 184: `DomoJupyter_Account.to_api`**

Return type: `None`

**Suggested signature:**
```python
def to_api(
    self,
) -> None:
    pass
```

**Line 190: `DomoJupyter_Account.share_with_workspace`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_with_workspace(
    self,
) -> ResponseGetData:
    pass
```

**Line 204: `DomoJupyter_Account.read_creds`**

Return type: `None`

**Suggested signature:**
```python
def read_creds(
    self,
) -> None:
    pass
```


### DomoJupyter_Content.py

**Add these imports:**
```python
from typing import list, Optional, Union
```

**Line 56: `DomoJupyter_Content.export`**

Return type: `None`

**Suggested signature:**
```python
def export(
    self,
) -> None:
    pass
```

**Line 88: `DomoJupyter_Content.create_content`**

Parameter type hints:
- `new_content: Any`
- `folder_path: str`

Return type: `Union[DomoJupyter_Content, ResponseGetData, None]`

**Suggested signature:**
```python
async def create_content(
    self,
    new_content: Any,
    folder_path: str,
) -> Union[DomoJupyter_Content, ResponseGetData, None]:
    pass
```

**Line 120: `DomoJupyter_Content.update`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    self,
) -> ResponseGetData:
    pass
```

**Line 152: `DomoJupyter_Content.delete`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    self,
) -> ResponseGetData:
    pass
```


### DomoJupyter_DataSource.py

**Add these imports:**
```python
from typing import Optional
```

**Line 34: `DomoJupyter_DataSource.get_dataset`**

Return type: `Optional[DomoJupyter_DataSource]`

**Suggested signature:**
```python
async def get_dataset(
    self,
) -> Optional[DomoJupyter_DataSource]:
    pass
```

**Line 60: `DomoJupyter_DataSource.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 63: `DomoJupyter_DataSource.share_with_workspace_as_input_datasource`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_with_workspace_as_input_datasource(
    self,
) -> ResponseGetData:
    pass
```

**Line 77: `DomoJupyter_DataSource.share_with_workspace_as_output_datasource`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_with_workspace_as_output_datasource(
    self,
) -> ResponseGetData:
    pass
```


### DomoLineage.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 52: `DomoLineage_Link.get_entity`**

Parameter type hints:
- `entity_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineage_Link]`

**Suggested signature:**
```python
async def get_entity(
    self,
    entity_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineage_Link]:
    pass
```

**Line 61: `DomoLineage_Link.from_dict`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineage_Link]`

**Suggested signature:**
```python
async def from_dict(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineage_Link]:
    pass
```

**Line 102: `DomoLineageLink_Dataflow.get_entity`**

Parameter type hints:
- `entity_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Dataflow]`

**Suggested signature:**
```python
async def get_entity(
    self,
    entity_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Dataflow]:
    pass
```

**Line 110: `DomoLineageLink_Dataflow.from_dict`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Dataflow]`

**Suggested signature:**
```python
async def from_dict(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Dataflow]:
    pass
```

**Line 136: `DomoLineageLink_Publication.get_entity`**

Parameter type hints:
- `entity_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Publication]`

**Suggested signature:**
```python
async def get_entity(
    self,
    entity_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Publication]:
    pass
```

**Line 150: `DomoLineageLink_Publication.from_dict`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Publication]`

**Suggested signature:**
```python
async def from_dict(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Publication]:
    pass
```

**Line 171: `DomoLineageLink_Card.get_entity`**

Parameter type hints:
- `entity_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Card]`

**Suggested signature:**
```python
async def get_entity(
    self,
    entity_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Card]:
    pass
```

**Line 185: `DomoLineageLink_Card.from_dict`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Card]`

**Suggested signature:**
```python
async def from_dict(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Card]:
    pass
```

**Line 208: `DomoLineageLink_Dataset.get_entity`**

Parameter type hints:
- `entity_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Dataset]`

**Suggested signature:**
```python
async def get_entity(
    self,
    entity_id: str,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Dataset]:
    pass
```

**Line 222: `DomoLineageLink_Dataset.from_dict`**

Parameter type hints:
- `obj: Any`
- `auth: dmda.DomoAuth`

Return type: `Optional[DomoLineageLink_Dataset]`

**Suggested signature:**
```python
async def from_dict(
    self,
    obj: Any,
    auth: dmda.DomoAuth,
) -> Optional[DomoLineageLink_Dataset]:
    pass
```

**Line 286: `DomoLineage.get_parent`**

Return type: `Optional[DomoLineage]`

**Suggested signature:**
```python
async def get_parent(
    self,
) -> Optional[DomoLineage]:
    pass
```

**Line 312: `DomoLineage.get_datacenter`**

Return type: `Optional[DomoLineage]`

**Suggested signature:**
```python
async def get_datacenter(
    self,
) -> Optional[DomoLineage]:
    pass
```

**Line 403: `DomoLineage.get`**

Return type: `Union[DomoLineage, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoLineage, ResponseGetData, None]:
    pass
```

**Line 443: `DomoLineage_Page.get_cards`**

Return type: `Optional[DomoLineage_Page]`

**Suggested signature:**
```python
async def get_cards(
    self,
) -> Optional[DomoLineage_Page]:
    pass
```

**Line 463: `DomoLineage_Page.get`**

Return type: `Union[DomoLineage_Page, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoLineage_Page, ResponseGetData, None]:
    pass
```

**Line 513: `DomoLineage_Publication.get`**

Return type: `Union[DomoLineage_Publication, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoLineage_Publication, ResponseGetData, None]:
    pass
```


### DomoMembership.py

**Add these imports:**
```python
from typing import Optional
```

**Line 30: `Membership_Entity.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 56: `Membership.get_owners`**

Return type: `Optional[Membership]`

**Suggested signature:**
```python
async def get_owners(
    self,
) -> Optional[Membership]:
    pass
```

**Line 60: `Membership.get_members`**

Return type: `Optional[Membership]`

**Suggested signature:**
```python
async def get_members(
    self,
) -> Optional[Membership]:
    pass
```

**Line 64: `Membership.update`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    self,
) -> ResponseGetData:
    pass
```

**Line 183: `GroupMembership.get_owners`**

Return type: `Optional[GroupMembership]`

**Suggested signature:**
```python
async def get_owners(
    self,
) -> Optional[GroupMembership]:
    pass
```

**Line 212: `GroupMembership.update`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    self,
) -> ResponseGetData:
    pass
```

**Line 236: `GroupMembership.get_members`**

Return type: `Optional[GroupMembership]`

**Suggested signature:**
```python
async def get_members(
    self,
) -> Optional[GroupMembership]:
    pass
```

**Line 268: `add_members`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def add_members(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 298: `remove_members`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def remove_members(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 328: `set_members`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_members(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 372: `add_owners`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def add_owners(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 402: `remove_owners`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def remove_owners(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 432: `set_owners`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_owners(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 490: `add_owner_manage_all_groups_role`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_owner_manage_all_groups_role(
) -> ResponseGetData:
    pass
```


### DomoPDP.py

**Line 34: `generate_parameter_simple`**

Parameter type hints:
- `obj: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_parameter_simple(
    obj: Any,
) -> None:
    pass
```

**Line 46: `generate_body_from_parameter`**

Return type: `None`

**Suggested signature:**
```python
def generate_body_from_parameter(
) -> None:
    pass
```

**Line 107: `PDP_Policy.upsert_policy`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_policy(
    self,
) -> ResponseGetData:
    pass
```

**Line 143: `generate_body_from_policy`**

Return type: `None`

**Suggested signature:**
```python
def generate_body_from_policy(
) -> None:
    pass
```

**Line 178: `get_policies`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_policies(
) -> Optional[Any]:
    pass
```

**Line 226: `search_pdp_policies`**

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
async def search_pdp_policies(
) -> Union[Any, list[Any], None]:
    pass
```

**Line 291: `delete_policy`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_policy(
) -> ResponseGetData:
    pass
```

**Line 310: `toggle_dataset_pdp`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_dataset_pdp(
) -> ResponseGetData:
    pass
```


### DomoPage.py

**Add these imports:**
```python
from typing import Optional
```

**Line 72: `DomoPage.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 178: `DomoPage.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `id: Any`

Return type: `Optional[DomoPage]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
    id: Any,
) -> Optional[DomoPage]:
    pass
```

**Line 321: `DomoPages.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```

**Line 325: `DomoPages.get_admin_summary`**

Return type: `Optional[DomoPages]`

**Suggested signature:**
```python
async def get_admin_summary(
    self,
) -> Optional[DomoPages]:
    pass
```

**Line 362: `get_children`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_children(
) -> Optional[Any]:
    pass
```

**Line 409: `flatten_children`**

Parameter type hints:
- `path: Any`
- `hierarchy: Any`
- `results: Any`

Return type: `None`

**Suggested signature:**
```python
def flatten_children(
    path: Any,
    hierarchy: Any,
    results: Any,
) -> None:
    pass
```

**Line 426: `get_parents`**

Parameter type hints:
- `page: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_parents(
    page: Any,
) -> Optional[Any]:
    pass
```

**Line 480: `test_page_access`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `bool`

**Suggested signature:**
```python
async def test_page_access(
    debug_num_stacks_to_drop: int,
) -> bool:
    pass
```

**Line 526: `get_accesslist`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_accesslist(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 659: `share`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share(
) -> ResponseGetData:
    pass
```

**Line 690: `get_cards`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_cards(
) -> Optional[Any]:
    pass
```

**Line 720: `get_datasets`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_datasets(
) -> Optional[Any]:
    pass
```

**Line 747: `update_layout`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_layout(
) -> ResponseGetData:
    pass
```

**Line 782: `add_owner`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_owner(
) -> ResponseGetData:
    pass
```


### DomoPage_Content.py

**Add these imports:**
```python
from typing import Optional
```

**Line 30: `PageLayoutTemplate.get_body`**

Return type: `Optional[PageLayoutTemplate]`

**Suggested signature:**
```python
def get_body(
    self,
) -> Optional[PageLayoutTemplate]:
    pass
```

**Line 84: `PageLayoutBackground.get_body`**

Return type: `Optional[PageLayoutBackground]`

**Suggested signature:**
```python
def get_body(
    self,
) -> Optional[PageLayoutBackground]:
    pass
```

**Line 158: `PageLayoutContent.get_body`**

Return type: `Optional[PageLayoutContent]`

**Suggested signature:**
```python
def get_body(
    self,
) -> Optional[PageLayoutContent]:
    pass
```

**Line 279: `PageLayout.generate_new_background_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_new_background_body(
    self,
) -> None:
    pass
```

**Line 290: `PageLayout.get_body`**

Return type: `Optional[PageLayout]`

**Suggested signature:**
```python
def get_body(
    self,
) -> Optional[PageLayout]:
    pass
```


### DomoPublish.py

**Add these imports:**
```python
from typing import Union
```

**Line 92: `DomoPublication_Content.get_entity`**

Return type: `Optional[DomoPublication_Content]`

**Suggested signature:**
```python
async def get_entity(
    self,
) -> Optional[DomoPublication_Content]:
    pass
```

**Line 108: `DomoPublication_Content.to_api_json`**

Return type: `None`

**Suggested signature:**
```python
def to_api_json(
    self,
) -> None:
    pass
```

**Line 199: `DomoPublication.get_by_id`**

Parameter type hints:
- `publication_id: str`
- `timeout: Optional[dt.datetime]`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoPublication]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    publication_id: str,
    timeout: Optional[dt.datetime] = None,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoPublication]:
    pass
```

**Line 228: `DomoPublication.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 231: `DomoPublication.get_content_details`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoPublication]`

**Suggested signature:**
```python
async def get_content_details(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoPublication]:
    pass
```

**Line 290: `create_publication`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_publication(
) -> ResponseGetData:
    pass
```

**Line 335: `update_publication`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_publication(
) -> ResponseGetData:
    pass
```

**Line 414: `DomoSubscription.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 418: `DomoSubscription.get_by_id`**

Return type: `Optional[DomoSubscription]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoSubscription]:
    pass
```

**Line 439: `DomoSubscription.get_parent_publication`**

Return type: `Optional[DomoSubscription]`

**Suggested signature:**
```python
async def get_parent_publication(
    self,
) -> Optional[DomoSubscription]:
    pass
```

**Line 462: `DomoSubscription.get_content_details`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoSubscription]`

**Suggested signature:**
```python
async def get_content_details(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoSubscription]:
    pass
```

**Line 514: `get_content`**

Parameter type hints:
- `timeout: Optional[dt.datetime]`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_content(
    timeout: Optional[dt.datetime] = None,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 554: `DomoEverywhere.get_publications`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoEverywhere]`

**Suggested signature:**
```python
async def get_publications(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoEverywhere]:
    pass
```

**Line 584: `DomoEverywhere.search_publications`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoEverywhere, list[DomoEverywhere], None]`

**Suggested signature:**
```python
async def search_publications(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoEverywhere, list[DomoEverywhere], None]:
    pass
```

**Line 603: `DomoEverywhere.get_subscriptions`**

Return type: `Optional[DomoEverywhere]`

**Suggested signature:**
```python
async def get_subscriptions(
    self,
) -> Optional[DomoEverywhere]:
    pass
```

**Line 629: `DomoEverywhere.get_subscription_invitations`**

Return type: `Optional[DomoEverywhere]`

**Suggested signature:**
```python
async def get_subscription_invitations(
    self,
) -> Optional[DomoEverywhere]:
    pass
```

**Line 644: `DomoEverywhere.accept_invite_by_id`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def accept_invite_by_id(
    self,
) -> ResponseGetData:
    pass
```

**Line 665: `report_content_as_dataframe`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def report_content_as_dataframe(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 687: `report_lineage_as_dataframe`**

Return type: `None`

**Suggested signature:**
```python
def report_lineage_as_dataframe(
) -> None:
    pass
```


### DomoRole.py

**Add these imports:**
```python
from typing import Optional, Union
```

**Line 73: `DomoRole.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 77: `DomoRole.get_by_id`**

Return type: `Optional[DomoRole]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoRole]:
    pass
```

**Line 102: `get_grants`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_grants(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 140: `set_grants`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_grants(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 186: `create`**

Parameter type hints:
- `description: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    description: Any,
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 220: `get_membership`**

Parameter type hints:
- `role_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_membership(
    role_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 262: `add_user`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_user(
) -> ResponseGetData:
    pass
```

**Line 302: `update`**

Parameter type hints:
- `name: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update(
    name: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 345: `delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 363: `delete_role`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_role(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 408: `DomoRoles.get_default_role`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_default_role(
    self,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 435: `DomoRoles.get`**

Return type: `Union[DomoRole, ResponseGetData, None]`

**Suggested signature:**
```python
async def get(
    self,
) -> Union[DomoRole, ResponseGetData, None]:
    pass
```

**Line 466: `DomoRoles.search_by_name`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[DomoRole, list[DomoRole], None]`

**Suggested signature:**
```python
async def search_by_name(
    self,
    debug_num_stacks_to_drop: int,
) -> Union[DomoRole, list[DomoRole], None]:
    pass
```

**Line 496: `create`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 520: `upsert`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Any`

**Suggested signature:**
```python
async def upsert(
    debug_num_stacks_to_drop: int,
) -> Any:
    pass
```

**Line 574: `set_as_default_role`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_as_default_role(
) -> ResponseGetData:
    pass
```


### DomoSandbox.py

**Add these imports:**
```python
from typing import Optional
```

**Line 38: `DomoRepository.display_url`**

Return type: `None`

**Suggested signature:**
```python
def display_url(
    self,
) -> None:
    pass
```

**Line 60: `DomoRepository.get_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[DomoRepository]`

**Suggested signature:**
```python
async def get_by_id(
    self,
    debug_num_stacks_to_drop: int,
) -> Optional[DomoRepository]:
    pass
```

**Line 127: `DomoSandbox.get_repositories`**

Return type: `Optional[DomoSandbox]`

**Suggested signature:**
```python
async def get_repositories(
    self,
) -> Optional[DomoSandbox]:
    pass
```

**Line 141: `DomoSandbox.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```


### DomoUser.py

**Line 151: `get_role`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_role(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 171: `get_by_id`**

Parameter type hints:
- `user_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_id(
    user_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 216: `download_avatar`**

Parameter type hints:
- `folder_path: str`
- `img_name: Optional[str]`

Return type: `bytes`

**Suggested signature:**
```python
async def download_avatar(
    folder_path: str,
    img_name: Optional[str] = None,
) -> bytes:
    pass
```

**Line 257: `update_properties`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_properties(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 285: `set_user_landing_page`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_user_landing_page(
) -> ResponseGetData:
    pass
```

**Line 303: `create`**

Parameter type hints:
- `display_name: str`
- `email_address: str`
- `role_id: str`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    display_name: str,
    email_address: str,
    role_id: str,
) -> Any:
    pass
```

**Line 344: `delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 365: `reset_password`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def reset_password(
) -> ResponseGetData:
    pass
```

**Line 390: `request_password_reset`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def request_password_reset(
) -> ResponseGetData:
    pass
```

**Line 413: `upload_avatar`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upload_avatar(
) -> ResponseGetData:
    pass
```

**Line 447: `upsert_avatar`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def upsert_avatar(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 478: `toggle_direct_signon_access`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_direct_signon_access(
) -> ResponseGetData:
    pass
```

**Line 500: `get_api_clients`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_api_clients(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 541: `get_access_tokens`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_access_tokens(
) -> Optional[Any]:
    pass
```

**Line 629: `get`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 654: `all_users`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def all_users(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 692: `search_by_email`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def search_by_email(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 743: `by_email`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def by_email(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 792: `by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 839: `virtual_user_by_subscriber_instance`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def virtual_user_by_subscriber_instance(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 860: `create_user`**

Parameter type hints:
- `display_name: str`
- `email_address: str`
- `role_id: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_user(
    display_name: str,
    email_address: str,
    role_id: str,
) -> ResponseGetData:
    pass
```

**Line 899: `upsert`**

Return type: `Any`

**Suggested signature:**
```python
async def upsert(
) -> Any:
    pass
```

**Line 971: `upsert_user`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upsert_user(
) -> ResponseGetData:
    pass
```


## Client Directory

### DomoAuth.py

**Add these imports:**
```python
from typing import list
```

**Line 79: `_DomoAuth_Optional.who_am_i`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def who_am_i(
    self,
) -> ResponseGetData:
    pass
```

**Line 100: `_DomoAuth_Optional.elevate_otp`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def elevate_otp(
    self,
) -> ResponseGetData:
    pass
```

**Line 227: `test_is_full_auth`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `function_name: str`
- `num_stacks_to_drop: Any`

Return type: `bool`

**Suggested signature:**
```python
def test_is_full_auth(
    auth: dmda.DomoAuth,
    function_name: str,
    num_stacks_to_drop: Any,
) -> bool:
    pass
```

**Line 256: `_DomoTokenAuth_Required.get_auth_token`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `token_name: str`

**Suggested signature:**
```python
async def get_auth_token(
    self,
    debug_num_stacks_to_drop: int,
    token_name: str,
) -> None:
    pass
```

**Line 331: `DomoDeveloperAuth.get_auth_token`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_auth_token(
    self,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 386: `_DomoJupyter_Required.get_jupyter_token_flow`**

Return type: `Optional[_DomoJupyter_Required]`

**Suggested signature:**
```python
def get_jupyter_token_flow(
    self,
) -> Optional[_DomoJupyter_Required]:
    pass
```

**Line 439: `DomoJupyterFullAuth.convert_auth`**

Parameter type hints:
- `jupyter_token: Any`
- `service_location: Any`
- `service_prefix: Any`

Return type: `None`

**Suggested signature:**
```python
def convert_auth(
    self,
    jupyter_token: Any,
    service_location: Any,
    service_prefix: Any,
) -> None:
    pass
```

**Line 489: `DomoJupyterTokenAuth.convert_auth`**

Parameter type hints:
- `jupyter_token: Any`
- `service_location: Any`
- `service_prefix: Any`

Return type: `None`

**Suggested signature:**
```python
def convert_auth(
    self,
    jupyter_token: Any,
    service_location: Any,
    service_prefix: Any,
) -> None:
    pass
```

**Line 509: `test_is_jupyter_auth`**

Parameter type hints:
- `function_name: str`
- `required_auth_type_ls: list[str]`

Return type: `bool`

**Suggested signature:**
```python
def test_is_jupyter_auth(
    function_name: str,
    required_auth_type_ls: list[str],
) -> bool:
    pass
```


### DomoEntity.py

**Add these imports:**
```python
from typing import Optional
```

**Line 32: `DomoEnum.get`**

Parameter type hints:
- `value: Any`

Return type: `None`

**Suggested signature:**
```python
def get(
    self,
    value: Any,
) -> None:
    pass
```

**Line 84: `DomoEntity.get_by_id`**

Return type: `Optional[DomoEntity]`

**Suggested signature:**
```python
async def get_by_id(
    self,
) -> Optional[DomoEntity]:
    pass
```

**Line 122: `DomoFederatedEntity.get_federated_parent`**

Parameter type hints:
- `parent_auth: Any`

Return type: `Optional[DomoFederatedEntity]`

**Suggested signature:**
```python
async def get_federated_parent(
    self,
    parent_auth: Any,
) -> Optional[DomoFederatedEntity]:
    pass
```

**Line 134: `DomoPublishedEntity.get_subscription`**

Return type: `Optional[DomoPublishedEntity]`

**Suggested signature:**
```python
async def get_subscription(
    self,
) -> Optional[DomoPublishedEntity]:
    pass
```

**Line 140: `DomoPublishedEntity.get_parent_publication`**

Parameter type hints:
- `parent_auth: Any`
- `parent_auth_retreival_fn: Any`

Return type: `Optional[DomoPublishedEntity]`

**Suggested signature:**
```python
async def get_parent_publication(
    self,
    parent_auth: Any,
    parent_auth_retreival_fn: Any,
) -> Optional[DomoPublishedEntity]:
    pass
```

**Line 156: `DomoPublishedEntity.get_parent_content_details`**

Parameter type hints:
- `parent_auth: Any`

Return type: `Optional[DomoPublishedEntity]`

**Suggested signature:**
```python
async def get_parent_content_details(
    self,
    parent_auth: Any,
) -> Optional[DomoPublishedEntity]:
    pass
```

**Line 164: `DomoPublishedEntity.get_federated_prent`**

Parameter type hints:
- `parent_auth: Any`

Return type: `Optional[DomoPublishedEntity]`

**Suggested signature:**
```python
async def get_federated_prent(
    self,
    parent_auth: Any,
) -> Optional[DomoPublishedEntity]:
    pass
```

**Line 173: `DomoManager.get`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def get(
    self,
) -> ResponseGetData:
    pass
```


### Logger.py

**Line 36: `TracebackDetails.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 44: `get_traceback`**

Parameter type hints:
- `num_stacks_to_drop: Any`

**Suggested signature:**
```python
def get_traceback(
    num_stacks_to_drop: Any,
) -> None:
    pass
```

**Line 146: `Logger.get_traceback`**

Parameter type hints:
- `num_stacks_to_drop: Any`

Return type: `Optional[Logger]`

**Suggested signature:**
```python
def get_traceback(
    self,
    num_stacks_to_drop: Any,
) -> Optional[Logger]:
    pass
```

**Line 208: `log_info`**

Parameter type hints:
- `message: Any`
- `debug_log: Any`
- `num_stacks_to_drop: Any`

Return type: `None`

**Suggested signature:**
```python
def log_info(
    message: Any,
    debug_log: Any,
    num_stacks_to_drop: Any,
) -> None:
    pass
```

**Line 228: `log_error`**

Parameter type hints:
- `message: Any`
- `debug_log: Any`
- `num_stacks_to_drop: Any`

Return type: `None`

**Suggested signature:**
```python
def log_error(
    message: Any,
    debug_log: Any,
    num_stacks_to_drop: Any,
) -> None:
    pass
```

**Line 249: `log_warning`**

Parameter type hints:
- `message: Any`
- `debug_log: Any`
- `num_stacks_to_drop: Any`

Return type: `None`

**Suggested signature:**
```python
def log_warning(
    message: Any,
    debug_log: Any,
    num_stacks_to_drop: Any,
) -> None:
    pass
```

**Line 270: `output_log`**

Return type: `None`

**Suggested signature:**
```python
def output_log(
) -> None:
    pass
```


### ResponseGetData.py

**Line 44: `ResponseGetData.set_response`**

Parameter type hints:
- `response: Any`

Return type: `None`

**Suggested signature:**
```python
def set_response(
    self,
    response: Any,
) -> None:
    pass
```

**Line 66: `find_ip`**

Parameter type hints:
- `html: Any`

Return type: `None`

**Suggested signature:**
```python
def find_ip(
    html: Any,
) -> None:
    pass
```


### get_data.py

**Line 75: `get_data`**

Parameter type hints:
- `timeout: Optional[dt.datetime]`

**Suggested signature:**
```python
async def get_data(
    timeout: Optional[dt.datetime] = None,
) -> None:
    pass
```

**Line 336: `looper`**

Parameter type hints:
- `url: Any`
- `offset_params: Any`
- `method: Any`
- `body_fn: Any`
- `limit: Any`
- `skip: Any`
- `maximum: Any`

**Suggested signature:**
```python
async def looper(
    url: Any,
    offset_params: Any,
    method: Any,
    body_fn: Any,
    limit: Any,
    skip: Any,
    maximum: Any,
) -> None:
    pass
```


## Routes Directory

### access_token.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 29: `get_access_tokens`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_access_tokens(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 100: `generate_expiration_unixtimestamp`**

Return type: `None`

**Suggested signature:**
```python
def generate_expiration_unixtimestamp(
) -> None:
    pass
```

**Line 127: `generate_access_token`**

Parameter type hints:
- `user_id: str`
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def generate_access_token(
    user_id: str,
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 179: `revoke_access_token`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def revoke_access_token(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```


### account.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 55: `get_available_data_providers`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_available_data_providers(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 80: `get_accounts`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_accounts(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 107: `get_oauth_accounts`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_oauth_accounts(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 358: `generate_create_account_body`**

Parameter type hints:
- `account_name: str`
- `data_provider_type: Any`
- `config_body: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_create_account_body(
    account_name: str,
    data_provider_type: Any,
    config_body: Any,
) -> None:
    pass
```

**Line 368: `create_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def create_account(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 409: `delete_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def delete_account(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 440: `generate_create_oauth_account_body`**

Parameter type hints:
- `account_name: str`
- `data_provider_type: Any`
- `origin: Any`
- `config: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_create_oauth_account_body(
    account_name: str,
    data_provider_type: Any,
    origin: Any,
    config: Any,
) -> None:
    pass
```

**Line 453: `create_oauth_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def create_oauth_account(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 504: `delete_oauth_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def delete_oauth_account(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 717: `get_account_accesslist`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_account_accesslist(
) -> Optional[Any]:
    pass
```

**Line 756: `get_oauth_account_accesslist`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_oauth_account_accesslist(
) -> Optional[Any]:
    pass
```

**Line 794: `ShareAccount.generate_payload`**

Return type: `None`

**Suggested signature:**
```python
def generate_payload(
    self,
) -> None:
    pass
```

**Line 804: `ShareAccount_V1_AccessLevel.generate_payload`**

Return type: `None`

**Suggested signature:**
```python
def generate_payload(
    self,
) -> None:
    pass
```

**Line 819: `ShareAccount_AccessLevel.generate_payload`**

Return type: `None`

**Suggested signature:**
```python
def generate_payload(
    self,
) -> None:
    pass
```

**Line 842: `share_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_account(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 888: `share_oauth_account`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_oauth_account(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 929: `share_account_v1`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_account_v1(
) -> ResponseGetData:
    pass
```


### activity_log.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 22: `get_activity_log_object_types`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_activity_log_object_types(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 82: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```


### ai.py

**Add these imports:**
```python
from typing import Optional
```

**Line 26: `generate_chat_body`**

Parameter type hints:
- `model: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_chat_body(
    model: Any,
) -> None:
    pass
```

**Line 38: `llm_generate_text`**

Parameter type hints:
- `text_input: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def llm_generate_text(
    text_input: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 81: `generate_summarize_body`**

Parameter type hints:
- `model: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_summarize_body(
    model: Any,
) -> None:
    pass
```

**Line 103: `llm_summarize_text`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def llm_summarize_text(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 154: `get_dataset_ai_readiness`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_dataset_ai_readiness(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 191: `create_dataset_ai_readiness`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_dataset_ai_readiness(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 239: `update_dataset_ai_readiness`**

Parameter type hints:
- `body: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_dataset_ai_readiness(
    body: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### appdb.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 52: `get_datastores`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_datastores(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 81: `get_datastore_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_datastore_by_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 111: `get_collections_from_datastore`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_collections_from_datastore(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 139: `create_datastore`**

Parameter type hints:
- `datastore_name: str`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_datastore(
    datastore_name: str,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 170: `create_collection`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_collection(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 238: `get_collections`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_collections(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 273: `get_collection_by_id`**

Parameter type hints:
- `collection_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_collection_by_id(
    collection_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 301: `get_documents_from_collection`**

Parameter type hints:
- `body: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_documents_from_collection(
    body: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 341: `modify_collection_permissions`**

Parameter type hints:
- `permission: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def modify_collection_permissions(
    permission: Any,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 391: `get_collection_document_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_collection_document_by_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 422: `create_document`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_document(
) -> ResponseGetData:
    pass
```

**Line 451: `update_document`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_document(
) -> ResponseGetData:
    pass
```


### application.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 68: `get_applications`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_applications(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 155: `get_application_jobs`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_application_jobs(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 168: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 195: `get_application_job_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_application_job_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 229: `generate_remote_domostats`**

Return type: `None`

**Suggested signature:**
```python
def generate_remote_domostats(
) -> None:
    pass
```

**Line 262: `generate_body_watchdog_generic`**

Parameter type hints:
- `execution_timeout: Optional[dt.datetime]`

Return type: `None`

**Suggested signature:**
```python
def generate_body_watchdog_generic(
    execution_timeout: Optional[dt.datetime] = None,
) -> None:
    pass
```

**Line 314: `create_application_job`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def create_application_job(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 354: `update_application_job`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_application_job(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 394: `update_application_job_trigger`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_application_job_trigger(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 432: `execute_application_job`**

Parameter type hints:
- `application_id: str`
- `job_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def execute_application_job(
    application_id: str,
    job_id: str,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 467: `get_available_rds_reports_step1`**

Parameter type hints:
- `application_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_available_rds_reports_step1(
    application_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 497: `get_available_rds_reports_step2`**

Parameter type hints:
- `application_id: str`
- `job_id: str`
- `execution_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_available_rds_reports_step2(
    application_id: str,
    job_id: str,
    execution_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```


### appstudio.py

**Add these imports:**
```python
from typing import Optional
```

**Line 92: `get_appstudio_access`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `appstudio_id: str`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_appstudio_access(
    auth: dmda.DomoAuth,
    appstudio_id: str,
) -> Optional[Any]:
    pass
```

**Line 123: `get_appstudios_adminsummary`**

Parameter type hints:
- `limit: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_appstudios_adminsummary(
    limit: Any,
) -> Optional[Any]:
    pass
```

**Line 144: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 240: `add_page_owner`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def add_page_owner(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 287: `share`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def share(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```


### auth.py

**Line 72: `get_full_auth`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_full_auth(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 140: `get_developer_auth`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_developer_auth(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 186: `who_am_i`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def who_am_i(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 231: `elevate_user_otp`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def elevate_user_otp(
    auth: dmda.DomoAuth,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### beastmode.py

**Add these imports:**
```python
from typing import Optional
```

**Line 35: `generate_beastmode_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_beastmode_body(
) -> None:
    pass
```

**Line 56: `search_beastmodes`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
async def search_beastmodes(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> Union[Any, list[Any], None]:
    pass
```

**Line 75: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 102: `lock_beastmode`**

Parameter type hints:
- `beastmode_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def lock_beastmode(
    beastmode_id: str,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 134: `get_beastmode_by_id`**

Parameter type hints:
- `beastmode_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_beastmode_by_id(
    beastmode_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 161: `get_card_beastmodes`**

Parameter type hints:
- `card_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_card_beastmodes(
    card_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 208: `get_dataset_beastmodes`**

Parameter type hints:
- `dataset_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_dataset_beastmodes(
    dataset_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 255: `get_page_beastmodes`**

Parameter type hints:
- `page_id: str`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_page_beastmodes(
    page_id: str,
) -> Optional[Any]:
    pass
```


### bootstrap.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 24: `get_bootstrap`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_bootstrap(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 63: `get_bootstrap_customerid`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_bootstrap_customerid(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 91: `get_bootstrap_features`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_bootstrap_features(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 116: `get_bootstrap_features_is_accountsv2_enabled`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_bootstrap_features_is_accountsv2_enabled(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 151: `get_bootstrap_pages`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_bootstrap_pages(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```


### card.py

**Add these imports:**
```python
from typing import Optional
```

**Line 50: `get_card_by_id`**

Parameter type hints:
- `card_id: str`
- `optional_parts: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_card_by_id(
    card_id: str,
    optional_parts: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 87: `get_kpi_definition`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_kpi_definition(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 135: `get_card_metadata`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_card_metadata(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 180: `generate_body_search_cards_only_apps_filter`**

Return type: `None`

**Suggested signature:**
```python
def generate_body_search_cards_only_apps_filter(
) -> None:
    pass
```

**Line 243: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```


### cloud_amplifier.py

**Line 34: `create_integration_body`**

Return type: `None`

**Suggested signature:**
```python
def create_integration_body(
) -> None:
    pass
```

**Line 83: `get_integrations`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_integrations(
) -> Optional[Any]:
    pass
```

**Line 122: `get_integration_by_id`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_integration_by_id(
) -> Optional[Any]:
    pass
```

**Line 151: `get_integration_permissions`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_integration_permissions(
) -> Optional[Any]:
    pass
```

**Line 190: `check_for_colliding_datasources`**

Return type: `bool`

**Suggested signature:**
```python
async def check_for_colliding_datasources(
) -> bool:
    pass
```

**Line 232: `get_federated_source_metadata`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_federated_source_metadata(
) -> Optional[Any]:
    pass
```

**Line 270: `get_integration_warehouses`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_integration_warehouses(
) -> Optional[Any]:
    pass
```

**Line 306: `get_databases`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_databases(
) -> Optional[Any]:
    pass
```

**Line 342: `get_schemas`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_schemas(
) -> Optional[Any]:
    pass
```

**Line 379: `get_tables`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_tables(
) -> Optional[Any]:
    pass
```

**Line 417: `convert_federated_to_cloud_amplifier`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def convert_federated_to_cloud_amplifier(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 457: `create_integration`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_integration(
) -> ResponseGetData:
    pass
```

**Line 506: `update_integration_warehouses`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_integration_warehouses(
) -> ResponseGetData:
    pass
```

**Line 540: `update_integration`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_integration(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 576: `delete_integration`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_integration(
) -> ResponseGetData:
    pass
```


### codeengine.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 28: `get_packages`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_packages(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 66: `get_codeengine_package_by_id`**

Parameter type hints:
- `package_id: str`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_codeengine_package_by_id(
    package_id: str,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 105: `get_package_versions`**

Parameter type hints:
- `package_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_package_versions(
    package_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 143: `get_codeengine_package_by_id_and_version`**

Parameter type hints:
- `package_id: str`
- `version: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_codeengine_package_by_id_and_version(
    package_id: str,
    version: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 181: `test_package_is_released`**

Parameter type hints:
- `package_id: str`
- `version: Any`
- `existing_package: Any`
- `debug_num_stacks_to_drop: int`

Return type: `bool`

**Suggested signature:**
```python
async def test_package_is_released(
    package_id: str,
    version: Any,
    existing_package: Any,
    debug_num_stacks_to_drop: int,
) -> bool:
    pass
```

**Line 212: `test_package_is_identical`**

Parameter type hints:
- `package_id: str`
- `version: Any`
- `existing_package: Any`
- `new_package: Any`
- `new_code: Any`
- `debug_num_stacks_to_drop: int`

Return type: `bool`

**Suggested signature:**
```python
async def test_package_is_identical(
    package_id: str,
    version: Any,
    existing_package: Any,
    new_package: Any,
    new_code: Any,
    debug_num_stacks_to_drop: int,
) -> bool:
    pass
```


### codeengine_crud.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 34: `deploy_code_engine_package`**

Parameter type hints:
- `package_id: str`
- `version: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def deploy_code_engine_package(
    package_id: str,
    version: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 68: `create_code_engine_package`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def create_code_engine_package(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 116: `upsert_code_engine_package_version`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def upsert_code_engine_package_version(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 174: `upsert_package`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def upsert_package(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```


### datacenter.py

**Line 101: `generate_search_datacenter_filter`**

Return type: `None`

**Suggested signature:**
```python
def generate_search_datacenter_filter(
) -> None:
    pass
```

**Line 124: `generate_search_datacenter_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_search_datacenter_body(
) -> None:
    pass
```

**Line 166: `generate_search_datacenter_account_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_search_datacenter_account_body(
) -> None:
    pass
```

**Line 199: `search_datacenter`**

Parameter type hints:
- `search_text: Any`
- `additional_filters_ls: list[str]`

**Suggested signature:**
```python
async def search_datacenter(
    search_text: Any,
    additional_filters_ls: list[str],
) -> None:
    pass
```

**Line 228: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 263: `get_connectors`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_connectors(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 317: `get_lineage_upstream`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_lineage_upstream(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 369: `share_resource`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_resource(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### dataflow.py

**Add these imports:**
```python
from typing import Optional
```

**Line 40: `get_dataflows`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_dataflows(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 68: `get_dataflow_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_dataflow_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 97: `update_dataflow_definition`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_dataflow_definition(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 159: `generate_tag_body`**

Parameter type hints:
- `dataflow_id: str`
- `tag_ls: list[str]`

**Suggested signature:**
```python
def generate_tag_body(
    dataflow_id: str,
    tag_ls: list[str],
) -> None:
    pass
```

**Line 164: `put_dataflow_tags_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def put_dataflow_tags_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 200: `get_dataflow_versions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_dataflow_versions(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 228: `get_dataflow_by_id_and_version`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_dataflow_by_id_and_version(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 257: `get_dataflow_execution_history`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_dataflow_execution_history(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 270: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 297: `get_dataflow_execution_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_dataflow_execution_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 325: `execute_dataflow`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def execute_dataflow(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 350: `generate_search_dataflows_to_jupyter_workspaces_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_search_dataflows_to_jupyter_workspaces_body(
) -> None:
    pass
```

**Line 385: `search_dataflows_to_jupyter_workspaces`**

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
async def search_dataflows_to_jupyter_workspaces(
) -> Union[Any, list[Any], None]:
    pass
```


### dataset.py

**Line 92: `query_dataset_public`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def query_dataset_public(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 127: `query_dataset_private`**

Parameter type hints:
- `limit: Any`
- `skip: Any`
- `maximum: Any`
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def query_dataset_private(
    limit: Any,
    skip: Any,
    maximum: Any,
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 153: `body_fn`**

Parameter type hints:
- `skip: Any`
- `limit: Any`
- `body: Any`

Return type: `None`

**Suggested signature:**
```python
def body_fn(
    skip: Any,
    limit: Any,
    body: Any,
) -> None:
    pass
```

**Line 170: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 217: `get_dataset_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_dataset_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 249: `get_schema`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_schema(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 278: `alter_schema`**

Parameter type hints:
- `session: httpx.AsyncClient | None`

**Suggested signature:**
```python
async def alter_schema(
    session: httpx.AsyncClient | None = None,
) -> None:
    pass
```

**Line 309: `alter_schema_descriptions`**

Parameter type hints:
- `session: httpx.AsyncClient | None`

**Suggested signature:**
```python
async def alter_schema_descriptions(
    session: httpx.AsyncClient | None = None,
) -> None:
    pass
```

**Line 340: `set_dataset_tags`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_dataset_tags(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 396: `upload_dataset_stage_1`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def upload_dataset_stage_1(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 455: `upload_dataset_stage_2_file`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def upload_dataset_stage_2_file(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 494: `upload_dataset_stage_2_df`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def upload_dataset_stage_2_df(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 535: `upload_dataset_stage_3`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def upload_dataset_stage_3(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 589: `index_dataset`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def index_dataset(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 621: `index_status`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def index_status(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 650: `generate_list_partitions_body`**

Parameter type hints:
- `limit: Any`
- `offset: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_list_partitions_body(
    limit: Any,
    offset: Any,
) -> None:
    pass
```

**Line 667: `list_partitions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def list_partitions(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 686: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 714: `generate_create_dataset_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_create_dataset_body(
) -> None:
    pass
```

**Line 732: `create`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `Any`

**Suggested signature:**
```python
async def create(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> Any:
    pass
```

**Line 765: `generate_enterprise_toolkit_body`**

Parameter type hints:
- `dataset_name: str`
- `dataset_description: Any`
- `datasource_type: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_enterprise_toolkit_body(
    dataset_name: str,
    dataset_description: Any,
    datasource_type: Any,
) -> None:
    pass
```

**Line 776: `generate_remote_domostats_body`**

Parameter type hints:
- `dataset_name: str`
- `dataset_description: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_remote_domostats_body(
    dataset_name: str,
    dataset_description: Any,
) -> None:
    pass
```

**Line 789: `create_dataset_enterprise_tookit`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_dataset_enterprise_tookit(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 818: `delete_partition_stage_1`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_partition_stage_1(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 852: `delete_partition_stage_2`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_partition_stage_2(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 885: `delete`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 917: `generate_share_dataset_payload`**

Parameter type hints:
- `entity_type: Any`
- `entity_id: str`

Return type: `None`

**Suggested signature:**
```python
def generate_share_dataset_payload(
    entity_type: Any,
    entity_id: str,
) -> None:
    pass
```

**Line 939: `share_dataset`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_dataset(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```

**Line 973: `get_permissions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_permissions(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```


### enterprise_apps.py

**Add these imports:**
```python
from typing import Optional
```

**Line 31: `get_all_designs`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_all_designs(
) -> Optional[Any]:
    pass
```

**Line 86: `get_design_by_id`**

Parameter type hints:
- `parts: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_design_by_id(
    parts: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 116: `get_design_versions`**

Parameter type hints:
- `design_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_design_versions(
    design_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 150: `get_design_source_code_by_version`**

Parameter type hints:
- `design_id: str`
- `version: Any`
- `debug_num_stacks_to_drop: int`
- `is_unpack_archive: bool`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_design_source_code_by_version(
    design_id: str,
    version: Any,
    debug_num_stacks_to_drop: int,
    is_unpack_archive: bool,
) -> Optional[Any]:
    pass
```

**Line 204: `get_design_permissions`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_design_permissions(
) -> Optional[Any]:
    pass
```

**Line 227: `set_design_admins`**

Parameter type hints:
- `design_id: str`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_design_admins(
    design_id: str,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 255: `add_design_admin`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def add_design_admin(
) -> ResponseGetData:
    pass
```


### filesets.py

**Add these imports:**
```python
from typing import list
```

**Line 21: `create_filesets_index`**

Parameter type hints:
- `index_id: str`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_filesets_index(
    index_id: str,
) -> ResponseGetData:
    pass
```

**Line 112: `get_fileset_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_fileset_by_id(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 138: `search_fileset_files`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
async def search_fileset_files(
    debug_num_stacks_to_drop: int,
) -> Union[Any, list[Any], None]:
    pass
```


### group.py

**Add these imports:**
```python
from typing import Optional
```

**Line 54: `search_groups_by_name`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def search_groups_by_name(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 98: `get_all_groups`**

Parameter type hints:
- `maximum: Any`

**Suggested signature:**
```python
async def get_all_groups(
    maximum: Any,
) -> None:
    pass
```

**Line 112: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 182: `is_system_groups_visible`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `bool`

**Suggested signature:**
```python
async def is_system_groups_visible(
    debug_num_stacks_to_drop: int,
) -> bool:
    pass
```

**Line 216: `toggle_system_group_visibility`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_system_group_visibility(
    auth: dmda.DomoAuth,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 331: `update_group`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_group(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 431: `get_group_owners`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_group_owners(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 498: `get_group_membership`**

Parameter type hints:
- `maximum: Any`

**Suggested signature:**
```python
async def get_group_membership(
    maximum: Any,
) -> None:
    pass
```

**Line 526: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```


### instance_config.py

**Add these imports:**
```python
from typing import Optional
```

**Line 48: `get_is_invite_social_users_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_is_invite_social_users_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 87: `get_is_user_invite_notifications_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_is_user_invite_notifications_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 130: `toggle_is_user_invite_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def toggle_is_user_invite_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 179: `get_allowlist`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_allowlist(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 227: `set_allowlist`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def set_allowlist(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 373: `get_authorized_domains`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_authorized_domains(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 419: `set_authorized_domains`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_authorized_domains(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 461: `get_is_weekly_digest_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_weekly_digest_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 499: `toggle_is_weekly_digest_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_weekly_digest_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 544: `get_authorized_custom_app_domains`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_authorized_custom_app_domains(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 589: `set_authorized_custom_app_domains`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_authorized_custom_app_domains(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 628: `get_is_left_nav_enabled_v1`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_left_nav_enabled_v1(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 667: `get_is_left_nav_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_left_nav_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 706: `toggle_is_left_nav_enabled_v1`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_left_nav_enabled_v1(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 749: `toggle_is_left_nav_enabled`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def toggle_is_left_nav_enabled(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```


### instance_config_api_client.py

**Add these imports:**
```python
from typing import Optional
```

**Line 31: `get_api_clients`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_api_clients(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 64: `get_client_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_client_by_id(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 141: `create_api_client`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def create_api_client(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 204: `revoke_api_client`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def revoke_api_client(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> ResponseGetData:
    pass
```


### instance_config_scheduler_policies.py

**Line 28: `get_scheduler_policies`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_scheduler_policies(
) -> Optional[Any]:
    pass
```

**Line 66: `get_scheduler_policy_by_id`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_scheduler_policy_by_id(
) -> Optional[Any]:
    pass
```

**Line 104: `create_scheduler_policy`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def create_scheduler_policy(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 165: `update_scheduler_policy`**

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_scheduler_policy(
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 203: `delete_policy`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_policy(
) -> ResponseGetData:
    pass
```


### instance_config_sso.py

**Add these imports:**
```python
from typing import Optional
```

**Line 40: `toggle_user_direct_signon_access`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def toggle_user_direct_signon_access(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 95: `get_sso_oidc_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_sso_oidc_config(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 122: `generate_sso_oidc_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_sso_oidc_body(
) -> None:
    pass
```

**Line 235: `update_sso_oidc_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_sso_oidc_config(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 268: `get_sso_saml_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_sso_saml_config(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 296: `get_sso_saml_certificate`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_sso_saml_certificate(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 317: `generate_sso_saml_body`**

Parameter type hints:
- `login_enabled: Any`
- `token_endpoint: Any`
- `user_info_endpoint: Any`
- `public_key: Any`
- `override_sso: Any`
- `override_embed: Any`
- `well_known_config: Any`
- `assertion_endpoint: Any`
- `ingest_attributes: Any`
- `custom_attributes: Any`
- `sign_auth_request: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_sso_saml_body(
    login_enabled: Any,
    token_endpoint: Any,
    user_info_endpoint: Any,
    public_key: Any,
    override_sso: Any,
    override_embed: Any,
    well_known_config: Any,
    assertion_endpoint: Any,
    ingest_attributes: Any,
    custom_attributes: Any,
    sign_auth_request: Any,
) -> None:
    pass
```

**Line 440: `update_sso_saml_config`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_sso_saml_config(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 473: `toggle_sso_skip_to_idp`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_sso_skip_to_idp(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 502: `toggle_sso_custom_attributes`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_sso_custom_attributes(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 534: `set_sso_certificate`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def set_sso_certificate(
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```


### jupyter.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 49: `get_jupyter_workspaces`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_jupyter_workspaces(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 66: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 93: `get_jupyter_workspace_by_id`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `workspace_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_jupyter_workspace_by_id(
    auth: dmda.DomoAuth,
    workspace_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 119: `parse_instance_service_location_and_prefix`**

Parameter type hints:
- `domo_instance: str`

Return type: `None`

**Suggested signature:**
```python
def parse_instance_service_location_and_prefix(
    domo_instance: str,
) -> None:
    pass
```

**Line 131: `get_workspace_auth_token_params`**

Parameter type hints:
- `workspace_id: str`
- `auth: dmda.DomoAuth`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_workspace_auth_token_params(
    workspace_id: str,
    auth: dmda.DomoAuth,
) -> Optional[Any]:
    pass
```

**Line 156: `start_jupyter_workspace`**

Parameter type hints:
- `workspace_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def start_jupyter_workspace(
    workspace_id: str,
    debug_num_stacks_to_drop: int,
) -> Union[Any, ResponseGetData, None]:
    pass
```

**Line 202: `get_jupyter_content`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_jupyter_content(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 237: `generate_update_jupyter_body__new_content_path`**

Parameter type hints:
- `content_path: Any`

Return type: `str`

**Suggested signature:**
```python
def generate_update_jupyter_body__new_content_path(
    content_path: Any,
) -> str:
    pass
```

**Line 251: `generate_update_jupyter_body__text`**

Parameter type hints:
- `body: Any`
- `content_path: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_update_jupyter_body__text(
    body: Any,
    content_path: Any,
) -> None:
    pass
```

**Line 262: `generate_update_jupyter_body__ipynb`**

Parameter type hints:
- `body: Any`
- `content_path: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_update_jupyter_body__ipynb(
    body: Any,
    content_path: Any,
) -> None:
    pass
```

**Line 274: `generate_update_jupyter_body__directory`**

Parameter type hints:
- `content_path: Any`
- `body: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_update_jupyter_body__directory(
    content_path: Any,
    body: Any,
) -> None:
    pass
```

**Line 293: `generate_update_jupyter_body`**

Parameter type hints:
- `new_content: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_update_jupyter_body(
    new_content: Any,
) -> None:
    pass
```

**Line 319: `create_jupyter_obj`**

Parameter type hints:
- `new_content: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_jupyter_obj(
    new_content: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 400: `delete_jupyter_content`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_jupyter_content(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 437: `update_jupyter_file`**

Parameter type hints:
- `new_content: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_jupyter_file(
    new_content: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 480: `get_content_recursive`**

Parameter type hints:
- `all_rows: Any`
- `content_path: Any`
- `logs: Any`
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_content_recursive(
    all_rows: Any,
    content_path: Any,
    logs: Any,
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> Optional[Any]:
    pass
```

**Line 570: `get_content`**

Parameter type hints:
- `content_path: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_content(
    content_path: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 606: `update_jupyter_workspace_config`**

Parameter type hints:
- `workspace_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_jupyter_workspace_config(
    workspace_id: str,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### page.py

**Add these imports:**
```python
from typing import Optional
```

**Line 46: `get_pages_adminsummary`**

Parameter type hints:
- `limit: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_pages_adminsummary(
    limit: Any,
) -> Optional[Any]:
    pass
```

**Line 77: `arr_fn`**

Parameter type hints:
- `res: Any`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 141: `get_page_definition`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_page_definition(
) -> Optional[Any]:
    pass
```

**Line 181: `get_page_access_test`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `page_id: str`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_page_access_test(
    auth: dmda.DomoAuth,
    page_id: str,
) -> Optional[Any]:
    pass
```

**Line 212: `get_page_access_list`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `page_id: str`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_page_access_list(
    auth: dmda.DomoAuth,
    page_id: str,
) -> Optional[Any]:
    pass
```

**Line 267: `update_page_layout`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_page_layout(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 296: `put_writelock`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def put_writelock(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 334: `delete_writelock`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_writelock(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 363: `add_page_owner`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def add_page_owner(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```


### pdp.py

**Line 89: `search_pdp_policies_by_name`**

Return type: `Union[Any, list[Any], None]`

**Suggested signature:**
```python
def search_pdp_policies_by_name(
) -> Union[Any, list[Any], None]:
    pass
```

**Line 121: `generate_policy_parameter_simple`**

Parameter type hints:
- `operator: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_policy_parameter_simple(
    operator: Any,
) -> None:
    pass
```

**Line 140: `generate_policy_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_policy_body(
) -> None:
    pass
```


### publish.py

**Add these imports:**
```python
from typing import Optional
```

**Line 41: `search_publications`**

Parameter type hints:
- `limit: Any`
- `offset: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def search_publications(
    limit: Any,
    offset: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 62: `arr_fn`**

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
) -> None:
    pass
```

**Line 93: `get_publication_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `timeout: Optional[dt.datetime]`

**Suggested signature:**
```python
async def get_publication_by_id(
    debug_num_stacks_to_drop: int,
    timeout: Optional[dt.datetime] = None,
) -> None:
    pass
```

**Line 125: `generate_publish_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_publish_body(
) -> None:
    pass
```

**Line 155: `create_publish_job`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def create_publish_job(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 184: `update_publish_job`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_publish_job(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 213: `get_publish_subscriptions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_publish_subscriptions(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 242: `get_subscription_summaries`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_subscription_summaries(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 269: `get_subscriber_content_details`**

Parameter type hints:
- `publication_id: str`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_subscriber_content_details(
    publication_id: str,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 300: `get_subscription_invitations`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_subscription_invitations(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 327: `get_subscriber_domains`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_subscriber_domains(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 354: `add_subscriber_domain`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def add_subscriber_domain(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 384: `accept_invite_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def accept_invite_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 412: `accept_invite_by_id_v2`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def accept_invite_by_id_v2(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```


### role.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 99: `get_role_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_role_by_id(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 132: `get_role_grants`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_role_grants(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 294: `get_default_role`**

Parameter type hints:
- `auth: dmda.DomoAuth`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_default_role(
    auth: dmda.DomoAuth,
) -> Optional[Any]:
    pass
```

**Line 330: `set_default_role`**

Parameter type hints:
- `parent_class: Any`

**Suggested signature:**
```python
async def set_default_role(
    parent_class: Any,
) -> None:
    pass
```

**Line 368: `update_role_metadata`**

Parameter type hints:
- `role_id: str`
- `role_name: str`

Return type: `Union[Any, ResponseGetData, None]`

**Suggested signature:**
```python
async def update_role_metadata(
    role_id: str,
    role_name: str,
) -> Union[Any, ResponseGetData, None]:
    pass
```


### sandbox.py

**Line 26: `get_is_allow_same_instance_promotion_enabled`**

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_is_allow_same_instance_promotion_enabled(
) -> Optional[Any]:
    pass
```

**Line 66: `toggle_allow_same_instance_promotion`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def toggle_allow_same_instance_promotion(
) -> ResponseGetData:
    pass
```

**Line 125: `body_fn`**

Parameter type hints:
- `skip: Any`
- `limit: Any`
- `body: Any`

Return type: `None`

**Suggested signature:**
```python
def body_fn(
    skip: Any,
    limit: Any,
    body: Any,
) -> None:
    pass
```


### stream.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 25: `get_streams`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def get_streams(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 44: `arr_fn`**

Parameter type hints:
- `res: Any`

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
    res: Any,
) -> None:
    pass
```

**Line 108: `update_stream`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def update_stream(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 165: `execute_stream`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def execute_stream(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```


### user.py

**Add these imports:**
```python
from typing import Optional
```

**Line 103: `get_all_users`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def get_all_users(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 151: `search_users`**

Parameter type hints:
- `limit: Any`
- `maximum: Any`
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def search_users(
    limit: Any,
    maximum: Any,
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 169: `body_fn`**

Parameter type hints:
- `skip: Any`
- `limit: Any`
- `body: Any`

Return type: `None`

**Suggested signature:**
```python
def body_fn(
    skip: Any,
    limit: Any,
    body: Any,
) -> None:
    pass
```

**Line 172: `arr_fn`**

Return type: `None`

**Suggested signature:**
```python
def arr_fn(
) -> None:
    pass
```

**Line 209: `search_users_by_id`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def search_users_by_id(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 275: `search_users_by_email`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

**Suggested signature:**
```python
async def search_users_by_email(
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> None:
    pass
```

**Line 428: `get_by_id`**

Parameter type hints:
- `user_id: str`
- `debug_num_stacks_to_drop: int`
- `parent_class: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_by_id(
    user_id: str,
    debug_num_stacks_to_drop: int,
    parent_class: Any,
) -> Optional[Any]:
    pass
```

**Line 548: `set_user_landing_page`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def set_user_landing_page(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 579: `reset_password`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def reset_password(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 623: `request_password_reset`**

Parameter type hints:
- `locale: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def request_password_reset(
    locale: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 683: `UserProperty.to_dict`**

Return type: `None`

**Suggested signature:**
```python
def to_dict(
    self,
) -> None:
    pass
```

**Line 690: `generate_patch_user_property_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_patch_user_property_body(
) -> None:
    pass
```

**Line 699: `update_user`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_user(
) -> ResponseGetData:
    pass
```

**Line 734: `download_avatar`**

Parameter type hints:
- `user_id: str`
- `folder_path: str`
- `img_name: Optional[str]`
- `debug_num_stacks_to_drop: int`

Return type: `bytes`

**Suggested signature:**
```python
async def download_avatar(
    user_id: str,
    folder_path: str,
    img_name: Optional[str] = None,
    debug_num_stacks_to_drop: int,
) -> bytes:
    pass
```

**Line 788: `generate_avatar_bytestr`**

Parameter type hints:
- `img_bytestr: Any`
- `img_type: Any`

Return type: `bool`

**Suggested signature:**
```python
def generate_avatar_bytestr(
    img_bytestr: Any,
    img_type: Any,
) -> bool:
    pass
```

**Line 806: `upload_avatar`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upload_avatar(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 863: `delete_user`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def delete_user(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```

**Line 892: `user_is_allowed_direct_signon`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

**Suggested signature:**
```python
async def user_is_allowed_direct_signon(
    debug_num_stacks_to_drop: int,
) -> None:
    pass
```


### user_attributes.py

**Add these imports:**
```python
from typing import Optional
```

**Line 70: `get_user_attributes`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_user_attributes(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 122: `get_user_attribute_by_id`**

Parameter type hints:
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_user_attribute_by_id(
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 162: `clean_attribute_id`**

Parameter type hints:
- `text: Any`

Return type: `None`

**Suggested signature:**
```python
def clean_attribute_id(
    text: Any,
) -> None:
    pass
```

**Line 166: `generate_create_user_attribute_body`**

Return type: `None`

**Suggested signature:**
```python
def generate_create_user_attribute_body(
) -> None:
    pass
```

**Line 195: `create_user_attribute`**

Parameter type hints:
- `attribute_id: str`
- `name: Any`
- `description: Any`
- `security_voter: Any`
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def create_user_attribute(
    attribute_id: str,
    name: Any,
    description: Any,
    security_voter: Any,
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 255: `update_user_attribute`**

Parameter type hints:
- `attribute_id: str`
- `name: Any`
- `description: Any`
- `security_voter: Any`
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def update_user_attribute(
    attribute_id: str,
    name: Any,
    description: Any,
    security_voter: Any,
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 313: `delete_user_attribute`**

Parameter type hints:
- `attribute_id: str`
- `parent_class: Any`
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def delete_user_attribute(
    attribute_id: str,
    parent_class: Any,
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```


### workflows.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 17: `get_workflow`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_workflow(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 44: `generate_trigger_workflow_body`**

Parameter type hints:
- `starting_tile: Any`
- `model_id: str`
- `version_id: str`

Return type: `None`

**Suggested signature:**
```python
def generate_trigger_workflow_body(
    starting_tile: Any,
    model_id: str,
    version_id: str,
) -> None:
    pass
```

**Line 56: `trigger_workflow`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def trigger_workflow(
    debug_num_stacks_to_drop: int,
) -> ResponseGetData:
    pass
```

**Line 94: `get_workflow_trigger_history`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_workflow_trigger_history(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```

**Line 122: `get_workflow_executions`**

Parameter type hints:
- `debug_num_stacks_to_drop: int`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_workflow_executions(
    debug_num_stacks_to_drop: int,
) -> Optional[Any]:
    pass
```


## Utils Directory

### DictDot.py

**Line 30: `split_str_to_obj`**

Return type: `None`

**Suggested signature:**
```python
def split_str_to_obj(
) -> None:
    pass
```


### Image.py

**Line 20: `isBase64`**

Parameter type hints:
- `s: Any`

Return type: `bool`

**Suggested signature:**
```python
def isBase64(
    s: Any,
) -> bool:
    pass
```

**Line 27: `handle_string_to_bytes_and_decode`**

Return type: `None`

**Suggested signature:**
```python
def handle_string_to_bytes_and_decode(
) -> None:
    pass
```

**Line 38: `handle_string_to_bytes_and_encode`**

Return type: `None`

**Suggested signature:**
```python
def handle_string_to_bytes_and_encode(
) -> None:
    pass
```

**Line 64: `crop_square`**

Return type: `None`

**Suggested signature:**
```python
def crop_square(
) -> None:
    pass
```

**Line 108: `are_same_image`**

Parameter type hints:
- `image1: Any`
- `image2: Any`

Return type: `bool`

**Suggested signature:**
```python
def are_same_image(
    image1: Any,
    image2: Any,
) -> bool:
    pass
```


### chunk_execution.py

**Line 11: `run_with_retry`**

Return type: `None`

**Suggested signature:**
```python
def run_with_retry(
) -> None:
    pass
```

**Line 16: `actual_decorator`**

Return type: `None`

**Suggested signature:**
```python
def actual_decorator(
) -> None:
    pass
```

**Line 18: `wrapper`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def wrapper(
) -> ResponseGetData:
    pass
```

**Line 43: `gather_with_concurrency`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def gather_with_concurrency(
) -> ResponseGetData:
    pass
```

**Line 53: `sem_coro`**

Parameter type hints:
- `coro: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def sem_coro(
    coro: Any,
) -> ResponseGetData:
    pass
```


### compare.py

**Line 4: `compare_dicts`**

Parameter type hints:
- `dict1: Any`
- `dict2: Any`
- `path: Any`

Return type: `None`

**Suggested signature:**
```python
def compare_dicts(
    dict1: Any,
    dict2: Any,
    path: Any,
) -> None:
    pass
```


### convert.py

**Add these imports:**
```python
from typing import Optional
```

**Line 29: `print_md`**

Parameter type hints:
- `md_str: Any`

Return type: `None`

**Suggested signature:**
```python
def print_md(
    md_str: Any,
) -> None:
    pass
```

**Line 33: `convert_epoch_millisecond_to_datetime`**

Return type: `None`

**Suggested signature:**
```python
def convert_epoch_millisecond_to_datetime(
) -> None:
    pass
```

**Line 38: `convert_datetime_to_epoch_millisecond`**

Return type: `None`

**Suggested signature:**
```python
def convert_datetime_to_epoch_millisecond(
) -> None:
    pass
```

**Line 115: `convert_snake_to_pascal`**

Parameter type hints:
- `clean_str: Any`

Return type: `None`

**Suggested signature:**
```python
def convert_snake_to_pascal(
    clean_str: Any,
) -> None:
    pass
```

**Line 122: `convert_str_to_snake_case`**

Parameter type hints:
- `text_str: Any`

Return type: `None`

**Suggested signature:**
```python
def convert_str_to_snake_case(
    text_str: Any,
) -> None:
    pass
```

**Line 144: `test_valid_email`**

Parameter type hints:
- `email: str`

Return type: `bool`

**Suggested signature:**
```python
def test_valid_email(
    email: str,
) -> bool:
    pass
```

**Line 158: `convert_string_to_bool`**

Parameter type hints:
- `v: Any`

Return type: `None`

**Suggested signature:**
```python
def convert_string_to_bool(
    v: Any,
) -> None:
    pass
```

**Line 187: `merge_dict`**

Return type: `None`

**Suggested signature:**
```python
def merge_dict(
) -> None:
    pass
```


### files.py

**Line 20: `upsert_folder`**

Parameter type hints:
- `replace_folder: Any`

Return type: `None`

**Suggested signature:**
```python
def upsert_folder(
    replace_folder: Any,
) -> None:
    pass
```

**Line 40: `upsert_file`**

Parameter type hints:
- `file_update_method: Optional[dt.datetime]`
- `encoding: Any`

**Suggested signature:**
```python
def upsert_file(
    file_update_method: Optional[dt.datetime] = None,
    encoding: Any,
) -> None:
    pass
```

**Line 62: `change_extension`**

Parameter type hints:
- `file_path: Any`
- `new_extension: Any`

Return type: `None`

**Suggested signature:**
```python
def change_extension(
    file_path: Any,
    new_extension: Any,
) -> None:
    pass
```

**Line 76: `export_zip_binary_contents`**

Parameter type hints:
- `output_folder: Any`
- `zip_bytes_content: Any`

Return type: `None`

**Suggested signature:**
```python
def export_zip_binary_contents(
    output_folder: Any,
    zip_bytes_content: Any,
) -> None:
    pass
```

**Line 87: `download_zip`**

Parameter type hints:
- `output_folder: Any`

Return type: `bytes`

**Suggested signature:**
```python
def download_zip(
    output_folder: Any,
) -> bytes:
    pass
```


### upload_data.py

**Line 11: `loop_upload`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def loop_upload(
) -> ResponseGetData:
    pass
```

**Line 68: `upload_data`**

Parameter type hints:
- `data_fn: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def upload_data(
    data_fn: Any,
) -> ResponseGetData:
    pass
```


### xkcd_password.py

**Line 25: `add_leet_to_string`**

Parameter type hints:
- `text: Any`
- `leet: Any`

Return type: `None`

**Suggested signature:**
```python
def add_leet_to_string(
    text: Any,
    leet: Any,
) -> None:
    pass
```

**Line 32: `add_padding_characters_fn`**

Parameter type hints:
- `text: Any`
- `padding: Any`

Return type: `None`

**Suggested signature:**
```python
def add_padding_characters_fn(
    text: Any,
    padding: Any,
) -> None:
    pass
```

**Line 42: `process_add_leet`**

Parameter type hints:
- `my_pass: Any`

Return type: `None`

**Suggested signature:**
```python
def process_add_leet(
    my_pass: Any,
) -> None:
    pass
```

**Line 54: `process_pad_suffix_fn`**

Parameter type hints:
- `my_pass: Any`

Return type: `None`

**Suggested signature:**
```python
def process_pad_suffix_fn(
    my_pass: Any,
) -> None:
    pass
```

**Line 58: `process_random_capitalization_fn`**

Parameter type hints:
- `text: Any`
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def process_random_capitalization_fn(
    text: Any,
    delimiter: Any,
) -> None:
    pass
```

**Line 69: `process_first_capitalization_fn`**

Parameter type hints:
- `text: Any`
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def process_first_capitalization_fn(
    text: Any,
    delimiter: Any,
) -> None:
    pass
```

**Line 82: `process_caps_first_word_add_year_and_add_suffix`**

Parameter type hints:
- `my_pass: Any`
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def process_caps_first_word_add_year_and_add_suffix(
    my_pass: Any,
    delimiter: Any,
) -> None:
    pass
```

**Line 93: `generate_xkcd_password`**

Parameter type hints:
- `min_word_length: Any`
- `max_word_length: Any`
- `valid_chars: Any`
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_xkcd_password(
    min_word_length: Any,
    max_word_length: Any,
    valid_chars: Any,
    delimiter: Any,
) -> None:
    pass
```

**Line 106: `process_domo_password_fn`**

Parameter type hints:
- `my_pass: Any`
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def process_domo_password_fn(
    my_pass: Any,
    delimiter: Any,
) -> None:
    pass
```

**Line 114: `generate_domo_password`**

Parameter type hints:
- `delimiter: Any`

Return type: `None`

**Suggested signature:**
```python
def generate_domo_password(
    delimiter: Any,
) -> None:
    pass
```


## Integrations Directory

### Automation.py

**Add these imports:**
```python
from typing import Optional
```

**Line 66: `search_or_upsert_domo_group`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `group_name: str`
- `group_type: Any`

**Suggested signature:**
```python
async def search_or_upsert_domo_group(
    auth: dmda.DomoAuth,
    group_name: str,
    group_type: Any,
) -> None:
    pass
```

**Line 124: `share_domo_account_with_domo_group`**

Parameter type hints:
- `access_level: Any`

**Suggested signature:**
```python
async def share_domo_account_with_domo_group(
    access_level: Any,
) -> None:
    pass
```

**Line 153: `remove_partition_by_x_days`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def remove_partition_by_x_days(
) -> ResponseGetData:
    pass
```


### RoleHierarchy.py

**Add these imports:**
```python
from typing import list, Optional
```

**Line 9: `extract_role_hierarchy`**

Parameter type hints:
- `hierarchy_delimiter: Any`

**Suggested signature:**
```python
def extract_role_hierarchy(
    hierarchy_delimiter: Any,
) -> None:
    pass
```

**Line 38: `get_roles_w_hierarchy`**

Parameter type hints:
- `auth: dmda.DomoAuth`
- `hierarchy_delimiter: Any`

Return type: `Optional[Any]`

**Suggested signature:**
```python
async def get_roles_w_hierarchy(
    auth: dmda.DomoAuth,
    hierarchy_delimiter: Any,
) -> Optional[Any]:
    pass
```

**Line 56: `calc_role`**

Parameter type hints:
- `current_role_id: str`
- `new_role_name: str`
- `auth: dmda.DomoAuth`
- `hierarchy_delimiter: Any`

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def calc_role(
    current_role_id: str,
    new_role_name: str,
    auth: dmda.DomoAuth,
    hierarchy_delimiter: Any,
) -> ResponseGetData:
    pass
```


### shortcut_fn.py

**Line 13: `share_domo_account_with_domo_group`**

Return type: `ResponseGetData`

**Suggested signature:**
```python
async def share_domo_account_with_domo_group(
) -> ResponseGetData:
    pass
```


## Summary

- **Files to update:** 103
- **Functions needing type hints:** 810
- **Implementation priority:** classes → client → routes → utils → integrations

## Next Steps

1. Start with the `classes/` directory
2. Add the suggested imports to each file
3. Add type hints to functions following the suggestions
4. Test that imports work after changes
5. Run linting to ensure consistency
6. Move to the next directory
