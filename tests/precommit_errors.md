# Pre-commit Errors

**Total Errors:** 160

## Error Summary

- **E402**: 1 occurrences
- **E721**: 2 occurrences
- **E722**: 2 occurrences
- **F401**: 30 occurrences
- **F403**: 1 occurrences
- **F405**: 4 occurrences
- **F821**: 18 occurrences
- **F822**: 11 occurrences
- **N802**: 2 occurrences
- **N803**: 4 occurrences
- **N806**: 2 occurrences
- **N811**: 1 occurrences
- **N813**: 59 occurrences
- **N815**: 2 occurrences
- **N999**: 20 occurrences
- **YAML**: 1 occurrences

## Errors by File


### .github/workflows/pre-commit.yml (1 errors)

- **[YAML]** Line 30, Col 26: mapping values are not allowed in this context

### src/domolibrary2/__init__.py (2 errors)

- **[F401]** Line 11, Col 35: `dc_logger.client.base.Logger` imported but unused
- **[F401]** Line 11, Col 43: `dc_logger.client.base.get_global_logger` imported but unused

### src/domolibrary2/classes/DomoAccount/config.py (1 errors)

- **[N813]** Line 34, Col 5: Camelcase `DictDot` imported as lowercase `util_dd`

### src/domolibrary2/classes/DomoAppDb.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoAppDb'

### src/domolibrary2/classes/DomoAppStudio.py (5 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoAppStudio'
- **[N813]** Line 12, Col 5: Camelcase `DictDot` imported as lowercase `util_dd`
- **[N813]** Line 15, Col 15: Camelcase `DomoUser` imported as lowercase `dmdu`
- **[N813]** Line 86, Col 23: Camelcase `DomoGroup` imported as lowercase `dmg`
- **[N813]** Line 169, Col 23: Camelcase `DomoGroup` imported as lowercase `dmg`

### src/domolibrary2/classes/DomoApplication/Application.py (5 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Application'
- **[F822]** Line 1, Col 12: Undefined name `DomoJob_Types` in `__all__`
- **[N813]** Line 11, Col 5: Camelcase `DictDot` imported as lowercase `util_dd`
- **[N813]** Line 13, Col 15: Camelcase `Job` imported as lowercase `dmdj`
- **[F821]** Line 72, Col 16: Undefined name `DomoJob_Types`

### src/domolibrary2/classes/DomoApplication/Job.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Job'

### src/domolibrary2/classes/DomoApplication/Job_Base.py (2 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Job_Base'
- **[N802]** Line 137, Col 9: Function name `_convert_API_res_to_DomoJob_base_obj` should be lowercase

### src/domolibrary2/classes/DomoApplication/Job_RemoteDomoStats.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Job_RemoteDomoStats'

### src/domolibrary2/classes/DomoApplication/Job_Watchdog.py (3 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Job_Watchdog'
- **[F821]** Line 199, Col 15: Undefined name `DomoAuth`
- **[F821]** Line 234, Col 15: Undefined name `DomoAuth`

### src/domolibrary2/classes/DomoCard.py (4 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoCard'
- **[N813]** Line 88, Col 13: Camelcase `DomoGroup` imported as lowercase `dmgr`
- **[N813]** Line 89, Col 13: Camelcase `DomoUser` imported as lowercase `dmdu`
- **[N813]** Line 228, Col 23: Camelcase `DomoAppDb` imported as lowercase `dmdb`

### src/domolibrary2/classes/DomoCodeEngine/CodeEngine.py (2 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'CodeEngine'
- **[N813]** Line 45, Col 16: Camelcase `DomoUser` imported as lowercase `dmdu`

### src/domolibrary2/classes/DomoCodeEngine/Manifest.py (2 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Manifest'
- **[F821]** Line 137, Col 13: Undefined name `os`

### src/domolibrary2/classes/DomoCodeEngine/Manifest_Argument.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Manifest_Argument'

### src/domolibrary2/classes/DomoCodeEngine/Manifest_Function.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Manifest_Function'

### src/domolibrary2/classes/DomoDatacenter.py (6 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoDatacenter'
- **[N813]** Line 59, Col 23: Camelcase `DomoDataset` imported as lowercase `dmds`
- **[N813]** Line 113, Col 23: Camelcase `DomoAccount` imported as lowercase `dmac`
- **[N813]** Line 163, Col 23: Camelcase `DomoCard` imported as lowercase `dmc`
- **[N813]** Line 208, Col 23: Camelcase `DomoCard` imported as lowercase `dmc`
- **[N813]** Line 246, Col 37: Camelcase `CodeEngine` imported as lowercase `dmceg`

### src/domolibrary2/classes/DomoDataflow/Dataflow.py (7 errors)

- **[N813]** Line 11, Col 27: Camelcase `Jupyter` imported as lowercase `dmdj`
- **[F821]** Line 22, Col 11: Undefined name `DomoAuth`
- **[F821]** Line 82, Col 15: Undefined name `DomoAuth`
- **[N813]** Line 164, Col 23: Camelcase `DomoJupyter` imported as lowercase `dmdj`
- **[F821]** Line 190, Col 15: Undefined name `DomoAuth`
- **[F821]** Line 205, Col 15: Undefined name `DomoAuth`
- **[F821]** Line 276, Col 11: Undefined name `DomoAuth`

### src/domolibrary2/classes/DomoDataflow/Dataflow_Action.py (1 errors)

- **[N813]** Line 9, Col 5: Camelcase `DictDot` imported as lowercase `util_dd`

### src/domolibrary2/classes/DomoDataset/stream_config.py (2 errors)

- **[F822]** Line 37, Col 5: Undefined name `DomoStream` in `__all__`
- **[E722]** Line 258, Col 9: Do not use bare `except`

### src/domolibrary2/classes/DomoGroup.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoGroup'

### src/domolibrary2/classes/DomoInstanceConfig/__init__.py (12 errors)

- **[F401]** Line 4, Col 5: `.access_token` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 5, Col 5: `.allowlist` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 6, Col 5: `.api_client` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 7, Col 5: `.core` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 8, Col 5: `.instance_switcher` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 9, Col 5: `.mfa` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 10, Col 5: `.role` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 11, Col 5: `.role_grant` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 12, Col 5: `.scheduler_policies` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 13, Col 5: `.sso` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 14, Col 5: `.toggle` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 15, Col 5: `.user_attributes` imported but unused; consider removing, adding to `__all__`, or using a redundant alias

### src/domolibrary2/classes/DomoInstanceConfig/bootstrap.py (1 errors)

- **[N813]** Line 12, Col 16: Camelcase `DomoPage` imported as lowercase `dmpg`

### src/domolibrary2/classes/DomoInstanceConfig/core.py (1 errors)

- **[N811]** Line 30, Col 18: Constant `SSO` imported as non-constant `SSO_Class`

### src/domolibrary2/classes/DomoInstanceConfig/instance_switcher.py (1 errors)

- **[E721]** Line 51, Col 12: Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks

### src/domolibrary2/classes/DomoInstanceConfig/mfa.py (2 errors)

- **[N803]** Line 112, Col 9: Argument name `is_enable_MFA` should be lowercase
- **[N803]** Line 245, Col 9: Argument name `is_enable_MFA` should be lowercase

### src/domolibrary2/classes/DomoInstanceConfig/role_grant.py (2 errors)

- **[N813]** Line 10, Col 28: Camelcase `DomoAuth` imported as lowercase `dmda`
- **[N813]** Line 12, Col 22: Camelcase `DictDot` imported as lowercase `util_dd`

### src/domolibrary2/classes/DomoInstanceConfig/sso.py (2 errors)

- **[N806]** Line 366, Col 9: Variable `OIDC` in function should be lowercase
- **[N806]** Line 383, Col 9: Variable `SAML` in function should be lowercase

### src/domolibrary2/classes/DomoIntegration.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoIntegration'

### src/domolibrary2/classes/DomoJupyter/Account.py (1 errors)

- **[N813]** Line 21, Col 15: Camelcase `Account` imported as lowercase `dmac`

### src/domolibrary2/classes/DomoJupyter/Content.py (1 errors)

- **[N813]** Line 14, Col 22: Camelcase `DictDot` imported as lowercase `util_dd`

### src/domolibrary2/classes/DomoJupyter/DataSource.py (1 errors)

- **[N813]** Line 9, Col 27: Camelcase `DomoDataset` imported as lowercase `dmds`

### src/domolibrary2/classes/DomoJupyter/Jupyter.py (6 errors)

- **[N813]** Line 28, Col 16: Camelcase `DomoUser` imported as lowercase `dmdu`
- **[N813]** Line 29, Col 27: Camelcase `DomoDataset` imported as lowercase `dmds`
- **[N813]** Line 31, Col 5: Camelcase `Account` imported as lowercase `dmac`
- **[F821]** Line 232, Col 15: Undefined name `DomoAuth`
- **[F821]** Line 381, Col 11: Undefined name `DomoAuth`
- **[F821]** Line 498, Col 12: Undefined name `DomoError`

### src/domolibrary2/classes/DomoPage.py (6 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoPage'
- **[F403]** Line 12, Col 1: `from .page import *` used; unable to detect undefined names
- **[F405]** Line 14, Col 12: `DomoPage_GetRecursive` may be undefined, or defined from star imports
- **[F405]** Line 14, Col 37: `DomoPage` may be undefined, or defined from star imports
- **[F405]** Line 14, Col 49: `DomoPages` may be undefined, or defined from star imports
- **[F405]** Line 14, Col 62: `Page_NoAccess` may be undefined, or defined from star imports

### src/domolibrary2/classes/DomoPage/__init__.py (1 errors)

- **[F401]** Line 45, Col 32: `.management` imported but unused; consider removing, adding to `__all__`, or using a redundant alias

### src/domolibrary2/classes/DomoPage/access.py (2 errors)

- **[N813]** Line 16, Col 16: Camelcase `DomoUser` imported as lowercase `dmu`
- **[N813]** Line 137, Col 20: Camelcase `DomoGroup` imported as lowercase `dmg`

### src/domolibrary2/classes/DomoPage/content.py (1 errors)

- **[N813]** Line 23, Col 20: Camelcase `DomoCard` imported as lowercase `dc`

### src/domolibrary2/classes/DomoPage/core.py (7 errors)

- **[N813]** Line 14, Col 5: Camelcase `DictDot` imported as lowercase `util_dd`
- **[N813]** Line 18, Col 5: Camelcase `DomoUser` imported as lowercase `dmu`
- **[F821]** Line 51, Col 18: Undefined name `DomoCard`
- **[F821]** Line 52, Col 21: Undefined name `DomoDataset`
- **[F821]** Line 55, Col 24: Undefined name `dmdl`
- **[N813]** Line 71, Col 24: Camelcase `DomoGroup` imported as lowercase `dmg`
- **[N813]** Line 219, Col 24: Camelcase `DomoCard` imported as lowercase `dmc`

### src/domolibrary2/classes/DomoPage/page_content.py (1 errors)

- **[N815]** Line 57, Col 5: Variable `is_darkMode` in class scope should not be mixedCase

### src/domolibrary2/classes/DomoSandbox.py (4 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DomoSandbox'
- **[N813]** Line 20, Col 24: Camelcase `DomoLineage` imported as lowercase `dmdl`
- **[F821]** Line 24, Col 22: Undefined name `DomoEntity_w_Lineage`
- **[F821]** Line 166, Col 19: Undefined name `DomoManager`

### src/domolibrary2/classes/publish.py (4 errors)

- **[N813]** Line 54, Col 9: Camelcase `DomoAppStudio` imported as lowercase `dmas`
- **[N813]** Line 55, Col 9: Camelcase `DomoCard` imported as lowercase `dmac`
- **[N813]** Line 56, Col 9: Camelcase `DomoDataset` imported as lowercase `dmds`
- **[N813]** Line 57, Col 9: Camelcase `DomoPage` imported as lowercase `dmpg`

### src/domolibrary2/classes/subentity/lineage.py (5 errors)

- **[N813]** Line 105, Col 36: Camelcase `Dataflow` imported as lowercase `dmdf`
- **[N813]** Line 141, Col 24: Camelcase `DomoPublish` imported as lowercase `dmpb`
- **[N813]** Line 175, Col 24: Camelcase `DomoCard` imported as lowercase `dmcd`
- **[N813]** Line 491, Col 28: Camelcase `DomoPage` imported as lowercase `dmpg`
- **[N813]** Line 581, Col 28: Camelcase `DomoPublish` imported as lowercase `dmpb`

### src/domolibrary2/classes/subentity/membership.py (8 errors)

- **[N813]** Line 47, Col 13: Camelcase `DomoGroup` imported as lowercase `dmdg`
- **[N813]** Line 48, Col 13: Camelcase `DomoUser` imported as lowercase `dmdu`
- **[N813]** Line 128, Col 24: Camelcase `DomoGroup` imported as lowercase `dmg`
- **[N813]** Line 145, Col 24: Camelcase `DomoGroup` imported as lowercase `dmg`
- **[N813]** Line 167, Col 24: Camelcase `DomoGroup` imported as lowercase `dmg`
- **[N813]** Line 185, Col 24: Camelcase `DomoUser` imported as lowercase `dmu`
- **[N813]** Line 509, Col 24: Camelcase `DomoGroup` imported as lowercase `dmdg`
- **[N813]** Line 566, Col 24: Camelcase `DomoGroup` imported as lowercase `dmg`

### src/domolibrary2/integrations/Automation.py (4 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'Automation'
- **[N813]** Line 17, Col 5: Camelcase `DomoAccount` imported as lowercase `dmacc`
- **[N813]** Line 18, Col 5: Camelcase `DomoDataset` imported as lowercase `dmds`
- **[N813]** Line 19, Col 5: Camelcase `DomoGroup` imported as lowercase `dmdg`

### src/domolibrary2/integrations/RoleHierarchy.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'RoleHierarchy'

### src/domolibrary2/integrations/shortcut_fn.py (2 errors)

- **[N813]** Line 7, Col 5: Camelcase `DomoAccount` imported as lowercase `dmacc`
- **[N813]** Line 8, Col 5: Camelcase `DomoGroup` imported as lowercase `dmdg`

### src/domolibrary2/routes/auth.py (1 errors)

- **[F822]** Line 14, Col 5: Undefined name `NoAccessTokenReturned` in `__all__`

### src/domolibrary2/routes/datacenter/__init__.py (3 errors)

- **[F401]** Line 14, Col 5: `.exceptions.SearchDatacenterNoResultsFoundError` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[F401]** Line 15, Col 5: `.exceptions.ShareResourceError` imported but unused; consider removing, adding to `__all__`, or using a redundant alias
- **[E402]** Line 25, Col 1: Module level import not at top of file

### src/domolibrary2/routes/datacenter/core.py (1 errors)

- **[N803]** Line 174, Col 5: Argument name `combineResults` should be lowercase

### src/domolibrary2/routes/instance_config/api_client.py (1 errors)

- **[F821]** Line 194, Col 15: Undefined name `InvalidAuthType`

### src/domolibrary2/routes/instance_config/authorized_domains.py (2 errors)

- **[F822]** Line 2, Col 5: Undefined name `GetDomains_NotFound` in `__all__`
- **[F822]** Line 3, Col 5: Undefined name `GetAppDomains_NotFound` in `__all__`

### src/domolibrary2/routes/instance_config/mfa.py (1 errors)

- **[N803]** Line 81, Col 5: Argument name `is_enable_MFA` should be lowercase

### src/domolibrary2/routes/jupyter/exceptions.py (1 errors)

- **[F822]** Line 9, Col 5: Undefined name `SearchJupyterNotFoundError
` in `__all__`

### src/domolibrary2/routes/page/exceptions.py (1 errors)

- **[F822]** Line 9, Col 5: Undefined name `SearchPageNotFoundError` in `__all__`

### src/domolibrary2/routes/pdp.py (1 errors)

- **[F822]** Line 37, Col 5: Undefined name `PDP_NotRetrieved` in `__all__`

### src/domolibrary2/routes/role.py (1 errors)

- **[F822]** Line 2, Col 5: Undefined name `Role_NotRetrieved` in `__all__`

### src/domolibrary2/routes/user/exceptions.py (2 errors)

- **[F822]** Line 22, Col 5: Undefined name `UserSharingError` in `__all__`
- **[F822]** Line 26, Col 5: Undefined name `ResetPasswordPasswordUsedError` in `__all__`

### src/domolibrary2/utils/DictDot.py (1 errors)

- **[N999]** Line 1, Col 1: Invalid module name: 'DictDot'

### src/domolibrary2/utils/images.py (1 errors)

- **[N802]** Line 58, Col 5: Function name `isBase64` should be lowercase

### src/domolibrary2/utils/logging/processors.py (1 errors)

- **[E722]** Line 225, Col 13: Do not use bare `except`

### src/domolibrary2/utils/read_creds_from_dotenv.py (1 errors)

- **[N813]** Line 36, Col 15: Camelcase `DictDot` imported as lowercase `utils_dd`

### src/postman/converter/models.py (1 errors)

- **[N815]** Line 354, Col 5: Variable `originalRequest` in class scope should not be mixedCase

### src/postman/converter/test_models.py (13 errors)

- **[F401]** Line 11, Col 13: `models.PostmanAuth` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 12, Col 13: `models.PostmanCollection` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 13, Col 13: `models.PostmanCollectionInfo` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 14, Col 13: `models.PostmanEvent` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 15, Col 13: `models.PostmanFolder` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 16, Col 13: `models.PostmanQueryParam` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 17, Col 13: `models.PostmanRequest` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 18, Col 13: `models.PostmanRequest_Body` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 19, Col 13: `models.PostmanRequest_Header` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 20, Col 13: `models.PostmanResponse` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 21, Col 13: `models.PostmanScript` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 22, Col 13: `models.PostmanUrl` imported but unused; consider using `importlib.util.find_spec` to test for availability
- **[F401]** Line 23, Col 13: `models.PostmanVariable` imported but unused; consider using `importlib.util.find_spec` to test for availability

### src/postman/converter/validate_structure.py (1 errors)

- **[E721]** Line 34, Col 8: Use `is` and `is not` for type comparisons, or `isinstance()` for isinstance checks
