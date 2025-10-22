"""Page access control and sharing operations."""

__all__ = ["test_page_access", "get_accesslist", "share"]

import httpx

from .. import DomoUser as dmu

from ...client.auth import DomoAuth
from ...routes import page as page_routes, datacenter as datacenter_routes
from ...utils import chunk_execution as dmce
from .exceptions import Page_NoAccess


async def test_page_access(
    self,
    suppress_no_access_error: bool = False,  # suppresses error if user doesn't have access
    debug_api: bool = False,
    return_raw: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    """throws an error if user doesn't have access to the page
    API returns the owners of the page
    """

    res = await page_routes.get_page_access_test(
        auth=self.auth,
        page_id=self.id,
        session=session,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    try:
        page_access = res.response.get("pageAccess")

        if not page_access:
            raise Page_NoAccess(
                page_id=self.id,
                page_title=self.title,
                domo_instance=self.auth.domo_instance,
                function_name=res.traceback_details.function_name,
                parent_class=self.__class__.__name__,
            )

    except Page_NoAccess as e:
        print(e)

        if not suppress_no_access_error:
            raise e

    return res


async def get_accesslist(
    self,
    auth: DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    debug_num_stacks_to_drop=2,
):
    auth = auth or self.auth

    res = await page_routes.get_page_access_list(
        auth=auth,
        is_expand_users=True,
        page_id=self.id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        session=session,
        parent_class=self.__class__.__name__,
    )

    if return_raw:
        return res

    from .. import DomoGroup as dmg

    s = {
        "explicit_shared_user_count": res.response.get("explicitSharedUserCount"),
        "total_user_count": res.response.get("totalUserCount"),
    }

    user_ls = res.response.get("users", None)
    domo_users = []

    if user_ls and isinstance(user_ls, list) and len(user_ls) > 0:
        domo_users = await dmu.DomoUsers.by_id(
            user_ids=[user.get("id") for user in user_ls],
            only_allow_one=False,
            auth=auth,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
        )

    group_ls = res.response.get("groups", None)
    domo_groups = []
    if group_ls and isinstance(group_ls, list) and len(group_ls) > 0:
        domo_groups = await dmce.gather_with_concurrency(
            n=60,
            *[
                dmg.DomoGroup.get_by_id(
                    group_id=group.get("id"),
                    auth=auth,
                    session=session,
                    debug_num_stacks_to_drop=debug_num_stacks_to_drop + 1,
                )
                for group in group_ls
            ],
        )

    res = await self.test_page_access(suppress_no_access_error=True)
    owner_ls = res.response["owners"]  # from test_page_access

    for domo_user in domo_users:
        # isExplicitShare is set by the get_access_list API response
        domo_user.custom_attributes["is_explicit_share"] = next(
            obj["isExplicitShare"]
            for obj in user_ls
            if int(obj.get("id")) == int(domo_user.id)
        )

        # group membership is determined by get_access_list API response
        domo_user.custom_attributes["group_membership"] = [
            domo_group
            for group_obj in group_ls
            for domo_group in domo_groups
            if int(domo_user.id) in [int(obj["id"]) for obj in group_obj.get("users")]
            and domo_group.id == group_obj["id"]
        ]

        # isOwner determined by test_access API response and group membership
        domo_user.custom_attributes["is_owner"] = False

        # test ownership as a user
        match_owner = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"]) == int(domo_user.id)
                and owner_obj["type"] == "USER"
            ),
            None,
        )

        match_group = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"])
                in [
                    int(domo_group.id)
                    for domo_group in domo_user.custom_attributes["group_membership"]
                ]
                and owner_obj["type"] == "GROUP"
            ),
            None,
        )

        if match_owner or match_group:
            domo_user.custom_attributes["is_owner"] = True

    # group ownership is confirmed test_access API
    for domo_group in domo_groups:
        match_owner = next(
            (
                owner_obj
                for owner_obj in owner_ls
                if int(owner_obj["id"]) == int(domo_group.id)
                and owner_obj["type"] == "GROUP"
            ),
            None,
        )

        domo_group.custom_attributes["is_owner"] = True if match_owner else False

    return {
        **s,
        "domo_users": domo_users,
        "domo_groups": domo_groups,
    }


async def share(
    self,
    auth: DomoAuth = None,
    domo_users: list = None,  # DomoUsers to share page with,
    domo_groups: list = None,  # DomoGroups to share page with
    message: str = None,  # message for automated email
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    if domo_groups:
        domo_groups = domo_groups if isinstance(domo_groups, list) else [domo_groups]
    if domo_users:
        domo_users = domo_users if isinstance(domo_users, list) else [domo_users]

    res = await datacenter_routes.share_resource(
        auth=auth or self.auth,
        resource_ids=[self.id],
        resource_type=datacenter_routes.ShareResource_Enum.PAGE,
        group_ids=[group.id for group in domo_groups] if domo_groups else None,
        user_ids=[user.id for user in domo_users] if domo_users else None,
        message=message,
        debug_api=debug_api,
        session=session,
    )

    return res
