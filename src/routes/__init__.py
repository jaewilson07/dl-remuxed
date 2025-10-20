# Routes module - automatically imports all route modules
# Users can import route functions like: from domolibrary2.routes import user

# Import all route modules
from . import access_token
from . import account
from . import activity_log
from . import ai
from . import appdb
from . import application
from . import appstudio
from . import auth
from . import beastmode
from . import bootstrap
from . import card
from . import cloud_amplifier
from . import codeengine
from . import codeengine_crud
from . import datacenter
from . import dataflow
from . import dataset
from . import enterprise_apps
from . import filesets
from . import grant
from . import group
from . import instance_config
from . import instance_config_api_client
from . import instance_config_instance_switcher
from . import instance_config_mfa
from . import instance_config_scheduler_policies
from . import instance_config_sso
from . import jupyter
from . import page
from . import pdp
from . import publish
from . import role
from . import sandbox
from . import stream
from . import user
from . import user_attributes
from . import workflows

# Define what gets imported with "from domolibrary2.routes import *"
__all__ = [
    "access_token",
    "account",
    "activity_log",
    "ai",
    "appdb",
    "application",
    "appstudio",
    "auth",
    "beastmode",
    "bootstrap",
    "card",
    "cloud_amplifier",
    "codeengine",
    "codeengine_crud",
    "datacenter",
    "dataflow",
    "dataset",
    "enterprise_apps",
    "filesets",
    "grant",
    "group",
    "instance_config",
    "instance_config_api_client",
    "instance_config_instance_switcher",
    "instance_config_mfa",
    "instance_config_scheduler_policies",
    "instance_config_sso",
    "jupyter",
    "page",
    "pdp",
    "publish",
    "role",
    "sandbox",
    "stream",
    "user",
    "user_attributes",
    "workflows",
]
