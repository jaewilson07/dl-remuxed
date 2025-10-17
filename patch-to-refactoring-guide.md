# @patch_to Refactoring Implementation Guide

## Summary

- **Files to refactor:** 38
- **Total @patch_to methods:** 221
- **Affected classes:** 45
- **Directories:** client, classes, utils

## Implementation Order

Process directories in this order for minimal dependencies:
1. **client/**: 2 files
2. **classes/**: 35 files
3. **utils/**: 1 files

## Client Directory

### Logger.py

**File:** `client\Logger.py`

**Classes in file:**
- `TracebackDetails` (line 15)
- `Logger` (line 106)

**Methods to move into classes:**

**Target class: `Logger`**
- Line 165: `_add_log()` (instance method)
- Line 208: `log_info()` (instance method)
- Line 228: `log_error()` (instance method)
- Line 249: `log_warning()` (instance method)
- Line 270: `output_log()` (instance method)

**Example refactor for `_add_log`:**
```python
# BEFORE:
@patch_to(Logger)
def _add_log(self: Logger, ...):
    pass

# AFTER (inside class definition):
def _add_log(self, ...):
    pass
```

---

### ResponseGetData.py

**File:** `client\ResponseGetData.py`

**Classes in file:**
- `BlockedByVPN` (line 19)
- `ResponseGetData` (line 32)

**Methods to move into classes:**

**Target class: `ResponseGetData`**
- Line 49: `_from_requests_response()` (classmethod)
- Line 74: `_from_httpx_response()` (classmethod)
- Line 171: `async _from_looper()` (classmethod)

**Example refactor for `_from_requests_response`:**
```python
# BEFORE:
@patch_to(ResponseGetData, cls_method=True)
def _from_requests_response(cls: ResponseGetData, ...):
    pass

# AFTER (inside class definition):
@classmethod
def _from_requests_response(cls, ...):
    pass
```

---

## Classes Directory

### DomoAccount.py

**File:** `classes\DomoAccount.py`

**Classes in file:**
- `DomoAccount` (line 32)
- `DomoAccounts_NoAccount` (line 58)
- `DomoAccounts` (line 66)

**Methods to move into classes:**

**Target class: `DomoAccounts`**
- Line 185: `async get_oauths()` (instance method)
- Line 214: `async upsert_account()` (classmethod)

**Example refactor for `get_oauths`:**
```python
# BEFORE:
@patch_to(DomoAccounts)
async def get_oauths(self: DomoAccounts, ...):
    pass

# AFTER (inside class definition):
async def get_oauths(self, ...):
    pass
```


**Target class: `DomoAccount_Default`**
- Line 314: `async upsert_target_account()` (instance method)

**Example refactor for `upsert_target_account`:**
```python
# BEFORE:
@patch_to(DomoAccount_Default)
async def upsert_target_account(self: DomoAccount_Default, ...):
    pass

# AFTER (inside class definition):
async def upsert_target_account(self, ...):
    pass
```

---

### DomoAccount_Config.py

**File:** `classes\DomoAccount_Config.py`

**Classes in file:**
- `DomoAccount_Config` (line 40)
- `AccountConfig_UsesOauth` (line 90)
- `DomoAccount_NoConfig_OAuth` (line 98)
- `AccountConfig_ProviderTypeNotDefined` (line 118)
- `DomoAccount_NoConfig` (line 126)
- `DomoAccount_Config_AbstractCredential` (line 145)
- `DomoAccount_Config_DatasetCopy` (line 164)
- `DomoAccount_Config_DomoAccessToken` (line 189)
- `DomoAccount_Config_Governance` (line 221)
- `DomoAccount_Config_AmazonS3` (line 245)
- `DomoAccount_Config_AmazonS3Advanced` (line 286)
- `DomoAccount_Config_AwsAthena` (line 327)
- `DomoAccount_Config_HighBandwidthConnector` (line 365)
- `DomoAccount_Config_Snowflake` (line 405)
- `DomoAccount_Config_SnowflakeUnload_V2` (line 441)
- `DomoAccount_Config_SnowflakeUnloadAdvancedPartition` (line 491)
- `DomoAccount_Config_SnowflakeWriteback` (line 523)
- `DomoAccount_Config_SnowflakeUnload` (line 558)
- `DomoAccount_Config_SnowflakeFederated` (line 596)
- `DomoAccount_Config_SnowflakeInternalUnload` (line 634)
- `DomoAccount_Config_SnowflakeKeyPairAuthentication` (line 666)
- `AccountConfig` (line 706)

**Methods to move into classes:**

**Target class: `dmee.DomoEnum`**
- Line 702: `generate_alt_search_str()` (instance method)

**Example refactor for `generate_alt_search_str`:**
```python
# BEFORE:
@patch_to(dmee.DomoEnum)
def generate_alt_search_str(self: dmee.DomoEnum, ...):
    pass

# AFTER (inside class definition):
def generate_alt_search_str(self, ...):
    pass
```

---

### DomoAccount_Credential.py

**File:** `classes\DomoAccount_Credential.py`

**Classes in file:**
- `DAC_NoTargetInstance` (line 26)
- `DAC_NoTargetUser` (line 34)
- `DAC_NoPassword` (line 42)
- `DAC_NoUserName` (line 50)
- `DAC_NoAccessTokenName` (line 58)
- `DAC_NoAccessToken` (line 66)
- `DAC_ValidAuth` (line 74)
- `DomoAccount_Credential` (line 84)

**Methods to move into classes:**

**Target class: `DomoAccount_Credential`**
- Line 263: `async get_target_user()` (instance method)
- Line 297: `async update_target_user_password()` (instance method)
- Line 338: `async get_target_access_token()` (instance method)
- Line 385: `async regenerate_target_access_token()` (instance method)

**Example refactor for `get_target_user`:**
```python
# BEFORE:
@patch_to(DomoAccount_Credential)
async def get_target_user(self: DomoAccount_Credential, ...):
    pass

# AFTER (inside class definition):
async def get_target_user(self, ...):
    pass
```

---

### DomoAccount_Default.py

**File:** `classes\DomoAccount_Default.py`

**Classes in file:**
- `Account_CanIModify` (line 31)
- `UpsertAccount_MatchCriteria` (line 40)
- `DomoAccounConfig_MissingFields` (line 48)
- `DomoAccount_Default` (line 57)
- `AccountClass_CRUD_Error` (line 333)

**Methods to move into classes:**

**Target class: `DomoAccount_Default`**
- Line 245: `async create_account()` (classmethod)
- Line 276: `async update_name()` (instance method)
- Line 308: `async delete_account()` (instance method)
- Line 339: `async update_config()` (instance method)

**Example refactor for `create_account`:**
```python
# BEFORE:
@patch_to(DomoAccount_Default, cls_method=True)
async def create_account(cls: DomoAccount_Default, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create_account(cls, ...):
    pass
```

---

### DomoAccount_OAuth.py

**File:** `classes\DomoAccount_OAuth.py`

**Classes in file:**
- `DomoAccountOAuth_Config_SnowflakeOauth` (line 29)
- `DomoAccountOAuth_Config_JiraOnPremOauth` (line 50)
- `OAuthConfig` (line 70)
- `DomoAccount_OAuth` (line 92)

**Methods to move into classes:**

**Target class: `dmee.DomoEnum`**
- Line 24: `generate_alt_search_str()` (instance method)

**Example refactor for `generate_alt_search_str`:**
```python
# BEFORE:
@patch_to(dmee.DomoEnum)
def generate_alt_search_str(self: dmee.DomoEnum, ...):
    pass

# AFTER (inside class definition):
def generate_alt_search_str(self, ...):
    pass
```

---

### DomoAppDb.py

**File:** `classes\DomoAppDb.py`

**Classes in file:**
- `AppDbDocument` (line 35)
- `AppDbCollection` (line 242)
- `AppDbCollections` (line 416)

**Methods to move into classes:**

**Target class: `AppDbDocument`**
- Line 187: `async create_document()` (classmethod)
- Line 216: `async update_document()` (instance method)
- Line 375: `async upsert()` (classmethod)

**Example refactor for `create_document`:**
```python
# BEFORE:
@patch_to(AppDbDocument, cls_method=True)
async def create_document(cls: AppDbDocument, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create_document(cls, ...):
    pass
```


**Target class: `AppDbCollection`**
- Line 299: `async share_collection()` (instance method)
- Line 323: `async query_documents()` (instance method)

**Example refactor for `share_collection`:**
```python
# BEFORE:
@patch_to(AppDbCollection)
async def share_collection(self: AppDbCollection, ...):
    pass

# AFTER (inside class definition):
async def share_collection(self, ...):
    pass
```

---

### DomoAppStudio.py

**File:** `classes\DomoAppStudio.py`

**Classes in file:**
- `DomoAppStudio` (line 19)
- `DomoAppStudios` (line 154)

**Methods to move into classes:**

**Target class: `DomoAppStudio`**
- Line 132: `async _from_adminsummary()` (classmethod)
- Line 197: `async get_accesslist()` (instance method)
- Line 255: `async share()` (instance method)
- Line 284: `async add_appstudio_owner()` (classmethod)

**Example refactor for `_from_adminsummary`:**
```python
# BEFORE:
@patch_to(DomoAppStudio, cls_method=True)
async def _from_adminsummary(cls: DomoAppStudio, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def _from_adminsummary(cls, ...):
    pass
```

---

### DomoApplication.py

**File:** `classes\DomoApplication.py`

**Classes in file:**
- `DomoJob_Types` (line 18)
- `DomoApplication` (line 46)

**Methods to move into classes:**

**Target class: `DomoApplication`**
- Line 78: `async get_by_id()` (classmethod)
- Line 102: `async get_jobs()` (instance method)
- Line 128: `async get_schedules()` (instance method)
- Line 166: `async find_next_job_schedule()` (instance method)

**Example refactor for `get_by_id`:**
```python
# BEFORE:
@patch_to(DomoApplication, cls_method=True)
async def get_by_id(cls: DomoApplication, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def get_by_id(cls, ...):
    pass
```

---

### DomoApplication_Job_Base.py

**File:** `classes\DomoApplication_Job_Base.py`

**Classes in file:**
- `DomoTrigger_Schedule` (line 16)
- `DomoTrigger` (line 63)
- `DomoJob_Base` (line 80)

**Methods to move into classes:**

**Target class: `DomoJob_Base`**
- Line 144: `_from_dict()` (classmethod)
- Line 160: `async _get_by_id()` (classmethod)
- Line 201: `async get_by_id()` (classmethod)
- Line 230: `_generate_to_dict()` (instance method)
- Line 257: `to_dict()` (instance method)

**Example refactor for `_from_dict`:**
```python
# BEFORE:
@patch_to(DomoJob_Base, cls_method=True)
def _from_dict(cls: DomoJob_Base, ...):
    pass

# AFTER (inside class definition):
@classmethod
def _from_dict(cls, ...):
    pass
```

---

### DomoApplication_Job_RemoteDomoStats.py

**File:** `classes\DomoApplication_Job_RemoteDomoStats.py`

**Classes in file:**
- `RemoteDomoStats_Config_Policy` (line 24)
- `RemoteDomoStats_Config` (line 39)
- `DomoJob_RemoteDomoStats` (line 74)

**Methods to move into classes:**

**Target class: `DomoJob_RemoteDomoStats`**
- Line 137: `async create()` (classmethod)

**Example refactor for `create`:**
```python
# BEFORE:
@patch_to(DomoJob_RemoteDomoStats, cls_method=True)
async def create(cls: DomoJob_RemoteDomoStats, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create(cls, ...):
    pass
```

---

### DomoApplication_Job_Watchdog.py

**File:** `classes\DomoApplication_Job_Watchdog.py`

**Classes in file:**
- `Watchdog_Config` (line 32)
- `Watchdog_Config_MaxIndexingTime` (line 59)
- `Watchdog_Config__Variance` (line 79)
- `Watchdog_Config_RowCountVariance` (line 97)
- `Watchdog_Config_ExecutionVariance` (line 102)
- `Watchdog_Config_ErrorDetection` (line 107)
- `Watchdog_Config_LastDataUpdated` (line 117)
- `Watchdog_Config_CustomQuery` (line 139)
- `Watchdog_ConfigFactory` (line 156)
- `DomoJob_Watchdog` (line 166)

**Methods to move into classes:**

**Target class: `DomoJob_Base`**
- Line 242: `async update()` (instance method)
- Line 264: `async execute()` (instance method)

**Example refactor for `update`:**
```python
# BEFORE:
@patch_to(DomoJob_Base)
async def update(self: DomoJob_Base, ...):
    pass

# AFTER (inside class definition):
async def update(self, ...):
    pass
```


**Target class: `DomoJob_Watchdog`**
- Line 285: `async create()` (classmethod)

**Example refactor for `create`:**
```python
# BEFORE:
@patch_to(DomoJob_Watchdog, cls_method=True)
async def create(cls: DomoJob_Watchdog, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create(cls, ...):
    pass
```

---

### DomoBootstrap.py

**File:** `classes\DomoBootstrap.py`

**Classes in file:**
- `DomoBootstrap_Feature` (line 18)
- `DomoBootstrap` (line 40)

**Methods to move into classes:**

**Target class: `DomoBootstrap`**
- Line 75: `async get_customer_id()` (instance method)
- Line 100: `async get_pages()` (instance method)
- Line 134: `async get_features()` (instance method)
- Line 162: `async is_feature_accountsv2_enabled()` (instance method)

**Example refactor for `get_customer_id`:**
```python
# BEFORE:
@patch_to(DomoBootstrap)
async def get_customer_id(self: DomoBootstrap, ...):
    pass

# AFTER (inside class definition):
async def get_customer_id(self, ...):
    pass
```

---

### DomoCard.py

**File:** `classes\DomoCard.py`

**Classes in file:**
- `DomoCard` (line 23)
- `Card_DownloadSourceCode` (line 211)

**Methods to move into classes:**

**Target class: `DomoCard`**
- Line 146: `async get_datasets()` (instance method)
- Line 181: `async share()` (instance method)
- Line 217: `async get_collections()` (instance method)
- Line 247: `async get_source_code()` (instance method)
- Line 285: `async download_source_code()` (instance method)

**Example refactor for `get_datasets`:**
```python
# BEFORE:
@patch_to(DomoCard)
async def get_datasets(self: DomoCard, ...):
    pass

# AFTER (inside class definition):
async def get_datasets(self, ...):
    pass
```

---

### DomoCodeEngine.py

**File:** `classes\DomoCodeEngine.py`

**Classes in file:**
- `ExportExtension` (line 30)
- `DomoCodeEngine_ConfigError` (line 35)
- `DomoCodeEngine_PackageVersion` (line 51)
- `DomoCodeEngine_Package` (line 294)

**Methods to move into classes:**

**Target class: `DomoCodeEngine_PackageVersion`**
- Line 267: `export()` (instance method)

**Example refactor for `export`:**
```python
# BEFORE:
@patch_to(DomoCodeEngine_PackageVersion)
def export(self: DomoCodeEngine_PackageVersion, ...):
    pass

# AFTER (inside class definition):
def export(self, ...):
    pass
```


**Target class: `DomoCodeEngine_Package`**
- Line 382: `async get_current_version_by_id()` (classmethod)

**Example refactor for `get_current_version_by_id`:**
```python
# BEFORE:
@patch_to(DomoCodeEngine_Package, cls_method=True)
async def get_current_version_by_id(cls: DomoCodeEngine_Package, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def get_current_version_by_id(cls, ...):
    pass
```

---

### DomoDatacenter.py

**File:** `classes\DomoDatacenter.py`

**Classes in file:**
- `DomoDatacenter` (line 20)

**Methods to move into classes:**

**Target class: `DomoDatacenter`**
- Line 27: `async search_datacenter()` (instance method)
- Line 58: `async search_datasets()` (instance method)
- Line 98: `async get_accounts()` (instance method)
- Line 153: `async search_cards()` (instance method)
- Line 198: `async get_cards_admin_summary()` (instance method)
- Line 247: `async search_codeengine()` (instance method)

**Example refactor for `search_datacenter`:**
```python
# BEFORE:
@patch_to(DomoDatacenter)
async def search_datacenter(self: DomoDatacenter, ...):
    pass

# AFTER (inside class definition):
async def search_datacenter(self, ...):
    pass
```

---

### DomoDataflow.py

**File:** `classes\DomoDataflow.py`

**Classes in file:**
- `DomoDataflow` (line 26)
- `DomoDataflows` (line 290)

**Methods to move into classes:**

**Target class: `DomoDataflow`**
- Line 119: `async get_definition()` (instance method)
- Line 147: `async update_dataflow_definition()` (instance method)
- Line 167: `async get_jupyter_config()` (instance method)
- Line 200: `async execute()` (instance method)
- Line 216: `async get_by_version_id()` (classmethod)
- Line 250: `async get_versions()` (instance method)

**Example refactor for `get_definition`:**
```python
# BEFORE:
@patch_to(DomoDataflow)
async def get_definition(self: DomoDataflow, ...):
    pass

# AFTER (inside class definition):
async def get_definition(self, ...):
    pass
```

---

### DomoDataflow_Action.py

**File:** `classes\DomoDataflow_Action.py`

**Classes in file:**
- `DomoDataflow_Action_Type` (line 21)
- `DomoAction` (line 28)
- `DomoDataflow_Action` (line 35)
- `DomoDataflow_ActionResult` (line 88)

**Methods to move into classes:**

**Target class: `DomoDataflow_Action`**
- Line 68: `get_parents()` (instance method)

**Example refactor for `get_parents`:**
```python
# BEFORE:
@patch_to(DomoDataflow_Action)
def get_parents(self: DomoDataflow_Action, ...):
    pass

# AFTER (inside class definition):
def get_parents(self, ...):
    pass
```

---

### DomoDataflow_History.py

**File:** `classes\DomoDataflow_History.py`

**Classes in file:**
- `DomoDataflow_History_Execution` (line 21)
- `DomoDataflow_History` (line 144)

**Methods to move into classes:**

**Target class: `DomoDataflow_History_Execution`**
- Line 81: `async get_by_id()` (classmethod)
- Line 110: `async get_actions()` (instance method)

**Example refactor for `get_by_id`:**
```python
# BEFORE:
@patch_to(DomoDataflow_History_Execution, cls_method=True)
async def get_by_id(cls: DomoDataflow_History_Execution, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def get_by_id(cls, ...):
    pass
```


**Target class: `DomoDataflow_History`**
- Line 154: `async get_execution_history()` (instance method)

**Example refactor for `get_execution_history`:**
```python
# BEFORE:
@patch_to(DomoDataflow_History)
async def get_execution_history(self: DomoDataflow_History, ...):
    pass

# AFTER (inside class definition):
async def get_execution_history(self, ...):
    pass
```

---

### DomoDataset.py

**File:** `classes\DomoDataset.py`

**Classes in file:**
- `DomoDataset_Default` (line 48)
- `FederatedDomoDataset` (line 677)
- `DomoPublishDataset` (line 724)
- `DomoDataset` (line 734)

**Methods to move into classes:**

**Target class: `DomoDataset_Default`**
- Line 189: `async query_dataset_private()` (instance method)
- Line 252: `async delete()` (instance method)
- Line 271: `async share()` (instance method)
- Line 301: `async index_dataset()` (instance method)
- Line 317: `async upload_data()` (instance method)
- Line 445: `async list_partitions()` (instance method)
- Line 466: `async create()` (classmethod)
- Line 501: `async delete_partition()` (instance method)
- Line 572: `async reset_dataset()` (instance method)
- Line 632: `async upsert_connector()` (instance method)
- Line 656: `_is_federated_dataset_obj()` (instance method)

**Example refactor for `query_dataset_private`:**
```python
# BEFORE:
@patch_to(DomoDataset_Default)
async def query_dataset_private(self: DomoDataset_Default, ...):
    pass

# AFTER (inside class definition):
async def query_dataset_private(self, ...):
    pass
```

---

### DomoDataset_PDP.py

**File:** `classes\DomoDataset_PDP.py`

**Classes in file:**
- `PDP_Parameter` (line 16)
- `PDP_Policy` (line 58)
- `Dataset_PDP_Policies` (line 166)
- `SearchPDP_NotFound` (line 212)

**Methods to move into classes:**

**Target class: `PDP_Parameter`**
- Line 34: `generate_parameter_simple()` (instance method)
- Line 46: `generate_body_from_parameter()` (instance method)

**Example refactor for `generate_parameter_simple`:**
```python
# BEFORE:
@patch_to(PDP_Parameter)
def generate_parameter_simple(self: PDP_Parameter, ...):
    pass

# AFTER (inside class definition):
def generate_parameter_simple(self, ...):
    pass
```


**Target class: `PDP_Policy`**
- Line 143: `generate_body_from_policy()` (instance method)
- Line 291: `async delete_policy()` (instance method)

**Example refactor for `generate_body_from_policy`:**
```python
# BEFORE:
@patch_to(PDP_Policy)
def generate_body_from_policy(self: PDP_Policy, ...):
    pass

# AFTER (inside class definition):
def generate_body_from_policy(self, ...):
    pass
```


**Target class: `Dataset_PDP_Policies`**
- Line 178: `async get_policies()` (instance method)
- Line 226: `async search_pdp_policies()` (classmethod)
- Line 310: `async toggle_dataset_pdp()` (instance method)

**Example refactor for `get_policies`:**
```python
# BEFORE:
@patch_to(Dataset_PDP_Policies)
async def get_policies(self: Dataset_PDP_Policies, ...):
    pass

# AFTER (inside class definition):
async def get_policies(self, ...):
    pass
```

---

### DomoDataset_Schema.py

**File:** `classes\DomoDataset_Schema.py`

**Classes in file:**
- `DatasetSchema_Types` (line 24)
- `DomoDataset_Schema_Column` (line 33)
- `DomoDataset_Schema` (line 76)
- `DatasetSchema_InvalidSchema` (line 129)
- `CRUD_Dataset_Error` (line 221)

**Methods to move into classes:**

**Target class: `DomoDataset_Schema`**
- Line 146: `async _test_missing_columns()` (instance method)
- Line 173: `async reset_col_order()` (instance method)
- Line 190: `add_col()` (instance method)
- Line 206: `remove_col()` (instance method)
- Line 233: `async alter_schema()` (instance method)
- Line 262: `async alter_schema_descriptions()` (instance method)

**Example refactor for `_test_missing_columns`:**
```python
# BEFORE:
@patch_to(DomoDataset_Schema)
async def _test_missing_columns(self: DomoDataset_Schema, ...):
    pass

# AFTER (inside class definition):
async def _test_missing_columns(self, ...):
    pass
```

---

### DomoGroup.py

**File:** `classes\DomoGroup.py`

**Classes in file:**
- `Group_Class_Error` (line 20)
- `DomoGroup` (line 33)
- `DomoGroups` (line 248)

**Methods to move into classes:**

**Target class: `DomoGroup`**
- Line 143: `async create_from_name()` (classmethod)
- Line 175: `async update_metadata()` (instance method)
- Line 227: `async delete()` (instance method)

**Example refactor for `create_from_name`:**
```python
# BEFORE:
@patch_to(DomoGroup, cls_method=True)
async def create_from_name(cls: DomoGroup, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create_from_name(cls, ...):
    pass
```


**Target class: `DomoGroups`**
- Line 313: `async get()` (instance method)
- Line 350: `async search_by_name()` (instance method)
- Line 401: `async upsert()` (instance method)

**Example refactor for `get`:**
```python
# BEFORE:
@patch_to(DomoGroups)
async def get(self: DomoGroups, ...):
    pass

# AFTER (inside class definition):
async def get(self, ...):
    pass
```

---

### DomoInstanceConfig.py

**File:** `classes\DomoInstanceConfig.py`

**Classes in file:**
- `DomoInstanceConfig` (line 33)
- `InstanceConfig_ClassError` (line 388)

**Methods to move into classes:**

**Target class: `DomoInstanceConfig`**
- Line 79: `async get_applications()` (instance method)
- Line 105: `async generate_applications_report()` (instance method)
- Line 141: `async get_authorized_domains()` (instance method)
- Line 160: `async set_authorized_domains()` (instance method)
- Line 181: `async upsert_authorized_domains()` (instance method)
- Line 206: `async get_authorized_custom_app_domains()` (instance method)
- Line 231: `async set_authorized_custom_app_domains()` (instance method)
- Line 251: `async upsert_authorized_custom_app_domains()` (instance method)
- Line 275: `async get_sandbox_is_same_instance_promotion_enabled()` (instance method)
- Line 300: `async toggle_sandbox_allow_same_instance_promotion()` (instance method)
- Line 328: `async get_is_user_invite_notification_enabled()` (instance method)
- Line 357: `async toggle_is_user_invite_notification_enabled()` (instance method)
- Line 398: `async get_is_invite_social_users_enabled()` (instance method)
- Line 439: `async toggle_is_invite_social_users_enabled()` (instance method)
- Line 472: `async get_is_weekly_digest_enabled()` (instance method)
- Line 498: `async toggle_is_weekly_digest_enabled()` (instance method)
- Line 541: `async toggle_is_left_nav_enabled()` (instance method)
- Line 569: `async get_is_left_nav_enabled()` (instance method)
- Line 595: `async toggle_is_left_nav_enabled()` (instance method)
- Line 623: `async get_is_left_nav_enabled()` (instance method)

**Example refactor for `get_applications`:**
```python
# BEFORE:
@patch_to(DomoInstanceConfig)
async def get_applications(self: DomoInstanceConfig, ...):
    pass

# AFTER (inside class definition):
async def get_applications(self, ...):
    pass
```

---

### DomoInstanceConfig_ApiClient.py

**File:** `classes\DomoInstanceConfig_ApiClient.py`

**Classes in file:**
- `ApiClient` (line 22)
- `ApiClient_Search_Error` (line 109)
- `ApiClients` (line 119)

**Methods to move into classes:**

**Target class: `ApiClients`**
- Line 185: `async create_for_authorized_user()` (instance method)
- Line 220: `async upsert_client()` (instance method)

**Example refactor for `create_for_authorized_user`:**
```python
# BEFORE:
@patch_to(ApiClients)
async def create_for_authorized_user(self: ApiClients, ...):
    pass

# AFTER (inside class definition):
async def create_for_authorized_user(self, ...):
    pass
```

---

### DomoInstanceConfig_MFA.py

**File:** `classes\DomoInstanceConfig_MFA.py`

**Classes in file:**
- `MFAConfig_InstantiationError` (line 14)
- `MFA_Config` (line 22)

**Methods to move into classes:**

**Target class: `MFA_Config`**
- Line 102: `_test_need_update_config()` (instance method)
- Line 119: `async toggle_mfa()` (instance method)
- Line 155: `async enable()` (instance method)
- Line 173: `async disable()` (instance method)
- Line 191: `async set_max_code_attempts()` (instance method)
- Line 227: `async set_num_days_valid()` (instance method)
- Line 262: `async update()` (instance method)

**Example refactor for `_test_need_update_config`:**
```python
# BEFORE:
@patch_to(MFA_Config)
def _test_need_update_config(self: MFA_Config, ...):
    pass

# AFTER (inside class definition):
def _test_need_update_config(self, ...):
    pass
```

---

### DomoInstanceConfig_UserAttribute.py

**File:** `classes\DomoInstanceConfig_UserAttribute.py`

**Classes in file:**
- `UserAttribute` (line 22)
- `UserAttributes` (line 122)

**Methods to move into classes:**

**Target class: `UserAttribute`**
- Line 89: `async update()` (instance method)

**Example refactor for `update`:**
```python
# BEFORE:
@patch_to(UserAttribute)
async def update(self: UserAttribute, ...):
    pass

# AFTER (inside class definition):
async def update(self, ...):
    pass
```


**Target class: `UserAttributes`**
- Line 158: `async create()` (instance method)
- Line 198: `async upsert()` (instance method)
- Line 264: `async delete()` (instance method)

**Example refactor for `create`:**
```python
# BEFORE:
@patch_to(UserAttributes)
async def create(self: UserAttributes, ...):
    pass

# AFTER (inside class definition):
async def create(self, ...):
    pass
```

---

### DomoJupyter.py

**File:** `classes\DomoJupyter.py`

**Classes in file:**
- `DJW_Search_Error` (line 37)
- `DJW_InvalidClass` (line 55)
- `DomoJupyterWorkspace` (line 61)
- `DomoJupyterWorkspaces` (line 392)

**Methods to move into classes:**

**Target class: `DomoJupyterWorkspace`**
- Line 267: `async get_current_workspace()` (classmethod)
- Line 287: `async get_account_configuration()` (instance method)
- Line 308: `async get_input_configuration()` (instance method)
- Line 327: `async get_output_configuration()` (instance method)
- Line 346: `_add_config()` (instance method)
- Line 363: `add_config_input_datasource()` (instance method)
- Line 373: `add_config_output_datasource()` (instance method)
- Line 383: `add_config_account()` (instance method)
- Line 483: `_test_config_duplicates()` (instance method)
- Line 494: `async update_config()` (instance method)
- Line 521: `async add_account()` (instance method)
- Line 585: `async add_input_dataset()` (instance method)
- Line 636: `async add_output_dataset()` (instance method)
- Line 685: `async get_content()` (instance method)
- Line 712: `async download_workspace_content()` (instance method)

**Example refactor for `get_current_workspace`:**
```python
# BEFORE:
@patch_to(DomoJupyterWorkspace, cls_method=True)
async def get_current_workspace(cls: DomoJupyterWorkspace, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def get_current_workspace(cls, ...):
    pass
```

---

### DomoJupyter_Account.py

**File:** `classes\DomoJupyter_Account.py`

**Classes in file:**
- `DJW_PermissionToAccountDenied` (line 25)
- `DJW_AccountInvalid_NotAddedToWorkspace` (line 30)
- `DomoJupyter_Account` (line 76)
- `DJW_InvalidClass` (line 249)

**Methods to move into classes:**

**Target class: `DomoJupyter_Account`**
- Line 255: `async regenerate_failed_password()` (instance method)
- Line 321: `async regenerate_failed_token()` (instance method)

**Example refactor for `regenerate_failed_password`:**
```python
# BEFORE:
@patch_to(DomoJupyter_Account)
async def regenerate_failed_password(self: DomoJupyter_Account, ...):
    pass

# AFTER (inside class definition):
async def regenerate_failed_password(self, ...):
    pass
```

---

### DomoMembership.py

**File:** `classes\DomoMembership.py`

**Classes in file:**
- `UpdateMembership` (line 18)
- `Membership_Entity` (line 28)
- `Membership` (line 44)
- `GroupMembership` (line 181)

**Methods to move into classes:**

**Target class: `GroupMembership`**
- Line 268: `async add_members()` (instance method)
- Line 298: `async remove_members()` (instance method)
- Line 328: `async set_members()` (instance method)
- Line 372: `async add_owners()` (instance method)
- Line 402: `async remove_owners()` (instance method)
- Line 432: `async set_owners()` (instance method)
- Line 490: `async add_owner_manage_all_groups_role()` (instance method)

**Example refactor for `add_members`:**
```python
# BEFORE:
@patch_to(GroupMembership)
async def add_members(self: GroupMembership, ...):
    pass

# AFTER (inside class definition):
async def add_members(self, ...):
    pass
```

---

### DomoPDP.py

**File:** `classes\DomoPDP.py`

**Classes in file:**
- `PDP_Parameter` (line 16)
- `PDP_Policy` (line 58)
- `Dataset_PDP_Policies` (line 166)
- `SearchPDP_NotFound` (line 212)

**Methods to move into classes:**

**Target class: `PDP_Parameter`**
- Line 34: `generate_parameter_simple()` (instance method)
- Line 46: `generate_body_from_parameter()` (instance method)

**Example refactor for `generate_parameter_simple`:**
```python
# BEFORE:
@patch_to(PDP_Parameter)
def generate_parameter_simple(self: PDP_Parameter, ...):
    pass

# AFTER (inside class definition):
def generate_parameter_simple(self, ...):
    pass
```


**Target class: `PDP_Policy`**
- Line 143: `generate_body_from_policy()` (instance method)
- Line 291: `async delete_policy()` (instance method)

**Example refactor for `generate_body_from_policy`:**
```python
# BEFORE:
@patch_to(PDP_Policy)
def generate_body_from_policy(self: PDP_Policy, ...):
    pass

# AFTER (inside class definition):
def generate_body_from_policy(self, ...):
    pass
```


**Target class: `Dataset_PDP_Policies`**
- Line 178: `async get_policies()` (instance method)
- Line 226: `async search_pdp_policies()` (classmethod)
- Line 310: `async toggle_dataset_pdp()` (instance method)

**Example refactor for `get_policies`:**
```python
# BEFORE:
@patch_to(Dataset_PDP_Policies)
async def get_policies(self: Dataset_PDP_Policies, ...):
    pass

# AFTER (inside class definition):
async def get_policies(self, ...):
    pass
```

---

### DomoPage.py

**File:** `classes\DomoPage.py`

**Classes in file:**
- `DomoPage_GetRecursive` (line 22)
- `DomoPage` (line 40)
- `DomoPages` (line 317)
- `Page_NoAccess` (line 469)

**Methods to move into classes:**

**Target class: `DomoPage`**
- Line 229: `async _from_adminsummary()` (classmethod)
- Line 281: `async _from_bootstrap()` (classmethod)
- Line 362: `async get_children()` (instance method)
- Line 409: `flatten_children()` (instance method)
- Line 426: `async get_parents()` (instance method)
- Line 480: `async test_page_access()` (instance method)
- Line 526: `async get_accesslist()` (instance method)
- Line 659: `async share()` (instance method)
- Line 690: `async get_cards()` (instance method)
- Line 720: `async get_datasets()` (instance method)
- Line 747: `async update_layout()` (classmethod)
- Line 782: `async add_owner()` (instance method)

**Example refactor for `_from_adminsummary`:**
```python
# BEFORE:
@patch_to(DomoPage, cls_method=True)
async def _from_adminsummary(cls: DomoPage, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def _from_adminsummary(cls, ...):
    pass
```

---

### DomoPublish.py

**File:** `classes\DomoPublish.py`

**Classes in file:**
- `DomoPublication_Content_Enum` (line 32)
- `DomoPublication_Content` (line 45)
- `DomoPublication_UnexpectedContentType` (line 117)
- `DomoPublication` (line 126)
- `DomoSubscription_NoParentAuth` (line 367)
- `DomoSubscription_NoParent` (line 376)
- `DomoSubscription` (line 386)
- `DomoEverywhere` (line 545)

**Methods to move into classes:**

**Target class: `DomoPublication`**
- Line 290: `async create_publication()` (classmethod)
- Line 335: `async update_publication()` (instance method)
- Line 514: `async get_content()` (instance method)
- Line 665: `async report_content_as_dataframe()` (instance method)
- Line 687: `report_lineage_as_dataframe()` (instance method)

**Example refactor for `create_publication`:**
```python
# BEFORE:
@patch_to(DomoPublication, cls_method=True)
async def create_publication(cls: DomoPublication, ...):
    pass

# AFTER (inside class definition):
@classmethod
async def create_publication(cls, ...):
    pass
```

---

### DomoRole.py

**File:** `classes\DomoRole.py`

**Classes in file:**
- `DomoRole` (line 27)
- `SetRoleGrants_MissingGrants` (line 131)
- `AddUser_Error` (line 252)
- `DeleteRole_Error` (line 337)
- `SearchRole_NotFound` (line 392)
- `DomoRoles` (line 402)

**Methods to move into classes:**

**Target class: `DomoRole`**
- Line 102: `async get_grants()` (instance method)
- Line 140: `async set_grants()` (instance method)
- Line 186: `async create()` (classmethod)
- Line 220: `async get_membership()` (instance method)
- Line 262: `async add_user()` (instance method)
- Line 302: `async update()` (instance method)
- Line 345: `async delete()` (instance method)
- Line 363: `async delete_role()` (classmethod)
- Line 574: `async set_as_default_role()` (instance method)

**Example refactor for `get_grants`:**
```python
# BEFORE:
@patch_to(DomoRole)
async def get_grants(self: DomoRole, ...):
    pass

# AFTER (inside class definition):
async def get_grants(self, ...):
    pass
```


**Target class: `DomoRoles`**
- Line 496: `async create()` (instance method)
- Line 520: `async upsert()` (instance method)

**Example refactor for `create`:**
```python
# BEFORE:
@patch_to(DomoRoles)
async def create(self: DomoRoles, ...):
    pass

# AFTER (inside class definition):
async def create(self, ...):
    pass
```

---

### DomoTag.py

**File:** `classes\DomoTag.py`

**Classes in file:**
- `DomoTags_SetTagsError` (line 18)
- `DomoTags` (line 27)

**Methods to move into classes:**

**Target class: `DomoTags`**
- Line 99: `async add()` (instance method)
- Line 119: `async remove()` (instance method)

**Example refactor for `add`:**
```python
# BEFORE:
@patch_to(DomoTags)
async def add(self: DomoTags, ...):
    pass

# AFTER (inside class definition):
async def add(self, ...):
    pass
```

---

### DomoUser.py

**File:** `classes\DomoUser.py`

**Classes in file:**
- `CreateUser_MissingRole` (line 38)
- `DownloadAvatar_NoAvatarKey` (line 46)
- `DomoUser` (line 59)
- `DomoUsers` (line 576)
- `DomoUser_NoSearch` (line 684)

**Methods to move into classes:**

**Target class: `DomoUser`**
- Line 151: `async get_role()` (instance method)
- Line 171: `async get_by_id()` (classmethod)
- Line 216: `async download_avatar()` (instance method)
- Line 257: `async update_properties()` (instance method)
- Line 285: `async set_user_landing_page()` (instance method)
- Line 303: `async create()` (classmethod)
- Line 344: `async delete()` (instance method)
- Line 365: `async reset_password()` (instance method)
- Line 390: `async request_password_reset()` (classmethod)
- Line 413: `async upload_avatar()` (instance method)
- Line 447: `async upsert_avatar()` (instance method)
- Line 478: `async toggle_direct_signon_access()` (instance method)
- Line 500: `async get_api_clients()` (instance method)
- Line 541: `async get_access_tokens()` (instance method)

**Example refactor for `get_role`:**
```python
# BEFORE:
@patch_to(DomoUser)
async def get_role(self: DomoUser, ...):
    pass

# AFTER (inside class definition):
async def get_role(self, ...):
    pass
```


**Target class: `DomoUsers`**
- Line 629: `async get()` (instance method)
- Line 654: `async all_users()` (classmethod)
- Line 692: `async search_by_email()` (instance method)
- Line 743: `async by_email()` (classmethod)
- Line 792: `async by_id()` (classmethod)
- Line 839: `async virtual_user_by_subscriber_instance()` (classmethod)
- Line 860: `async create_user()` (classmethod)
- Line 899: `async upsert()` (instance method)
- Line 971: `async upsert_user()` (classmethod)

**Example refactor for `get`:**
```python
# BEFORE:
@patch_to(DomoUsers)
async def get(self: DomoUsers, ...):
    pass

# AFTER (inside class definition):
async def get(self, ...):
    pass
```

---

## Utils Directory

### Image.py

**File:** `utils\Image.py`

**Methods to move into classes:**

**Target class: `Image`**
- Line 50: `to_bytes()` (instance method)
- Line 64: `crop_square()` (instance method)
- Line 84: `from_image_file()` (classmethod)
- Line 99: `from_bytestr()` (classmethod)

**Example refactor for `to_bytes`:**
```python
# BEFORE:
@patch_to(Image)
def to_bytes(self: Image, ...):
    pass

# AFTER (inside class definition):
def to_bytes(self, ...):
    pass
```

---

## Methods by Target Class

This shows which methods need to be moved into each class:

### ApiClients

**Total methods:** 2

- `async create_for_authorized_user()` (instance) - classes\DomoInstanceConfig_ApiClient.py:185
- `async upsert_client()` (instance) - classes\DomoInstanceConfig_ApiClient.py:220

### AppDbCollection

**Total methods:** 2

- `async share_collection()` (instance) - classes\DomoAppDb.py:299
- `async query_documents()` (instance) - classes\DomoAppDb.py:323

### AppDbDocument

**Total methods:** 3

- `async create_document()` (classmethod) - classes\DomoAppDb.py:187
- `async update_document()` (instance) - classes\DomoAppDb.py:216
- `async upsert()` (classmethod) - classes\DomoAppDb.py:375

### Dataset_PDP_Policies

**Total methods:** 6

- `async get_policies()` (instance) - classes\DomoDataset_PDP.py:178
- `async search_pdp_policies()` (classmethod) - classes\DomoDataset_PDP.py:226
- `async toggle_dataset_pdp()` (instance) - classes\DomoDataset_PDP.py:310
- `async get_policies()` (instance) - classes\DomoPDP.py:178
- `async search_pdp_policies()` (classmethod) - classes\DomoPDP.py:226
- `async toggle_dataset_pdp()` (instance) - classes\DomoPDP.py:310

### DomoAccount_Credential

**Total methods:** 4

- `async get_target_user()` (instance) - classes\DomoAccount_Credential.py:263
- `async update_target_user_password()` (instance) - classes\DomoAccount_Credential.py:297
- `async get_target_access_token()` (instance) - classes\DomoAccount_Credential.py:338
- `async regenerate_target_access_token()` (instance) - classes\DomoAccount_Credential.py:385

### DomoAccount_Default

**Total methods:** 5

- `async upsert_target_account()` (instance) - classes\DomoAccount.py:314
- `async create_account()` (classmethod) - classes\DomoAccount_Default.py:245
- `async update_name()` (instance) - classes\DomoAccount_Default.py:276
- `async delete_account()` (instance) - classes\DomoAccount_Default.py:308
- `async update_config()` (instance) - classes\DomoAccount_Default.py:339

### DomoAccounts

**Total methods:** 2

- `async get_oauths()` (instance) - classes\DomoAccount.py:185
- `async upsert_account()` (classmethod) - classes\DomoAccount.py:214

### DomoAppStudio

**Total methods:** 4

- `async _from_adminsummary()` (classmethod) - classes\DomoAppStudio.py:132
- `async get_accesslist()` (instance) - classes\DomoAppStudio.py:197
- `async share()` (instance) - classes\DomoAppStudio.py:255
- `async add_appstudio_owner()` (classmethod) - classes\DomoAppStudio.py:284

### DomoApplication

**Total methods:** 4

- `async get_by_id()` (classmethod) - classes\DomoApplication.py:78
- `async get_jobs()` (instance) - classes\DomoApplication.py:102
- `async get_schedules()` (instance) - classes\DomoApplication.py:128
- `async find_next_job_schedule()` (instance) - classes\DomoApplication.py:166

### DomoBootstrap

**Total methods:** 4

- `async get_customer_id()` (instance) - classes\DomoBootstrap.py:75
- `async get_pages()` (instance) - classes\DomoBootstrap.py:100
- `async get_features()` (instance) - classes\DomoBootstrap.py:134
- `async is_feature_accountsv2_enabled()` (instance) - classes\DomoBootstrap.py:162

### DomoCard

**Total methods:** 5

- `async get_datasets()` (instance) - classes\DomoCard.py:146
- `async share()` (instance) - classes\DomoCard.py:181
- `async get_collections()` (instance) - classes\DomoCard.py:217
- `async get_source_code()` (instance) - classes\DomoCard.py:247
- `async download_source_code()` (instance) - classes\DomoCard.py:285

### DomoCodeEngine_Package

**Total methods:** 1

- `async get_current_version_by_id()` (classmethod) - classes\DomoCodeEngine.py:382

### DomoCodeEngine_PackageVersion

**Total methods:** 1

- `export()` (instance) - classes\DomoCodeEngine.py:267

### DomoDatacenter

**Total methods:** 6

- `async search_datacenter()` (instance) - classes\DomoDatacenter.py:27
- `async search_datasets()` (instance) - classes\DomoDatacenter.py:58
- `async get_accounts()` (instance) - classes\DomoDatacenter.py:98
- `async search_cards()` (instance) - classes\DomoDatacenter.py:153
- `async get_cards_admin_summary()` (instance) - classes\DomoDatacenter.py:198
- `async search_codeengine()` (instance) - classes\DomoDatacenter.py:247

### DomoDataflow

**Total methods:** 6

- `async get_definition()` (instance) - classes\DomoDataflow.py:119
- `async update_dataflow_definition()` (instance) - classes\DomoDataflow.py:147
- `async get_jupyter_config()` (instance) - classes\DomoDataflow.py:167
- `async execute()` (instance) - classes\DomoDataflow.py:200
- `async get_by_version_id()` (classmethod) - classes\DomoDataflow.py:216
- `async get_versions()` (instance) - classes\DomoDataflow.py:250

### DomoDataflow_Action

**Total methods:** 1

- `get_parents()` (instance) - classes\DomoDataflow_Action.py:68

### DomoDataflow_History

**Total methods:** 1

- `async get_execution_history()` (instance) - classes\DomoDataflow_History.py:154

### DomoDataflow_History_Execution

**Total methods:** 2

- `async get_by_id()` (classmethod) - classes\DomoDataflow_History.py:81
- `async get_actions()` (instance) - classes\DomoDataflow_History.py:110

### DomoDataset_Default

**Total methods:** 11

- `async query_dataset_private()` (instance) - classes\DomoDataset.py:189
- `async delete()` (instance) - classes\DomoDataset.py:252
- `async share()` (instance) - classes\DomoDataset.py:271
- `async index_dataset()` (instance) - classes\DomoDataset.py:301
- `async upload_data()` (instance) - classes\DomoDataset.py:317
- `async list_partitions()` (instance) - classes\DomoDataset.py:445
- `async create()` (classmethod) - classes\DomoDataset.py:466
- `async delete_partition()` (instance) - classes\DomoDataset.py:501
- `async reset_dataset()` (instance) - classes\DomoDataset.py:572
- `async upsert_connector()` (instance) - classes\DomoDataset.py:632
- `_is_federated_dataset_obj()` (instance) - classes\DomoDataset.py:656

### DomoDataset_Schema

**Total methods:** 6

- `async _test_missing_columns()` (instance) - classes\DomoDataset_Schema.py:146
- `async reset_col_order()` (instance) - classes\DomoDataset_Schema.py:173
- `add_col()` (instance) - classes\DomoDataset_Schema.py:190
- `remove_col()` (instance) - classes\DomoDataset_Schema.py:206
- `async alter_schema()` (instance) - classes\DomoDataset_Schema.py:233
- `async alter_schema_descriptions()` (instance) - classes\DomoDataset_Schema.py:262

### DomoGroup

**Total methods:** 3

- `async create_from_name()` (classmethod) - classes\DomoGroup.py:143
- `async update_metadata()` (instance) - classes\DomoGroup.py:175
- `async delete()` (instance) - classes\DomoGroup.py:227

### DomoGroups

**Total methods:** 3

- `async get()` (instance) - classes\DomoGroup.py:313
- `async search_by_name()` (instance) - classes\DomoGroup.py:350
- `async upsert()` (instance) - classes\DomoGroup.py:401

### DomoInstanceConfig

**Total methods:** 20

- `async get_applications()` (instance) - classes\DomoInstanceConfig.py:79
- `async generate_applications_report()` (instance) - classes\DomoInstanceConfig.py:105
- `async get_authorized_domains()` (instance) - classes\DomoInstanceConfig.py:141
- `async set_authorized_domains()` (instance) - classes\DomoInstanceConfig.py:160
- `async upsert_authorized_domains()` (instance) - classes\DomoInstanceConfig.py:181
- `async get_authorized_custom_app_domains()` (instance) - classes\DomoInstanceConfig.py:206
- `async set_authorized_custom_app_domains()` (instance) - classes\DomoInstanceConfig.py:231
- `async upsert_authorized_custom_app_domains()` (instance) - classes\DomoInstanceConfig.py:251
- `async get_sandbox_is_same_instance_promotion_enabled()` (instance) - classes\DomoInstanceConfig.py:275
- `async toggle_sandbox_allow_same_instance_promotion()` (instance) - classes\DomoInstanceConfig.py:300
- `async get_is_user_invite_notification_enabled()` (instance) - classes\DomoInstanceConfig.py:328
- `async toggle_is_user_invite_notification_enabled()` (instance) - classes\DomoInstanceConfig.py:357
- `async get_is_invite_social_users_enabled()` (instance) - classes\DomoInstanceConfig.py:398
- `async toggle_is_invite_social_users_enabled()` (instance) - classes\DomoInstanceConfig.py:439
- `async get_is_weekly_digest_enabled()` (instance) - classes\DomoInstanceConfig.py:472
- `async toggle_is_weekly_digest_enabled()` (instance) - classes\DomoInstanceConfig.py:498
- `async toggle_is_left_nav_enabled()` (instance) - classes\DomoInstanceConfig.py:541
- `async get_is_left_nav_enabled()` (instance) - classes\DomoInstanceConfig.py:569
- `async toggle_is_left_nav_enabled()` (instance) - classes\DomoInstanceConfig.py:595
- `async get_is_left_nav_enabled()` (instance) - classes\DomoInstanceConfig.py:623

### DomoJob_Base

**Total methods:** 7

- `_from_dict()` (classmethod) - classes\DomoApplication_Job_Base.py:144
- `async _get_by_id()` (classmethod) - classes\DomoApplication_Job_Base.py:160
- `async get_by_id()` (classmethod) - classes\DomoApplication_Job_Base.py:201
- `_generate_to_dict()` (instance) - classes\DomoApplication_Job_Base.py:230
- `to_dict()` (instance) - classes\DomoApplication_Job_Base.py:257
- `async update()` (instance) - classes\DomoApplication_Job_Watchdog.py:242
- `async execute()` (instance) - classes\DomoApplication_Job_Watchdog.py:264

### DomoJob_RemoteDomoStats

**Total methods:** 1

- `async create()` (classmethod) - classes\DomoApplication_Job_RemoteDomoStats.py:137

### DomoJob_Watchdog

**Total methods:** 1

- `async create()` (classmethod) - classes\DomoApplication_Job_Watchdog.py:285

### DomoJupyterWorkspace

**Total methods:** 15

- `async get_current_workspace()` (classmethod) - classes\DomoJupyter.py:267
- `async get_account_configuration()` (instance) - classes\DomoJupyter.py:287
- `async get_input_configuration()` (instance) - classes\DomoJupyter.py:308
- `async get_output_configuration()` (instance) - classes\DomoJupyter.py:327
- `_add_config()` (instance) - classes\DomoJupyter.py:346
- `add_config_input_datasource()` (instance) - classes\DomoJupyter.py:363
- `add_config_output_datasource()` (instance) - classes\DomoJupyter.py:373
- `add_config_account()` (instance) - classes\DomoJupyter.py:383
- `_test_config_duplicates()` (instance) - classes\DomoJupyter.py:483
- `async update_config()` (instance) - classes\DomoJupyter.py:494
- `async add_account()` (instance) - classes\DomoJupyter.py:521
- `async add_input_dataset()` (instance) - classes\DomoJupyter.py:585
- `async add_output_dataset()` (instance) - classes\DomoJupyter.py:636
- `async get_content()` (instance) - classes\DomoJupyter.py:685
- `async download_workspace_content()` (instance) - classes\DomoJupyter.py:712

### DomoJupyter_Account

**Total methods:** 2

- `async regenerate_failed_password()` (instance) - classes\DomoJupyter_Account.py:255
- `async regenerate_failed_token()` (instance) - classes\DomoJupyter_Account.py:321

### DomoPage

**Total methods:** 12

- `async _from_adminsummary()` (classmethod) - classes\DomoPage.py:229
- `async _from_bootstrap()` (classmethod) - classes\DomoPage.py:281
- `async get_children()` (instance) - classes\DomoPage.py:362
- `flatten_children()` (instance) - classes\DomoPage.py:409
- `async get_parents()` (instance) - classes\DomoPage.py:426
- `async test_page_access()` (instance) - classes\DomoPage.py:480
- `async get_accesslist()` (instance) - classes\DomoPage.py:526
- `async share()` (instance) - classes\DomoPage.py:659
- `async get_cards()` (instance) - classes\DomoPage.py:690
- `async get_datasets()` (instance) - classes\DomoPage.py:720
- `async update_layout()` (classmethod) - classes\DomoPage.py:747
- `async add_owner()` (instance) - classes\DomoPage.py:782

### DomoPublication

**Total methods:** 5

- `async create_publication()` (classmethod) - classes\DomoPublish.py:290
- `async update_publication()` (instance) - classes\DomoPublish.py:335
- `async get_content()` (instance) - classes\DomoPublish.py:514
- `async report_content_as_dataframe()` (instance) - classes\DomoPublish.py:665
- `report_lineage_as_dataframe()` (instance) - classes\DomoPublish.py:687

### DomoRole

**Total methods:** 9

- `async get_grants()` (instance) - classes\DomoRole.py:102
- `async set_grants()` (instance) - classes\DomoRole.py:140
- `async create()` (classmethod) - classes\DomoRole.py:186
- `async get_membership()` (instance) - classes\DomoRole.py:220
- `async add_user()` (instance) - classes\DomoRole.py:262
- `async update()` (instance) - classes\DomoRole.py:302
- `async delete()` (instance) - classes\DomoRole.py:345
- `async delete_role()` (classmethod) - classes\DomoRole.py:363
- `async set_as_default_role()` (instance) - classes\DomoRole.py:574

### DomoRoles

**Total methods:** 2

- `async create()` (instance) - classes\DomoRole.py:496
- `async upsert()` (instance) - classes\DomoRole.py:520

### DomoTags

**Total methods:** 2

- `async add()` (instance) - classes\DomoTag.py:99
- `async remove()` (instance) - classes\DomoTag.py:119

### DomoUser

**Total methods:** 14

- `async get_role()` (instance) - classes\DomoUser.py:151
- `async get_by_id()` (classmethod) - classes\DomoUser.py:171
- `async download_avatar()` (instance) - classes\DomoUser.py:216
- `async update_properties()` (instance) - classes\DomoUser.py:257
- `async set_user_landing_page()` (instance) - classes\DomoUser.py:285
- `async create()` (classmethod) - classes\DomoUser.py:303
- `async delete()` (instance) - classes\DomoUser.py:344
- `async reset_password()` (instance) - classes\DomoUser.py:365
- `async request_password_reset()` (classmethod) - classes\DomoUser.py:390
- `async upload_avatar()` (instance) - classes\DomoUser.py:413
- `async upsert_avatar()` (instance) - classes\DomoUser.py:447
- `async toggle_direct_signon_access()` (instance) - classes\DomoUser.py:478
- `async get_api_clients()` (instance) - classes\DomoUser.py:500
- `async get_access_tokens()` (instance) - classes\DomoUser.py:541

### DomoUsers

**Total methods:** 9

- `async get()` (instance) - classes\DomoUser.py:629
- `async all_users()` (classmethod) - classes\DomoUser.py:654
- `async search_by_email()` (instance) - classes\DomoUser.py:692
- `async by_email()` (classmethod) - classes\DomoUser.py:743
- `async by_id()` (classmethod) - classes\DomoUser.py:792
- `async virtual_user_by_subscriber_instance()` (classmethod) - classes\DomoUser.py:839
- `async create_user()` (classmethod) - classes\DomoUser.py:860
- `async upsert()` (instance) - classes\DomoUser.py:899
- `async upsert_user()` (classmethod) - classes\DomoUser.py:971

### GroupMembership

**Total methods:** 7

- `async add_members()` (instance) - classes\DomoMembership.py:268
- `async remove_members()` (instance) - classes\DomoMembership.py:298
- `async set_members()` (instance) - classes\DomoMembership.py:328
- `async add_owners()` (instance) - classes\DomoMembership.py:372
- `async remove_owners()` (instance) - classes\DomoMembership.py:402
- `async set_owners()` (instance) - classes\DomoMembership.py:432
- `async add_owner_manage_all_groups_role()` (instance) - classes\DomoMembership.py:490

### Image

**Total methods:** 4

- `to_bytes()` (instance) - utils\Image.py:50
- `crop_square()` (instance) - utils\Image.py:64
- `from_image_file()` (classmethod) - utils\Image.py:84
- `from_bytestr()` (classmethod) - utils\Image.py:99

### Logger

**Total methods:** 5

- `_add_log()` (instance) - client\Logger.py:165
- `log_info()` (instance) - client\Logger.py:208
- `log_error()` (instance) - client\Logger.py:228
- `log_warning()` (instance) - client\Logger.py:249
- `output_log()` (instance) - client\Logger.py:270

### MFA_Config

**Total methods:** 7

- `_test_need_update_config()` (instance) - classes\DomoInstanceConfig_MFA.py:102
- `async toggle_mfa()` (instance) - classes\DomoInstanceConfig_MFA.py:119
- `async enable()` (instance) - classes\DomoInstanceConfig_MFA.py:155
- `async disable()` (instance) - classes\DomoInstanceConfig_MFA.py:173
- `async set_max_code_attempts()` (instance) - classes\DomoInstanceConfig_MFA.py:191
- `async set_num_days_valid()` (instance) - classes\DomoInstanceConfig_MFA.py:227
- `async update()` (instance) - classes\DomoInstanceConfig_MFA.py:262

### PDP_Parameter

**Total methods:** 4

- `generate_parameter_simple()` (instance) - classes\DomoDataset_PDP.py:34
- `generate_body_from_parameter()` (instance) - classes\DomoDataset_PDP.py:46
- `generate_parameter_simple()` (instance) - classes\DomoPDP.py:34
- `generate_body_from_parameter()` (instance) - classes\DomoPDP.py:46

### PDP_Policy

**Total methods:** 4

- `generate_body_from_policy()` (instance) - classes\DomoDataset_PDP.py:143
- `async delete_policy()` (instance) - classes\DomoDataset_PDP.py:291
- `generate_body_from_policy()` (instance) - classes\DomoPDP.py:143
- `async delete_policy()` (instance) - classes\DomoPDP.py:291

### ResponseGetData

**Total methods:** 3

- `_from_requests_response()` (classmethod) - client\ResponseGetData.py:49
- `_from_httpx_response()` (classmethod) - client\ResponseGetData.py:74
- `async _from_looper()` (classmethod) - client\ResponseGetData.py:171

### UserAttribute

**Total methods:** 1

- `async update()` (instance) - classes\DomoInstanceConfig_UserAttribute.py:89

### UserAttributes

**Total methods:** 3

- `async create()` (instance) - classes\DomoInstanceConfig_UserAttribute.py:158
- `async upsert()` (instance) - classes\DomoInstanceConfig_UserAttribute.py:198
- `async delete()` (instance) - classes\DomoInstanceConfig_UserAttribute.py:264

### dmee.DomoEnum

**Total methods:** 2

- `generate_alt_search_str()` (instance) - classes\DomoAccount_Config.py:702
- `generate_alt_search_str()` (instance) - classes\DomoAccount_OAuth.py:24

## Implementation Checklist

For each file:

- [ ] Backup original file
- [ ] Move all @patch_to methods into their target classes
- [ ] Add @classmethod decorators where needed
- [ ] Remove explicit self/cls type hints
- [ ] Add forward reference quotes to return types
- [ ] Remove @patch_to imports if no longer needed
- [ ] Test syntax: `python -m py_compile filename.py`
- [ ] Test imports work
- [ ] Run linting

## Quality Assurance

After refactoring:

```bash
# Test all imports work
python -c "import src; print('All imports successful')"

# Run linting
.\scripts\lint.ps1

# Check for remaining @patch_to usage
findstr /s /n "@patch_to" src\*.py
```
