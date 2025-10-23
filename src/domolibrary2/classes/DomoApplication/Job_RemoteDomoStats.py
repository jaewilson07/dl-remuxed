__all__ = [
    "RemoteDomoStats_Config_Policy",
    "RemoteDomoStats_Config",
    "DomoJob_RemoteDomoStats",
]

import datetime as dt
from dataclasses import dataclass, field
from typing import List, Optional

import httpx

from ...client.auth import DomoAuth
from .Job_Base import (
    DomoJob_Base,
    DomoTrigger,
    DomoTrigger_Schedule,
)
from ...routes import application as application_routes


@dataclass
class RemoteDomoStats_Config_Policy:
    type: str
    dataset_id: str

    def to_dict(self):
        return {self.type: self.dataset_id}

    def __eq__(self, other) -> bool:
        if not isinstance(other, RemoteDomoStats_Config_Policy):
            return False

        return self.type == other.type


@dataclass
class RemoteDomoStats_Config:
    policies: List[RemoteDomoStats_Config_Policy] = field(default_factory=lambda: [])

    def _add_policy(self, report_type, dataset_id):
        new_policy = RemoteDomoStats_Config_Policy(
            type=report_type, dataset_id=dataset_id
        )

        if new_policy not in self.policies:
            self.policies.append(new_policy)

        else:
            policy_index = self.policies.index(new_policy)
            self.policies[policy_index] = new_policy

        return self.policies

    @classmethod
    def from_dict(cls, obj):
        domo_policies = cls()
        [
            domo_policies._add_policy(report_type, dataset_id)
            for report_type, dataset_id in obj.items()
        ]
        return domo_policies

    def to_dict(self):
        return {
            report_type: dataset_id
            for policy in self.policies
            for report_type, dataset_id in policy.to_dict().items()
        }


@dataclass
class DomoJob_RemoteDomoStats(DomoJob_Base):
    remote_instance: str = None
    subscriber_job_id: str = None

    Config: RemoteDomoStats_Config = None

    @classmethod
    def from_dict(cls, obj, auth):
        return cls(
            **cls._convert_API_res_to_DomoJob_base_obj(obj),
            remote_instance=cls._format_remote_instance(
                obj["executionPayload"]["remoteInstance"]
            ),
            subscriber_job_id=obj.get("executionPayload", {}).get(
                "subscriberJobId", None
            ),
            auth=auth,
            Config=RemoteDomoStats_Config.from_dict(
                obj["executionPayload"]["policies"]
            ),
        )

    @classmethod
    async def get_by_id(
        cls,
        application_id,
        job_id,
        auth: DomoAuth,
        debug_api: bool = False,
        session: Optional[httpx.AsyncClient] = None,
        debug_num_stacks_to_drop=2,
        return_raw: bool = False,
    ):
        return await cls._get_by_id(
            application_id=application_id,
            job_id=job_id,
            auth=auth,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            return_raw=return_raw,
            new_cls=cls,
            parent_class=cls.__name__,
        )

    def to_dict(self):
        s = self._generate_to_dict()

        s["executionPayload"].update(
            {
                "policies": self.Config.to_dict(),
                "remoteInstance": self.remote_instance,
                "subscriberJobId": self.subscriber_job_id,
            }
        )

        return s

    @classmethod
    async def create(
        cls,
        auth: DomoAuth,
        name: str,
        config: RemoteDomoStats_Config,
        application_id: str,
        logs_dataset_id: str,
        description: str = f"created via domolibrary f{dt.date.today()}",
        remote_instance: str = None,
        accounts: List[int] = None,
        triggers: List[DomoTrigger_Schedule] = None,
        execution_timeout: int = 1440,
        return_raw: bool = False,
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        session: Optional[httpx.AsyncClient] = None,
    ):
        triggers_ls = []
        if triggers is not None and len(triggers) > 0:
            triggers_ls = [
                DomoTrigger(id=None, job_id=None, schedule=schedule)
                for schedule in triggers
            ]

        domo_job = cls(
            application_id=application_id,
            auth=auth,
            name=name,
            logs_dataset_id=logs_dataset_id,
            accounts=accounts,
            description=description,
            remote_instance=remote_instance,
            Config=config,
            triggers=triggers_ls,
            execution_timeout=execution_timeout,
        )

        body = domo_job.to_dict()

        res = await application_routes.create_application_job(
            auth=auth,
            application_id=application_id,
            body=body,
            parent_class=cls.__name__,
            session=session,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        )

        if return_raw:
            return res

        return cls.from_dict(res.response, auth=auth)
