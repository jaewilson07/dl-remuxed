__all__ = ["PDP_Parameter", "PDP_Policy", "Dataset_PDP_Policies", "SearchPDP_NotFound"]

from dataclasses import dataclass

import httpx

from domolibrary2.entities.entities import DomoBase, DomoManager, DomoSubEntity
from typing import List
from ...client.auth import DomoAuth
from ...client.exceptions import DomoError as de
from ...routes import pdp as pdp_routes
from ...utils import DictDot as util_dd, chunk_execution as ce


@dataclass
class PDP_Parameter(DomoBase):
    column_name: str
    column_values_ls: list
    operator: str = (
        "EQUALS"
        or "GREATER_THAN"
        or "LESS_THAN"
        or "GREATER_THAN_EQUAL"
        or "LESS_THAN_EQUAL"
        or "BETWEEN"
    )
    ignore_case: bool = True
    type: str = (
        "COLUMN" or "DYNAMIC"
    )  # column sets parameter on data vs dynamic creates on Domo Trusted Attribute

    def to_parameter_simple(self) -> dict:
        return pdp_routes.generate_policy_parameter_simple(
            column_name=self.name,
            type=self.type,
            column_values_ls=self.values,
            operator=self.operator,
            ignore_case=self.ignore_case,
        )


@dataclass
class PDP_Policy:
    dataset_id: str
    filter_group_id: str
    name: str
    # resources: list
    parameters_ls: list[dict]
    user_ls: list[str]
    group_ls: list[str]
    virtual_user_ls: list[str]

    @classmethod
    async def from_dict(cls, obj, auth: DomoAuth):
        from . import DomoGroup as dmg, DomoUser as dmu

        return cls(
            dataset_id=obj["dataSourceId"],
            filter_group_id=obj["filterGroupId"],
            name=obj["name"],
            # resources=dd.resources,
            parameters_ls=obj["parameters"],
            user_ls=(
                await ce.gather_with_concurrency(
                    n=60,
                    *[
                        dmu.DomoUser.get_by_id(user_id=id, auth=auth)
                        for id in obj.get("userIds", [])
                    ],
                )
                if obj.get("userIds")
                else None
            ),
            group_ls=(
                await ce.gather_with_concurrency(
                    n=60,
                    *[
                        dmg.DomoGroup.get_by_id(group_id=id, auth=auth)
                        for id in obj.get("groupIds", [])
                    ],
                )
                if obj.get("groupIds")
                else None
            ),
            virtual_user_ls=obj.get("virtualUserIds", []),
        )

    @classmethod
    async def upsert_policy(
        cls,
        auth: DomoAuth,
        dataset_id: str,
        # body sent to the API (uses camelCase instead of snake_case)
        policy_definition: dict,
        debug_api: bool = False,
        debug_prn: bool = False,
    ):
        # print(policy_definition)
        policy_id = policy_definition.get("filterGroupId")
        if policy_id:
            if debug_prn:
                print(f"Updating policy {policy_id} in {auth.domo_instance}")
            res = await pdp_routes.update_policy(
                auth=auth,
                dataset_id=dataset_id,
                policy_id=policy_id,
                body=policy_definition,
                debug_api=debug_api,
            )
            return res
        else:
            if debug_prn:
                print(f"Policy does not exist. Creating policy in {auth.domo_instance}")
            res = await pdp_routes.create_policy(
                auth=auth,
                dataset_id=dataset_id,
                body=policy_definition,
                debug_api=debug_api,
            )
            return res


def generate_body_from_policy(
    self: PDP_Policy,
    # params: list[dict] = ''
):
    if not self.parameters_ls:
        raise Exception("generate_body_from_policy: no parameters")

    self.parameters_ls = [
        PDP_Parameter.generate_parameter_simple(param) for param in self.parameters_ls
    ]

    return pdp_routes.generate_policy_body(
        policy_name=self.name,
        dataset_id=self.dataset_id,
        parameters_ls=self.parameters_ls,
        policy_id=self.filter_group_id,
        user_ids=self.user_ls,
        group_ids=self.group_ls,
        virtual_user_ids=self.virtual_user_ls,
    )


@dataclass
class Dataset_PDP_Policies(DomoSubEntity):
    parent = None  # domo dataset class
    policies: List[PDP_Policy] = None

    async def get(
        self,
        include_all_rows: bool = True,
        return_raw: bool = False,
        debug_api: bool = False,
        session: httpx.AsyncClient = None,
    ):
        dataset_id = self.parent.id
        auth = self.auth or self.parent.auth

        res = await pdp_routes.get_pdp_policies(
            auth=auth,
            dataset_id=dataset_id,
            debug_api=debug_api,
            include_all_rows=include_all_rows,
            session=session,
            parent_class=self.__class__.__name__,
        )

        if return_raw:
            return res

        policies: List[PDP_Policy] = await ce.gather_with_concurrency(
            n=60,
            *[
                PDP_Policy.from_dict(policy_obj, auth=auth)
                for policy_obj in res.response
            ],
        )

        self.policies = policies
        return policies


class SearchPDP_NotFound(de.DomoError):
    def __init__(
        self, domo_instance, dataset_id, message="not found", function_name="search_pdp"
    ):
        super().__init__(
            domo_instance=domo_instance,
            entity_id=dataset_id,
            message=message,
            function_name=function_name,
        )


async def search_pdp_policies(
    cls: Dataset_PDP_Policies,
    auth: DomoAuth,
    search: str,
    dataset_id: str = None,
    search_method: str = "id" or "name",
    is_exact_match: bool = True,
    return_raw: bool = False,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    all_pdp_policies = await Dataset_PDP_Policies(cls).get_policies(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api
    )

    if return_raw:
        return all_pdp_policies

    if search_method == "name":
        if is_exact_match:
            policy_search = next(
                (policy for policy in all_pdp_policies if policy.name == search), None
            )
            # print(policy_search)

            if not policy_search:
                raise SearchPDP_NotFound(
                    dataset_id=dataset_id,
                    message=f'There is no policy named "{search}" on dataset_id {dataset_id}',
                    domo_instance=auth.domo_instance,
                )

            return policy_search
        else:
            policy_search = [
                policy
                for policy in all_pdp_policies
                if search.lower() in policy.name.lower()
            ]
            if not policy_search:
                raise SearchPDP_NotFound(
                    dataset_id=dataset_id,
                    message=f'There is no policy name containing "{search}" on dataset_id {dataset_id}',
                    domo_instance=auth.domo_instance,
                )

            return policy_search
    else:
        policy_search = next(
            (policy for policy in all_pdp_policies if policy.filter_group_id == search),
            None,
        )

    if not policy_search:
        raise SearchPDP_NotFound(
            dataset_id=dataset_id,
            message=f'There is no policy id "{search}" on dataset_id {dataset_id}',
            domo_instance=auth.domo_instance,
        )

    return policy_search


async def delete_policy(
    self: PDP_Policy,
    auth: DomoAuth,
    policy_id: str = None,
    dataset_id: str = None,
    debug_api: bool = False,
):
    dataset_id = dataset_id or self.dataset_id
    policy_id = policy_id or self.filter_group_id

    res = await pdp_routes.delete_policy(
        auth=auth, dataset_id=dataset_id, policy_id=policy_id, debug_api=debug_api
    )

    return res


async def toggle_dataset_pdp(
    self: Dataset_PDP_Policies,
    auth: DomoAuth = None,
    dataset_id: str = None,
    is_enable: bool = True,  # True will enable pdp, False will disable pdp
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.dataset.auth

    return await pdp_routes.toggle_pdp(
        auth=auth,
        dataset_id=dataset_id or self.dataset.id,
        is_enable=is_enable,
        debug_api=debug_api,
        session=session,
    )
