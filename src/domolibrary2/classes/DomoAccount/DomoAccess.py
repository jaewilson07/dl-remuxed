"""DomoAccess re-export for DomoAccount package.

This module re-exports DomoAccess classes from the subentity package
to resolve import dependencies within the DomoAccount package.
"""

from dataclasses import dataclass, field

import httpx

from ...classes.subentity.access import Access_Entity, DomoAccess
from ...routes import account as account_routes
from ...routes.account import (
    ShareAccount,
    ShareAccount_AccessLevel,
    ShareAccount_V1_AccessLevel,
)
from ...utils import chunk_execution as dmce


@dataclass
class DomoAccess_Account(DomoAccess):
    """
    Account access management with unified access control integration.

    This class provides backward compatibility while integrating with
    the new unified access control system. Use get_unified_access_summary()
    for access to the standardized access control interface.
    """

    version: int = None  # api version - aligns to feature switch

    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    def __post_init__(self):
        super().__post_init__()

        if isinstance(self.share_enum, ShareAccount_AccessLevel):
            self.version = 2
        elif isinstance(self.share_enum, ShareAccount_V1_AccessLevel):
            self.version = 1

        return True

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """assumes v2 access api"""

        res = await account_routes.get_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        self.accesslist = await dmce.gather_with_concurrency(
            *[
                Access_Entity._from_user_id(
                    user_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "USER"
            ],
            *[
                Access_Entity._from_group_id(
                    group_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "GROUP"
            ],
            n=10,
        )
        return self.accesslist


@dataclass
class DomoAccess_OAuth(DomoAccess):
    share_enum: ShareAccount = field(repr=False, default=ShareAccount_AccessLevel)

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
    ):
        """assumes v2 access api"""

        res = await account_routes.get_oauth_account_accesslist(
            auth=self.auth,
            account_id=self.parent_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        self.accesslist = await dmce.gather_with_concurrency(
            *[
                Access_Entity._from_user_id(
                    user_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "USER"
            ],
            *[
                Access_Entity._from_group_id(
                    group_id=obj["id"],
                    auth=self.auth,
                    relation_type=self.share_enum.get(obj["accessLevel"]),
                )
                for obj in res.response
                if obj["type"] == "GROUP"
            ],
            n=10,
        )
        return self.accesslist


__all__ = [
    "DomoAccess_Account",
    "DomoAccess_OAuth",
]
