from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import List

import httpx

from ..routes import dataflow as dataflow_routes
from ..utils import chunk_execution as ce, convert as ct

__all__ = ["DomoDataflow_History_Execution", "DomoDataflow_History"]

from .Dataflow_Action import DomoDataflow_ActionResult


@dataclass
class DomoDataflow_History_Execution:
    auth: DomoAuth = field(repr=False)
    id: str
    dataflow_id: str
    dataflow_execution_id: str
    dataflow_version: str

    begin_time: dt.datetime
    end_time: dt.datetime
    last_updated: dt.datetime

    is_failed: bool
    state: str
    activation_type: str
    data_processor: str
    telemetry: dict
    execution_stats: dict

    action_results: List[DomoDataflow_ActionResult] = None

    @classmethod
    def from_dict(cls, de_obj, auth: DomoAuth):
        action_results = None
        if de_obj.get("actionResults"):
            action_results = [
                DomoDataflow_ActionResult.from_dict(action_obj)
                for action_obj in de_obj.get("actionResults")
            ]

        return cls(
            auth=auth,
            id=de_obj["id"],
            dataflow_id=de_obj["onboardFlowId"],
            dataflow_execution_id=de_obj["dapDataFlowExecutionId"],
            dataflow_version=de_obj.get("dataFlowVersion"),
            begin_time=ct.convert_epoch_millisecond_to_datetime(
                de_obj.get("beginTime")
            ),
            end_time=ct.convert_epoch_millisecond_to_datetime(de_obj.get("endTime")),
            last_updated=ct.convert_epoch_millisecond_to_datetime(
                de_obj["lastUpdated"]
            ),
            is_failed=de_obj.get("failed"),
            state=de_obj["state"],
            activation_type=de_obj["activationType"],
            data_processor=de_obj["dataProcessor"],
            telemetry=de_obj.get("telemetry"),
            execution_stats={
                "total_bytes_written": de_obj.get("totalBytesWritten", 0),
                "total_rows_read": de_obj.get("totalRowsRead", 0),
                "total_bytes_read": de_obj.get("totalBytesRead", 0),
                "mean_download_rate_kbps": de_obj.get("meanDownloadRateKbps", 0),
                "total_rows_written": de_obj.get("totalRowsWritten", 0),
            },
            action_results=action_results,
        )

    @classmethod
    async def get_by_id(
        cls,
        auth: DomoAuth,
        dataflow_id: int,
        execution_id: int,
        debug_api: bool = False,
        debug_num_stacks_to_drop=1,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
    ):
        """retrieves details about a dataflow execution including actions"""

        res = await dataflow_routes.get_dataflow_execution_by_id(
            auth=auth,
            dataflow_id=dataflow_id,
            execution_id=execution_id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=cls.__name__,
            session=session,
        )

        if return_raw:
            return res

        return cls.from_dict(auth=auth, de_obj=res.response)

    async def get_actions(
        self,
        debug_api: bool = False,
        debug_num_stacks_to_drop=1,
        session: httpx.AsyncClient = None,
        return_raw: bool = False,
    ):
        """retrieves details execution action results"""

        res = await dataflow_routes.get_dataflow_execution_by_id(
            auth=self.auth,
            dataflow_id=self.dataflow_id,
            execution_id=self.id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            session=session,
        )

        if return_raw:
            return res

        action_results = res.response.get("actionResults")
        if action_results:
            action_results = [
                DomoDataflow_ActionResult.from_dict(action_obj)
                for action_obj in action_results
            ]

        self.action_results = action_results
        return self.action_results


async def get_by_id(
    cls,
    auth: DomoAuth,
    dataflow_id: int,
    execution_id: int,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    """retrieves details about a dataflow execution including actions"""

    res = await dataflow_routes.get_dataflow_execution_by_id(
        auth=auth,
        dataflow_id=dataflow_id,
        execution_id=execution_id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=cls.__name__,
        session=session,
    )

    if return_raw:
        return res

    return cls.from_dict(auth=auth, de_obj=res.response)


async def get_actions(
    self: DomoDataflow_History_Execution,
    debug_api: bool = False,
    debug_num_stacks_to_drop=1,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    """retrieves details execution action results"""

    res = await dataflow_routes.get_dataflow_execution_by_id(
        auth=self.auth,
        dataflow_id=self.dataflow_id,
        execution_id=self.id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
        session=session,
    )

    if return_raw:
        return res

    action_results = res.response.get("actionResults")
    if action_results:
        action_results = [
            DomoDataflow_ActionResult.from_dict(action_obj)
            for action_obj in action_results
        ]

    self.action_results = action_results
    return self.action_results


@dataclass
class DomoDataflow_History:
    auth: DomoAuth = field(repr=False)
    dataflow_id: int = field(repr=False)

    dataflow: None = field(repr=False, default=None)

    execution_history: List[DomoDataflow_History_Execution] = None

    async def get_execution_history(
        self,
        auth: DomoAuth = None,
        maximum=10,  # maximum number of execution histories to retrieve
        debug_api: bool = False,
        debug_num_stacks_to_drop=2,
        return_raw: bool = False,
    ):
        """retrieves metadata about execution history.
        includes details like execution status.
        """

        auth = auth or self.auth or self.dataflow.auth

        res = await dataflow_routes.get_dataflow_execution_history(
            auth=auth,
            dataflow_id=self.dataflow_id,
            debug_api=debug_api,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=self.__class__.__name__,
            maximum=maximum,
        )

        if return_raw:
            return res

        execution_history = [
            DomoDataflow_History_Execution.from_dict(df_obj, auth)
            for df_obj in res.response
        ]

        await ce.gather_with_concurrency(
            *[domo_execution.get_actions() for domo_execution in execution_history],
            n=20,
        )

        self.execution_history = execution_history

        return self.execution_history


async def get_execution_history(
    self: DomoDataflow_History,
    auth: DomoAuth = None,
    maximum=10,  # maximum number of execution histories to retrieve
    debug_api: bool = False,
    debug_num_stacks_to_drop=2,
    return_raw: bool = False,
):
    """retrieves metadata about execution history.
    includes details like execution status.
    """

    auth = auth or self.auth or self.dataflow.auth

    res = await dataflow_routes.get_dataflow_execution_history(
        auth=auth,
        dataflow_id=self.dataflow_id,
        debug_api=debug_api,
        debug_num_stacks_to_drop=debug_num_stacks_to_drop,
        parent_class=self.__class__.__name__,
        maximum=maximum,
    )

    if return_raw:
        return res

    execution_history = [
        DomoDataflow_History_Execution.from_dict(df_obj, auth)
        for df_obj in res.response
    ]

    await ce.gather_with_concurrency(
        *[domo_execution.get_actions() for domo_execution in execution_history], n=20
    )

    self.execution_history = execution_history

    return self.execution_history
