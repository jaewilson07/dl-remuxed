__all__ = [
    "DomoAccountOAuth_Config_SnowflakeOauth",
    "DomoAccountOAuth_Config_JiraOnPremOauth",
    "OAuthConfig",
    "DomoAccount_OAuth",
    # Route exceptions
    "Account_GET_Error",
    "Account_CRUD_Error",
    "Account_NoMatch",
    "Account_Config_Error",
]

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import httpx

from ...client import entities as dmee
from ...client.auth import DomoAuth
from ...routes import account as account_routes
from ...routes.account.exceptions import (
    Account_Config_Error,
    Account_CRUD_Error,
    Account_GET_Error,
    Account_NoMatch,
)
from . import (
    Account_Default as dmacb,
    Config as dmacnfg,
)
from ..subentity.DomoAccess import DomoAccess_OAuth


@dataclass
class DomoAccountOAuth_Config_SnowflakeOauth(dmacnfg.DomoAccount_Config):
    data_provider_type: str = "snowflake-oauth-config"
    is_oauth: bool = True

    client_id: str = None
    secret: str = None

    @classmethod
    def from_dict(cls, obj: dict, parent: Any = None, **kwargs):
        return cls(
            client_id=obj["client-id"],
            secret=obj["client-secret"],
            raw=obj,
            parent=parent,
        )

    def to_dict(self):
        return {"client-id": self.client_id, "client-secret": self.secret}


@dataclass
class DomoAccountOAuth_Config_JiraOnPremOauth(dmacnfg.DomoAccount_Config):
    data_provider_type: str = "jira-on-prem-oauth-config"
    is_oauth: bool = True

    client_id: str = None
    secret: str = None

    @classmethod
    def from_dict(cls, obj: dict, parent: Any = None):
        return cls(
            client_id=obj["client_id"],
            secret=obj["client_secret"],
            raw=obj,
            parent=parent,
        )

    def to_dict(self):
        return {"client_id": self.client_id, "client_secret": self.secret}


class OAuthConfig(dmee.DomoEnumMixin, Enum):
    snowflake_oauth_config = DomoAccountOAuth_Config_SnowflakeOauth

    jira_on_prem_oauth_config = DomoAccountOAuth_Config_JiraOnPremOauth

    @classmethod
    def _missing_(cls, value):
        alt_search_str = cls.generate_alt_search_str(value)

        config_match = next(
            (member for member in cls if member.name in [value, alt_search_str]),
            None,
        )

        ## best case scenario alt_search yields a result
        if not config_match:
            raise dmacnfg.AccountConfig_ProviderTypeNotDefined(value)

        return config_match


@dataclass
class DomoAccount_OAuth(dmacb.DomoAccount_Default):
    Access: DomoAccess_OAuth = field(repr=False, default=None)

    def __post_init__(self):
        self.Access = DomoAccess_OAuth.from_parent(parent=self)

    async def _get_config(
        self,
        session=None,
        return_raw: bool = False,
        debug_api: bool = None,
        debug_num_stacks_to_drop=2,
        is_suppress_no_config: bool = False,
    ):
        """Retrieve OAuth account configuration.

        Internal method to fetch and parse OAuth account configuration.
        Can be used to suppress cases where the config is not defined, either
        because the account_config is OAuth and not stored in Domo, OR because
        the AccountConfig class doesn't cover the data_type.

        Args:
            session: HTTP client session (optional)
            return_raw: Return raw response without processing
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            is_suppress_no_config: Suppress errors when config is not defined

        Returns:
            DomoAccount_Config: OAuth account configuration object

        Raises:
            Account_Config_Error: If configuration retrieval or parsing fails
        """
        if not self.data_provider_type:
            res = await account_routes.get_account_by_id(
                auth=self.auth,
                account_id=self.id,
                session=session,
                debug_api=debug_api,
                parent_class=self.__class__.__name__,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            )

            self.data_provider_type = res.response["dataProviderType"]

        res = await account_routes.get_oauth_account_config(
            auth=self.auth,
            account_id=self.id,
            session=session,
            debug_api=debug_api,
            data_provider_type=self.data_provider_type,
            parent_class=self.__class__.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        config_fn = OAuthConfig(self.data_provider_type).value

        if not is_suppress_no_config and not config_fn.is_defined_config:
            raise config_fn._associated_exception(self.data_provider_type)

        self.Config = config_fn.from_dict(res.response)

        if self.Config and self.Config.to_dict() != {}:
            if not res.response:
                print(self.data_provider_type, "no response")

            if not self.Config.to_dict():
                print(
                    self.id,
                    self.data_provider_type,
                    "no config",
                    self.Config.to_dict(),
                    res.response,
                )

            self._test_missing_keys(
                res_obj=res.response, config_obj=self.Config.to_dict()
            )

        return self.Config

    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        account_id: int,
        is_suppress_no_config: bool = True,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        **kwargs,
    ):
        """Retrieve OAuth account metadata and attempt to retrieve configuration.

        Args:
            auth: Authentication object for API requests
            account_id: ID of the OAuth account to retrieve
            is_suppress_no_config: Suppress errors when config is not defined
            session: HTTP client session (optional)
            return_raw: Return raw response without processing
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            **kwargs: Additional arguments passed to from_dict

        Returns:
            DomoAccount_OAuth: OAuth account instance with configuration

        Raises:
            Account_NoMatch: If OAuth account is not found
            Account_GET_Error: If OAuth account retrieval fails
            Account_Config_Error: If configuration retrieval fails
        """

        res = await account_routes.get_oauth_account_by_id(
            auth=auth,
            account_id=account_id,
            session=session,
            debug_api=debug_api,
            parent_class=cls.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        acc = cls.from_dict(
            obj=res.response,
            auth=auth,
            is_admin_summary=False,
            is_use_default_account_class=False,
            new_cls=cls,
            **kwargs,
        )

        await acc._get_config(
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
            is_suppress_no_config=is_suppress_no_config,
        )

        return acc

    @classmethod
    async def create(
        cls,
        auth: DomoAuth,
        account_name: str,
        oauth_config: OAuthConfig,
        origin: str = "OAUTH_CONFIGURATION",
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """Create a new OAuth account.

        Args:
            auth: Authentication object for API requests
            account_name: Name for the new OAuth account
            oauth_config: OAuth configuration object
            origin: Origin type for OAuth configuration (default: OAUTH_CONFIGURATION)
            debug_api: Enable API debugging
            session: HTTP client session (optional)
            debug_num_stacks_to_drop: Stack frames to drop for debugging

        Returns:
            DomoAccount_OAuth: The newly created OAuth account instance

        Raises:
            Account_CRUD_Error: If OAuth account creation fails
        """
        res = await account_routes.create_oauth_account(
            account_name=account_name,
            data_provider_type=oauth_config.data_provider_type,
            origin=origin,
            config=oauth_config.to_dict(),
            debug_api=debug_api,
            session=session,
            parent_class=cls.__name__,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        return await cls.get_by_id(
            auth=auth,
            account_id=res.response["id"],
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

    async def delete(
        self,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        """Delete this OAuth account.

        Args:
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            session: HTTP client session (optional)

        Returns:
            ResponseGetData: API response from delete operation

        Raises:
            Account_CRUD_Error: If OAuth account deletion fails
        """
        return await account_routes.delete_oauth_account(
            auth=self.auth,
            account_id=self.id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

    async def update_name(
        self,
        account_name: str,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        session: httpx.AsyncClient = None,
    ):
        """Update the name of this OAuth account.

        Args:
            account_name: New name for the account
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            session: HTTP client session (optional)

        Returns:
            DomoAccount_OAuth: Self for method chaining

        Raises:
            Account_CRUD_Error: If OAuth account name update fails
        """
        await account_routes.update_oauth_account_name(
            auth=self.auth,
            account_id=self.id,
            account_name=account_name,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

        self.name = account_name
        return self

    async def update_config(
        self,
        oauth_config: OAuthConfig = None,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: httpx.AsyncClient = None,
    ):
        """Update the OAuth configuration for this account.

        Args:
            oauth_config: New OAuth configuration (if None, uses existing Config)
            debug_api: Enable API debugging
            debug_num_stacks_to_drop: Stack frames to drop for debugging
            session: HTTP client session (optional)

        Returns:
            DomoAccount_OAuth: Self for method chaining

        Raises:
            Account_Config_Error: If OAuth account config update fails
        """
        await account_routes.update_oauth_account_config(
            auth=self.auth,
            account_id=self.id,
            config_body=oauth_config.to_dict() or self.Config.to_dict(),
            data_provider_type=self.data_provider_type,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

        self.Config = oauth_config

        return self
