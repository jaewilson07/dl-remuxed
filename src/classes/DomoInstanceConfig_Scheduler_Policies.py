__all__ = [
    "parse_dt",
    "DomoScheduler_Policy_Restrictions",
    "DomoScheduler_Policy_Frequencies",
    "DomoScheduler_Policy_Member",
    "DomoScheduler_Policy",
    "DomoScheduler_Policies",
]

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional

import httpx

from ..client import DomoAuth as dmda
from ..client.DomoEntity import DomoBase, DomoEnum, DomoSubEntity
from ..routes import instance_config_scheduler_policies as scheduler_policies_routes


def parse_dt(dt: str) -> datetime:
    return datetime.fromisoformat(dt.replace("Z", "+00:00"))


class DomoScheduler_Policy_Restrictions(DomoEnum):
    NO_RESTRICTIONS = 0
    FIFTEEN_MINUTES = 15
    THIRTY_MINUTES = 30
    HOURLY = 60
    DAILY = 1440


@dataclass
class DomoScheduler_Policy_Frequencies:
    connector_frequency: DomoScheduler_Policy_Restrictions
    dataflow_frequency: DomoScheduler_Policy_Restrictions

    @classmethod
    def _from_dict(cls, d: dict):
        def to_enum(v: int) -> DomoScheduler_Policy_Restrictions:
            try:
                return DomoScheduler_Policy_Restrictions(v)
            except ValueError:
                raise ValueError(f"Unsupported frequency (minutes): {v}")

        return cls(
            connector_frequency=to_enum(d["connectorFrequency"]),
            dataflow_frequency=to_enum(d["dataflowFrequency"]),
        )

    def to_dict(self) -> dict:
        return {
            "connectorFrequency": self.connector_frequency.value,
            "dataflowFrequency": self.dataflow_frequency.value,
        }


@dataclass
class DomoScheduler_Policy_Member:
    type: Literal["USER", "GROUP"]
    # TODO: Investigate if its worth it to connect to group or user domo classes
    id: str

    @classmethod
    def _from_dict(cls, d: dict):
        return cls(type=d["type"], id=str(d["id"]))

    def to_dict(self) -> dict:
        return {"type": self.type, "id": self.id}


@dataclass
class DomoScheduler_Policy(DomoBase):
    created_on: datetime
    name: str
    frequencies: DomoScheduler_Policy_Frequencies
    members: List[DomoScheduler_Policy_Member] = field(default_factory=list)
    id: Optional[str] = field(
        default=None
    )  # Will be None if the policy is not yet created (used on upsert)
    policy_id: Optional[str] = field(default=None)

    @classmethod
    def _from_dict(cls, d: dict):
        return cls(
            created_on=parse_dt(d["createdOn"]),
            id=d["id"],
            name=d["name"],
            frequencies=DomoScheduler_Policy_Frequencies._from_dict(d["frequencies"]),
            members=[DomoScheduler_Policy_Member._from_dict(m) for m in d["members"]],
        )

    def to_dict(self) -> dict:
        return {
            "createdOn": self.created_on.isoformat().replace("+00:00", "Z"),
            "id": self.id,
            "name": self.name,
            "frequencies": self.frequencies.to_dict(),
            "members": [m.to_dict() for m in self.members],
            "policyId": self.policy_id,
        }


@dataclass
class DomoScheduler_Policies(DomoSubEntity):
    auth: dmda.DomoAuth
    policies: List[DomoScheduler_Policy] = field(default_factory=list)

    async def get(
        self,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
        debug_num_stacks_to_drop: int = 2,
        **kwargs,
    ):
        res = await scheduler_policies_routes.get_scheduler_policies(
            auth=self.auth,
            debug_api=debug_api,
            session=session,
            return_raw=return_raw,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            **kwargs,
        )
        self.policies = [DomoScheduler_Policy._from_dict(p) for p in res.response]
        return self.policies

    async def upsert(
        self,
        policy: DomoScheduler_Policy,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        session: Optional[httpx.AsyncClient] = None,
        return_raw: bool = False,
        **kwargs,
    ):
        create_policy = (not policy.id or not str(policy.id).strip()) or (
            policy.id not in {p.id for p in self.policies}
        )
        # If the policy is not yet created, create it
        if create_policy:
            res = await scheduler_policies_routes.create_schdeduler_policy(
                auth=self.auth,
                create_body=policy.to_dict(),
                debug_api=debug_api,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                session=session,
                return_raw=return_raw,
            )
            policy = DomoScheduler_Policy._from_dict(res.response)
            self.policies.append(policy)
            return policy
        else:
            idx = self.policies.index(policy)
            res = await scheduler_policies_routes.update_scheduler_policy(
                auth=self.auth,
                policy_id=policy.id,
                update_body=policy.to_dict(),
                debug_api=debug_api,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                session=session,
                return_raw=return_raw,
            )
            policy = DomoScheduler_Policy._from_dict(res.response)
            self.policies[idx] = policy
            return policy

    async def delete(
        self,
        policy_id: str,
        debug_api: bool = False,
        debug_num_stacks_to_drop: int = 2,
        session: Optional[httpx.AsyncClient] = None,
        **kwargs,
    ):
        res = await scheduler_policies_routes.delete_policy(
            auth=self.auth,
            policy_id=policy_id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            session=session,
        )
        return res.is_success == True
