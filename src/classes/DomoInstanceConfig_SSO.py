__all__ = [
    "SSOConfig_InstantiationError",
    "SSOConfig_UpdateError",
    "SSO_Config",
    "SSO_OIDC_Config",
    "SSO_SAML_Config",
    "SSO",
]


import json
from abc import abstractmethod
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from pprint import pprint  # pprint _from_dict
from typing import Any, Callable

import httpx

from ..client import auth as dmda
from ..client import DomoError as dmde
from ..client import response as rgd
from ..routes import instance_config_sso as sso_routes
from ..utils import convert as dmcv
from ..client.entities import DomoEntity


class SSOConfig_InstantiationError(dmde.ClassError):
    def __init__(self, message, auth, cls_instance=None):
        super().__init__(auth=auth, message=message, cls_instance=cls_instance)


class SSOConfig_UpdateError(dmde.ClassError):
    def __init__(
        self, errors_obj, res: rgd.ResponseGetData, cls_instance, domo_instance
    ):
        message = json.dumps(errors_obj)
        super().__init__(
            res=res, message=message, cls_instance=cls_instance, entity_id=domo_instance
        )


@dataclass
class SSO_Config(DomoEntity):
    """base class for SAML and OIDC Config"""

    idp_enabled: bool  # False
    enforce_allowlist: bool
    idp_certificate: str

    @property
    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/admin/security/sso?tab=configuration"

    def set_attribute(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise SSOConfig_InstantiationError(
                    message=f"key {key} not part of class", auth=self.auth
                )
            if value is not None:
                setattr(self, key, value)

        return self

    @classmethod
    def _parent_from_dict(
        cls,
        auth: dmda.DomoAuth,
        obj: dict,
        raw: dict,  # raw api response
        debug_prn: bool = False,
        **kwargs: dict,  # parameters that will be passed to the class object (must be attributes of the class)
    ):
        new_obj = {
            dmcv.convert_str_to_snake_case(key, is_pascal=True): value
            for key, value in obj.items()
        }

        idp_enabled = new_obj.pop("idp_enabled")

        if isinstance(idp_enabled, str):
            idp_enabled = dmcv.convert_string_to_bool(idp_enabled)

        enforce_allowlist = new_obj.pop("enforce_whitelist")

        if debug_prn:
            pprint(
                {
                    "new_obj": new_obj,
                    "idp_enabled": idp_enabled,
                    "enforce_allowlist": enforce_allowlist,
                    "kwargs": kwargs,
                }
            )

        sso_cls = cls(
            auth=auth,
            enforce_allowlist=enforce_allowlist,
            idp_enabled=idp_enabled,
            raw=raw,
            **kwargs,
            **new_obj,
        )

        sso_cls.set_attribute(**new_obj)

        return sso_cls

    @classmethod
    @abstractmethod
    async def get():
        raise NotImplementedError("must implement get")

    def _to_dict(
        self,
        generate_alternate_body_fn: Callable = None,
        is_include_undefined: bool = False,
    ):
        obj = asdict(self)
        obj.pop("auth")
        obj.pop("raw")

        if generate_alternate_body_fn:
            return generate_alternate_body_fn(
                **obj, is_include_undefined=is_include_undefined
            )

        return {key: dmcv.convert_snake_to_pascal(value) for key, value in obj.items()}

    def to_dict(self, is_include_undefined: bool = False):
        return self._to_dict(is_include_undefined=is_include_undefined)

    async def _update(
        self,
        update_config_route_fn: Callable,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        debug_is_test: bool = False,
        return_raw: bool = False,
        **kwargs,
    ):
        self.set_attribute(**kwargs)

        body_sso = self.to_dict()

        if debug_is_test:
            print("⚗️⚠️ This is a test, SSO Config will not be updated")
            return body_sso

        res = await update_config_route_fn(
            auth=self.auth,
            body_sso=body_sso,
            parent_class=self.__class__.__name__,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        new_config = await self.get(auth=self.auth)

        errors_obj = {}
        for n_key, current_value in asdict(new_config).items():
            if n_key in ["auth"]:
                continue

            expected_value = getattr(self, n_key)

            if expected_value != current_value:
                errors_obj.update(
                    {
                        "key": n_key,
                        "expected_value": expected_value,
                        "current_value": current_value,
                    }
                )

            self.set_attribute(**{n_key: current_value})

        if errors_obj:
            raise SSOConfig_UpdateError(
                res=res,
                errors_obj=errors_obj,
                cls_instance=self,
                domo_instance=self.auth.domo_instance,
            )

        return self


@dataclass
class SSO_OIDC_Config(SSO_Config):
    login_enabled: bool
    import_groups: bool
    require_invitation: bool
    skip_to_idp: bool
    redirect_url: str  # url
    override_sso: bool
    override_embed: bool
    well_known_config: str

    auth_request_endpoint: str = None  # url
    token_endpoint: str = None
    user_info_endpoint: str = None
    public_key: str = None

    @classmethod
    def _from_dict(cls, auth: dmda.DomoAuth, obj: dict, debug_prn: bool = False):
        raw = deepcopy(obj)

        override_sso = obj.pop("overrideSSO")

        idp_certificate = (
            obj.pop("certificate") if hasattr(obj, "certificate") else None
        )

        return cls._parent_from_dict(
            auth=auth,
            obj=obj,
            raw=raw,
            debug_prn=debug_prn,
            override_sso=override_sso,
            idp_certificate=idp_certificate,
        )

    def to_dict(self, is_include_undefined: bool = False):
        return self._to_dict(
            generate_alternate_body_fn=sso_routes.generate_sso_oidc_body,
            is_include_undefined=is_include_undefined,
        )

    @classmethod
    async def get(
        cls,
        auth: dmda.DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_prn: bool = False,
        return_raw: bool = False,
    ):
        res = await sso_routes.get_sso_oidc_config(
            auth=auth,
            session=session,
            parent_class=cls.__name__,
            debug_api=debug_api,
            debug_num_stacks_to_drop=2,
        )

        if return_raw:
            return res

        return cls._from_dict(auth=auth, obj=res.response, debug_prn=debug_prn)

    async def update(
        self,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        debug_is_test: bool = False,
        return_raw: bool = False,
        **kwargs,
    ):
        return await self._update(
            update_config_route_fn=sso_routes.update_sso_oidc_config,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            debug_is_test=debug_is_test,
            return_raw=return_raw,
            **kwargs,
        )


@dataclass
class SSO_SAML_Config(SSO_Config):
    is_enabled: bool
    import_groups: bool  # False
    require_invitation: bool
    redirect_url: str

    auth_request_endpoint: str = None
    issuer: str = None
    relay_state: bool = None
    redirect_url: str = None
    sign_auth_request: Any = None

    @classmethod
    def _from_dict(cls, auth: dmda.DomoAuth, obj: dict, debug_prn: bool = False):
        raw = deepcopy(obj)

        is_enabled = obj.pop("enabled")

        relay_state = (
            dmcv.convert_string_to_bool(obj.pop("relayState"))
            if obj.get("relayState")
            else None
        )

        idp_certificate = (
            obj.pop("idpCertificate") if obj.get("idpCertificate") else None
        )

        return cls._parent_from_dict(
            auth=auth,
            obj=obj,
            is_enabled=is_enabled,
            idp_certificate=idp_certificate,
            relay_state=relay_state,
            raw=raw,
            debug_prn=debug_prn,
        )

    def to_dict(self, is_include_undefined: bool = False):
        return self._to_dict(
            generate_alternate_body_fn=sso_routes.generate_sso_saml_body,
            is_include_undefined=is_include_undefined,
        )

    @classmethod
    async def get(
        cls,
        auth: dmda.DomoAuth,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_prn: bool = False,
        return_raw: bool = False,
    ):
        res = await sso_routes.get_sso_saml_config(
            auth=auth,
            session=session,
            parent_class=cls.__name__,
            debug_api=debug_api,
            debug_num_stacks_to_drop=1,
        )

        if return_raw:
            return res

        return SSO_SAML_Config._from_dict(
            auth=auth, obj=res.response, debug_prn=debug_prn
        )

    async def update(
        self,
        session: httpx.AsyncClient = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        debug_is_test: bool = False,
        return_raw: bool = False,
        **kwargs,
    ):
        return await self._update(
            update_config_route_fn=sso_routes.update_sso_saml_config,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            debug_is_test=debug_is_test,
            return_raw=return_raw,
            **kwargs,
        )


@dataclass
class SSO:
    """
    class for managing SSO Config.
    Includes both OIDC aand SAML
    """

    auth: dmda.DomoAuth = field(repr=False)

    OIDC: SSO_OIDC_Config = field(default=None)  # OIDDC config class
    SAML: SSO_SAML_Config = field(default=None)  # SAML config class

    async def get_oidc(
        self, debug_api: bool = False, debug_prn: bool = False, return_raw: bool = False
    ):
        OIDC = await SSO_OIDC_Config.get(
            auth=self.auth,
            debug_prn=debug_prn,
            debug_api=debug_api,
            return_raw=return_raw,
        )

        if return_raw:
            return OIDC

        self.OIDC = OIDC

        return self.OIDC

    async def get_saml(
        self, debug_api: bool = False, debug_prn: bool = False, return_raw: bool = False
    ):
        SAML = await SSO_SAML_Config.get(
            auth=self.auth,
            debug_prn=debug_prn,
            debug_api=debug_api,
            return_raw=return_raw,
        )

        if return_raw:
            return SAML

        self.SAML = SAML

        return self.SAML

    async def get(self, debug_api: bool = False, debug_prn: bool = False):
        await self.get_oidc(debug_prn=debug_prn, debug_api=debug_api)
        await self.get_saml(debug_prn=debug_prn, debug_api=debug_api)

        return self
