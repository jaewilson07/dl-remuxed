__all__ = ["DomoInstanceConfig"]

<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py

from dataclasses import dataclass, field
from typing import List

import httpx
import pandas as pd
from nbdev.showdoc import patch_to

from ..classes.DomoInstanceConfig_InstanceSwitcher import (
    DomoInstanceConfig_InstanceSwitcher,
)
from ..client import DomoAuth as dmda
from ..client import exceptions as dmde
from ..routes import application as application_routes
from ..routes import instance_config as instance_config_routes
from ..routes import sandbox as sandbox_routes
from . import DomoAccessToken as dmat
from . import DomoAccount as dmac
from . import DomoAllowlist as dmal
from . import DomoDataset_Connector as dmdsc
from . import DomoGrant as dmgr
from . import DomoInstanceConfig_ApiClient as dicli
from . import DomoInstanceConfig_MFA as dimfa
from . import DomoInstanceConfig_SSO as dicsso
from . import DomoInstanceConfig_UserAttribute as dicua
from . import DomoPublish as dmpb
from . import DomoRole as dmrl
from ..client import auth as dmda
from ..client import exceptions as dmde
from ..routes import application as application_routes
from ..routes import instance_config as instance_config_routes
from ..routes import sandbox as sandbox_routes
from ..classes.DomoInstanceConfig_InstanceSwitcher import (
    DomoInstanceConfig_InstanceSwitcher,
)


========
=======
>>>>>>> main

from dataclasses import dataclass, field
from typing import List

import httpx
import pandas as pd

from ..classes.DomoInstanceConfig_InstanceSwitcher import (
    DomoInstanceConfig_InstanceSwitcher,
)
from ..client import DomoAuth as dmda, auth as dmda, exceptions as dmde
from ..routes import (
    application as application_routes,
    instance_config as instance_config_routes,
    sandbox as sandbox_routes,
)
from . import (
    MFA as dimfa,
    SSO as dicsso,
    Allowlist as dmal,
    ApiClient as dicli,
    DomoAccessToken as dmat,
    DomoAccount as dmac,
    DomoDataset_Connector as dmdsc,
    DomoGrant as dmgr,
    DomoPublish as dmpb,
    DomoRole as dmrl,
    UserAttribute as dicua,
)


<<<<<<< HEAD
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
=======
>>>>>>> main
@dataclass
class DomoInstanceConfig:
    """utility class that absorbs many of the domo instance configuration methods"""

    auth: DomoAuth = field(repr=False)

    allowlist: list[str] = field(default_factory=list)

    is_sandbox_self_instance_promotion_enabled: bool = field(default=None)
    is_user_invite_notification_enabled: bool = field(default=None)
    is_invite_social_users_enabled: bool = field(default=None)
    is_use_left_nav: bool = field(default=None)

    Accounts: dmac.DomoAccounts = field(default=None)
    AccessTokens: dmat.DomoAccessTokens = field(default=None)
    Allowlist: dmal.DomoAllowlist = field(default=None)
    ApiClients: dicli.ApiClients = field(default=None)

    Connectors: dmdsc.DomoConnectors = field(default=None)
    InstanceSwitcher: DomoInstanceConfig_InstanceSwitcher = field(default=None)

    Grants: dmgr.DomoGrants = field(default=None)

    MFA: dimfa.MFA_Config = field(default=None)
    Roles: dmrl.DomoRoles = field(default=None)

    SSO: dicsso.SSO_Config = field(default=None)
    Everywhere: dmpb.DomoEverywhere = field(default=None)
    UserAttributes: dicua.UserAttributes = field(default=None)

    def __post_init__(self):
        self.Accounts = dmac.DomoAccounts(auth=self.auth)
        self.AccessTokens = dmat.DomoAccessTokens(auth=self.auth)
        self.ApiClients = dicli.ApiClients(auth=self.auth)
        self.Allowlist = dmal.DomoAllowlist(auth=self.auth)

        self.Connectors = dmdsc.DomoConnectors(auth=self.auth)
        self.Grants = dmgr.DomoGrants(auth=self.auth)
        self.InstanceSwitcher = DomoInstanceConfig_InstanceSwitcher(auth=self.auth)
        self.MFA = dimfa.MFA_Config(auth=self.auth)
        self.Everywhere = dmpb.DomoEverywhere(auth=self.auth)
        self.UserAttributes = dicua.UserAttributes(auth=self.auth)
        self.Roles = dmrl.DomoRoles(auth=self.auth)
        self.SSO = dicsso.SSO(auth=self.auth)


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_applications(
=======
    async def get_applications(
>>>>>>> main
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
<<<<<<< HEAD
):
=======
        ):
>>>>>>> main
    from . import DomoApplication as dmapp

    res = await application_routes.get_applications(
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    return [
        dmapp.DomoApplication.from_dict(job, auth=self.auth) for job in res.response
    ]


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def generate_applications_report(
=======
    async def generate_applications_report(
>>>>>>> main
    self,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
<<<<<<< HEAD
):
=======
        ):
>>>>>>> main
    domo_apps = await self.get_applications(
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        return_raw=return_raw,
    )

    if return_raw:
        return domo_apps

    df = pd.DataFrame([app.__dict__ for app in domo_apps])
    df["domo_instance"] = self.auth.domo_instance

    df.drop(columns=["auth"], inplace=True)
    df.rename(
        columns={
            "id": "application_id",
            "name": "application_name",
            "description": "application_description",
            "version": "application_version",
        },
        inplace=True,
    )

    return df.sort_index(axis=1)


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_authorized_domains(
=======
    async def get_authorized_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
        ) -> List[str]:
    """returns a list of authorized domains (str) does not update instance_config"""

    res = await instance_config_routes.get_authorized_domains(
        auth=self.auth, debug_api=debug_api, session=session, return_raw=return_raw
    )

    if return_raw:
        return res

    return res.response


<<<<<<< HEAD
async def set_authorized_domains(
=======
    async def set_authorized_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    authorized_domains: List[str],
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
<<<<<<< HEAD
):
=======
        ):
>>>>>>> main
    res = await instance_config_routes.set_authorized_domains(
        auth=self.auth,
        authorized_domain_ls=authorized_domains,
        debug_api=debug_api,
        session=session,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    return res


<<<<<<< HEAD
async def upsert_authorized_domains(
=======
    async def upsert_authorized_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    authorized_domains: List[str],
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
<<<<<<< HEAD
):
=======
        ):
>>>>>>> main
    existing_domains = await self.get_authorized_domains(
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
    )

    authorized_domains += existing_domains

    return await self.set_authorized_domains(
        authorized_domains=authorized_domains,
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
    )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_authorized_custom_app_domains(
=======
    async def get_authorized_custom_app_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
<<<<<<< HEAD
) -> List[str]:
=======
        ) -> List[str]:
>>>>>>> main
    res = await instance_config_routes.get_authorized_custom_app_domains(
        auth=self.auth,
        debug_api=debug_api,
        session=session,
        return_raw=return_raw,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    return res.response


<<<<<<< HEAD
# | exporti
async def set_authorized_custom_app_domains(
=======
        # | exporti
    async def set_authorized_custom_app_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    authorized_domains: List[str],
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
        ):
    res = await instance_config_routes.set_authorized_custom_app_domains(
        auth=self.auth,
        authorized_custom_app_domain_ls=authorized_domains,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=self.__class__.__name__,
    )

    return res


<<<<<<< HEAD
async def upsert_authorized_custom_app_domains(
=======
    async def upsert_authorized_custom_app_domains(
>>>>>>> main
    self: DomoInstanceConfig,
    authorized_domains: List[str],
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    session: httpx.AsyncClient = None,
        ):
    existing_domains = await self.get_authorized_custom_app_domains(
        debug_api=debug_api,
        session=session,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
    )

    authorized_domains += existing_domains

    return await self.set_authorized_custom_app_domains(
        authorized_custom_app_domain_ls=authorized_domains,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        session=session,
    )


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_sandbox_is_same_instance_promotion_enabled(
=======
    async def get_sandbox_is_same_instance_promotion_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
<<<<<<< HEAD
):
=======
        ):
>>>>>>> main
    res = await sandbox_routes.get_is_allow_same_instance_promotion_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    self.is_sandbox_self_instance_promotion_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def toggle_sandbox_allow_same_instance_promotion(
=======
    async def toggle_sandbox_allow_same_instance_promotion(
>>>>>>> main
    self: DomoInstanceConfig,
    is_enabled: bool,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
    debug_num_stacks_to_drop=2,
        ):
    """will enable or disable same instance promotion for sandbox"""

    res = await sandbox_routes.toggle_allow_same_instance_promotion(
        auth=self.auth,
        session=session,
        is_enabled=is_enabled,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    res_is_enabled = await self.get_sandbox_is_same_instance_promotion_enabled()

    if return_raw:
        return res

    return res_is_enabled


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_is_user_invite_notification_enabled(
=======
    async def get_is_user_invite_notification_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
        ):
    """
    Admin > Company Settings > Admin Notifications
    Toggles whether user recieves 'You've been Domo'ed email
    """

    res = await instance_config_routes.get_is_user_invite_notifications_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    self.is_user_invite_notification_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response


<<<<<<< HEAD
async def toggle_is_user_invite_notification_enabled(
=======
    async def toggle_is_user_invite_notification_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    is_enabled: bool,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop: int = 2,
    return_raw: bool = False,
        ):
    res_is_enabled = await self.get_is_user_invite_notification_enabled()

    if is_enabled == self.is_user_invite_notification_enabled:
        return res_is_enabled

    res = await instance_config_routes.toggle_is_user_invite_enabled(
        auth=self.auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    res_is_enabled = await self.get_is_user_invite_notification_enabled()

    if return_raw:
        return res

    return res_is_enabled


<<<<<<< HEAD
class InstanceConfig_ClassError(dmde.ClassError):
=======
    class InstanceConfig_ClassError(dmde.ClassError):
>>>>>>> main
    def __init__(self, cls_instance, message):
        super().__init__(
            cls_instance=cls_instance,
            message=message,
            entity_id=cls_instance.auth.domo_instance,
        )


<<<<<<< HEAD
async def get_is_invite_social_users_enabled(
=======
    async def get_is_invite_social_users_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    customer_id: str = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
        ):
    """checks if users can be invited as social users to the instaance"""

    if not customer_id:
        from . import DomoBootstrap as dmbp

        try:
            bs = dmbp.DomoBootstrap(auth=self.auth)
            customer_id = await bs.get_customer_id()

        except dmda.InvalidAuthTypeError as e:
            raise InstanceConfig_ClassError(
                self,
                message=f"{e.__class__.__name__} -- bootstrap API requires FullAuth OR pass customer_id",
            ) from e

    res = await instance_config_routes.get_is_invite_social_users_enabled(
        auth=self.auth,
        customer_id=customer_id,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    self.is_invite_social_users_enabled = res.response["is_enabled"]

    if return_raw:
        return res

    return res.response


<<<<<<< HEAD
async def toggle_is_invite_social_users_enabled(
=======
    async def toggle_is_invite_social_users_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    is_enabled: bool,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
        ):
    """enables or disables the ability to invite users to instance as social users"""

    res_is_enabled = await self.get_is_invite_social_users_enabled()

    if is_enabled == self.is_invite_social_users_enabled:
        return res_is_enabled

    res = await instance_config_routes.toggle_is_social_users_enabled(
        auth=self.auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    res_is_enabled = await self.get_is_invite_social_users_enabled()

    if return_raw:
        return res

    return res_is_enabled


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_is_weekly_digest_enabled(
=======
    async def get_is_weekly_digest_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    return_raw: bool = False,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    session: httpx.AsyncClient = None,
        ):
    """the weekly digest is a weekly email from Domo of changes to the instance"""

    res = await instance_config_routes.get_is_weekly_digest_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    self.is_weekly_digest_enabled = res.response["is_enabled"]

    return res.response


<<<<<<< HEAD
async def toggle_is_weekly_digest_enabled(
=======
    async def toggle_is_weekly_digest_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    is_enabled: bool,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_prn: bool = False,
    debug_num_stacks_to_drop=2,
        ):
    """toggles if weekly digest is enabled or disabled"""

    res_is_enabled = await self.get_is_weekly_digest_enabled()

    if is_enabled == self.is_weekly_digest_enabled:
        if debug_prn:
            print(
                f"weekly digest is already {'enabled' if is_enabled else 'disabled'} in {self.auth.domo_instance}"
            )
        return res_is_enabled

    if debug_prn:
        print(
            f"{'enabling' if is_enabled else 'disabling'} weekly digest {self.auth.domo_instance}"
        )

    res = await instance_config_routes.toggle_is_weekly_digest_enabled(
        auth=self.auth,
        is_enabled=is_enabled,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    res_is_enabled = await self.get_is_weekly_digest_enabled()

    if return_raw:
        return res

    return res_is_enabled


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def toggle_is_left_nav_enabled(
=======
    async def toggle_is_left_nav_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    is_use_left_nav: bool = True,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
        ):
    """toggles the use of the left nav in Domo"""

    res = await instance_config_routes.toggle_is_left_nav_enabled(
        auth=self.auth,
        is_use_left_nav=is_use_left_nav,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    self.is_use_left_nav = res.response["is_enabled"]

    return res


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_is_left_nav_enabled(
=======
    async def get_is_left_nav_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
        ):
    """gets the use of the left nav in Domo"""

    res = await instance_config_routes.get_is_left_nav_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    self.is_use_left_nav = res.response["is_enabled"]

    return res


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def toggle_is_left_nav_enabled(
=======
    async def toggle_is_left_nav_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    is_use_left_nav: bool = True,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
        ):
    """toggles the use of the left nav in Domo"""

    res = await instance_config_routes.toggle_is_left_nav_enabled(
        auth=self.auth,
        is_use_left_nav=is_use_left_nav,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    self.is_use_left_nav = res.response["is_enabled"]

    return res


<<<<<<< HEAD
<<<<<<<< HEAD:src/classes/DomoInstanceConfig.py
@patch_to(DomoInstanceConfig)
========
>>>>>>>> test:src/domolibrary2/classes/DomoInstanceConfig/IstanceConfig.py
async def get_is_left_nav_enabled(
=======
    async def get_is_left_nav_enabled(
>>>>>>> main
    self: DomoInstanceConfig,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
        ):
    """gets the use of the left nav in Domo"""

    res = await instance_config_routes.get_is_left_nav_enabled(
        auth=self.auth,
        session=session,
        debug_api=debug_api,
        parent_class=self.__class__.__name__,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
    )

    if return_raw:
        return res

    self.is_use_left_nav = res.response["is_enabled"]

    return res
