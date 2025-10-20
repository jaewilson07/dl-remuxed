__all__ = ["DomoAccount", "DomoAccounts_NoAccount", "DomoAccounts"]


from copy import deepcopy
from dataclasses import dataclass
from typing import List

import httpx

from ..client import auth as dmda
from ..client import entities as dmee
from ..client import exceptions as dmde
from ..routes import account as account_routes
from ..routes import datacenter as datacenter_routes

from ..utils import chunk_execution as dmce
from ..classes.DomoAccount_Config import (
    AccountConfig,
)
from ..classes.DomoAccount_Credential import (
    DomoAccount_Credential,
)
from ..classes.DomoAccount_Default import (
    DomoAccount_Default,
    UpsertAccount_MatchCriteria,
)
from ..classes.DomoAccount_OAuth import DomoAccount_OAuth
from ..client import DomoAuth as dmda
from ..client import DomoEntity as dmee
from ..client import exceptions as dmde
from ..routes import account as account_routes
from ..routes import datacenter as datacenter_routes
from ..utils import chunk_execution as dmce


@dataclass
class DomoAccount(DomoAccount_Default):
    @classmethod
    def from_dict(
        cls,
        obj: dict,
        is_admin_summary: bool = True,
        auth: dmda.DomoAuth = None,
        is_use_default_account_class=False,
        **kwargs,
    ):
        """converts data_v1_accounts API response into an accounts class object"""

        if is_use_default_account_class:
            new_cls = cls
        else:
            new_cls = DomoAccount_Credential

        return super().from_dict(
            auth=auth,
            obj=obj,
            is_admin_summary=is_admin_summary,
            **{**kwargs, "new_cls": new_cls},
        )


class DomoAccounts_NoAccount(dmde.ClassError):
    def __init__(self, cls=None, cls_instance=None, message=None, domo_instance=None):
        super().__init__(
            cls=cls, cls_instance=cls_instance, message=message, entity_id=domo_instance
        )


@dataclass
class DomoAccounts(dmee.DomoManager):
    accounts: List[DomoAccount] = None
    oauths: List[DomoAccount_OAuth] = None

    async def get_accounts_accountsapi(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        is_use_default_account_class: bool = True,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await account_routes.get_accounts(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop - 1,
        )

        if return_raw:
            return res

        if len(res.response) == 0:
            self.accounts = []
            return self.accounts

        self.accounts = await dmce.gather_with_concurrency(
            n=60,
            *[
                DomoAccount.get_by_id(
                    account_id=json_obj.get("id"),
                    debug_api=debug_api,
                    session=session,
                    auth=self.auth,
                    is_use_default_account_class=is_use_default_account_class,
                )
                for json_obj in res.response
            ],
        )

        return self.accounts

    async def get_accounts_queryapi(
        self,
        additional_filters_ls=None,
        is_use_default_account_class: bool = False,
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        session: httpx.AsyncClient = None,
    ):
        """v2 api for works with group_account_v2 beta"""

        from ..routes import datacenter as datacenter_routes

        res = await datacenter_routes.search_datacenter(
            auth=self.auth,
            entity_type=datacenter_routes.Datacenter_Enum.ACCOUNT.value,
            additional_filters_ls=additional_filters_ls,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop - 1,
        )

        if return_raw:
            return res

        if len(res.response) == 0:
            self.accounts = []
            return self.accounts

        self.accounts = [
            DomoAccount.from_dict(
                account_obj,
                auth=self.auth,
                is_use_default_account_class=is_use_default_account_class,
            )
            for account_obj in res.response
        ]
        return self.accounts

    async def get(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        is_use_default_account_class: bool = False,
        debug_num_stacks_to_drop: int = 3,
    ):
        domo_accounts = None
        try:
            domo_accounts = await self.get_accounts_queryapi(
                debug_api=debug_api,
                session=session,
                is_use_default_account_class=is_use_default_account_class,
                return_raw=return_raw,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop - 1,
            )

        except datacenter_routes.SearchDatacenter_NoResultsFound as e:
            print(e)

        if not domo_accounts:
            domo_accounts = await self.get_accounts_accountsapi(
                debug_api=debug_api,
                session=session,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop - 1,
                is_use_default_account_class=is_use_default_account_class,
                return_raw=return_raw,
            )

        if return_raw:
            return domo_accounts

        return self.accounts

    async def get_oauths(
        self,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
        debug_num_stacks_to_drop: int = 2,
    ):
        res = await account_routes.get_oauth_accounts(
            auth=self.auth,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

        if return_raw:
            return res

        self.oauths = [
            DomoAccount_OAuth.from_dict(
                obj=obj, auth=self.auth, is_use_default_account_class=True
            )
            for obj in res.response
        ]

        return self.oauths

    @classmethod
    async def upsert_account(
        cls,
        auth: dmda.DomoAuth,
        account_id: str = None,
        account_name: str = None,
        account_config: AccountConfig = None,
        data_provider_type: str = None,
        debug_api: bool = False,
        debug_prn: bool = False,
        return_raw: bool = False,
        return_search: bool = False,
        is_use_default_account_class: bool = True,
        session: httpx.AsyncClient = None,
        **kwargs,
    ):
        """search for an account and upsert it"""

        if not account_name and not account_id:
            raise UpsertAccount_MatchCriteria(domo_instance=auth.domo_instance)

        data_provider_type = (
            data_provider_type or account_config and account_config.data_provider_type
        )
        acc = None

        if account_id:
            try:
                acc = await DomoAccount.get_by_id(
                    auth=auth,
                    session=session,
                    debug_api=debug_api,
                    account_id=account_id,
                    is_use_default_account_class=is_use_default_account_class,
                    **kwargs,
                )
            except dmde.DomoError:
                pass

        if account_name and not acc:
            try:
                domo_accounts = DomoAccounts(auth=auth)
                await domo_accounts.get(
                    debug_api=debug_api,
                    session=session,
                    is_use_default_account_class=is_use_default_account_class,
                    **kwargs,
                )

                for da in domo_accounts.accounts:
                    if da.name and da.name.lower() != account_name.lower():
                        continue

                    if (
                        data_provider_type
                        and data_provider_type != da.data_provider_type
                    ):
                        continue

                    acc = da

            except dmde.DomoError:
                pass

        if return_search:
            return acc

        if not isinstance(
            acc, (DomoAccount_Default, DomoAccount, DomoAccount_Credential)
        ):
            if debug_prn:
                print(f"creating {account_name} in {auth.domo_instance}")

            return await DomoAccount.create_account(
                account_name=account_name,
                config=account_config,
                auth=auth,
                debug_api=debug_api,
                return_raw=return_raw,
            )

        if account_name and account_id:
            if debug_prn:
                print(f"upsert-ing {acc.id} - {acc.name} in {auth.domo_instance}")

            await acc.update_name(
                account_name=account_name,
                debug_api=debug_api,
                return_raw=return_raw,
                session=session,
            )

        if account_config:  # upsert account
            acc.Config = account_config

            if debug_prn:
                print(f"upsertting {acc.id}:  updating config")

            await acc.update_config(
                debug_api=debug_api, return_raw=return_raw, session=session
            )

        return acc
