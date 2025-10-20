# Classes module - automatically imports all class modules
# Users can do: from domolibrary2.classes import DomoUser
# Or: import domolibrary2.classes.DomoUser as DomoUser

# Import all class modules
from . import CodeEngineManifest
from . import CodeEngineManifest_Argument
from . import CodeEngineManifest_Function
from . import DomoAccess
from . import DomoAccessToken
from . import DomoAccount
from . import DomoAccount_Config
from . import DomoAccount_Credential
from . import DomoAccount_Default
from . import DomoAccount_OAuth
from . import DomoActivityLog
from . import DomoAllowlist
from . import DomoAppDb
from . import DomoAppStudio
from . import DomoApplication
from . import DomoApplication_Job
from . import DomoApplication_Job_Base
from . import DomoApplication_Job_RemoteDomoStats
from . import DomoApplication_Job_Watchdog
from . import DomoBootstrap
from . import DomoCard
from . import DomoCertification
from . import DomoCodeEngine
from . import DomoDatacenter
from . import DomoDataflow
from . import DomoDataflow_Action
from . import DomoDataflow_History
from . import DomoDataset
from . import DomoDataset_Connector
from . import DomoDataset_PDP
from . import DomoDataset_Schema
from . import DomoDataset_Stream
from . import DomoGrant
from . import DomoGroup
from . import DomoInstanceConfig
from . import DomoInstanceConfig_ApiClient
from . import DomoInstanceConfig_InstanceSwitcher
from . import DomoInstanceConfig_MFA
from . import DomoInstanceConfig_SSO
from . import DomoInstanceConfig_Scheduler_Policies
from . import DomoInstanceConfig_UserAttribute
from . import DomoIntegration
from . import DomoJupyter
from . import DomoJupyter_Account
from . import DomoJupyter_Content
from . import DomoJupyter_DataSource
from . import DomoLineage
from . import DomoMembership
from . import DomoPDP
from . import DomoPage
from . import DomoPage_Content
from . import DomoPublish
from . import DomoRole
from . import DomoSandbox
from . import DomoTag
from . import DomoUser

# Define what gets imported with "from domolibrary2.classes import *"
__all__ = [
    "CodeEngineManifest",
    "CodeEngineManifest_Argument",
    "CodeEngineManifest_Function",
    "DomoAccess",
    "DomoAccessToken",
    "DomoAccount",
    "DomoAccount_Config",
    "DomoAccount_Credential",
    "DomoAccount_Default",
    "DomoAccount_OAuth",
    "DomoActivityLog",
    "DomoAllowlist",
    "DomoAppDb",
    "DomoAppStudio",
    "DomoApplication",
    "DomoApplication_Job",
    "DomoApplication_Job_Base",
    "DomoApplication_Job_RemoteDomoStats",
    "DomoApplication_Job_Watchdog",
    "DomoBootstrap",
    "DomoCard",
    "DomoCertification",
    "DomoCodeEngine",
    "DomoDatacenter",
    "DomoDataflow",
    "DomoDataflow_Action",
    "DomoDataflow_History",
    "DomoDataset",
    "DomoDataset_Connector",
    "DomoDataset_PDP",
    "DomoDataset_Schema",
    "DomoDataset_Stream",
    "DomoGrant",
    "DomoGroup",
    "DomoInstanceConfig",
    "DomoInstanceConfig_ApiClient",
    "DomoInstanceConfig_InstanceSwitcher",
    "DomoInstanceConfig_MFA",
    "DomoInstanceConfig_SSO",
    "DomoInstanceConfig_Scheduler_Policies",
    "DomoInstanceConfig_UserAttribute",
    "DomoIntegration",
    "DomoJupyter",
    "DomoJupyter_Account",
    "DomoJupyter_Content",
    "DomoJupyter_DataSource",
    "DomoLineage",
    "DomoMembership",
    "DomoPDP",
    "DomoPage",
    "DomoPage_Content",
    "DomoPublish",
    "DomoRole",
    "DomoSandbox",
    "DomoTag",
    "DomoUser",
]
