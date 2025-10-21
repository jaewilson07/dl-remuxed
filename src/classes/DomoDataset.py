"""a class based approach for interacting with Domo Datasets"""

__all__ = [
    "DomoDataset_Default",
    "FederatedDomoDataset",
    "DomoPublishDataset",
    "DomoDataset",
]


import asyncio
import datetime as dt
import io
import json
from dataclasses import dataclass, field
from typing import Callable, List, Optional

import httpx
import pandas as pd
from ..client import DomoAuth as dmda
from ..client import exceptions as dmde
from ..client.DomoEntity import (
    DomoEntity_w_Lineage,
    DomoFederatedEntity,
    DomoPublishedEntity,
)
from ..routes import dataset as dataset_routes
from ..routes.dataset import (
    DatasetNotFoundError,
    QueryRequestError,
    ShareDataset_AccessLevelEnum,
)
from ..utils import chunk_execution as dmce
from ..utils import convert as dmcv
from . import DomoCertification as dmdc
from . import DomoDataset_Schema as dmdsc
from . import DomoDataset_Stream as dmdst
from . import DomoLineage as dmdl
from . import DomoPDP as dmpdp
from . import DomoTag as dmtg
from ..client import auth as dmda
from ..client import exceptions as dmde
from ..routes import dataset as dataset_routes

from ..utils import chunk_execution as dmce
from ..utils import convert as dmcv
from ..client.entities import (
    DomoEntity_w_Lineage,
    DomoFederatedEntity,
    DomoPublishedEntity,
)
from ..routes.dataset import (
    DatasetNotFoundError,
    QueryRequestError,
    ShareDataset_AccessLevelEnum,
)


@dataclass
class DomoDataset_Default(DomoEntity_w_Lineage):
    "interacts with domo datasets"

    id: str
    auth: DomoAuth = field(repr=False)

    display_type: str = ""
    data_provider_type: str = ""
    name: str = ""
    description: str = ""
    row_count: int = None
    column_count: int = None

    stream_id: int = None
    cloud_id: str = None

    last_touched_dt: dt.datetime = None
    last_updated_dt: dt.datetime = None
    created_dt: dt.datetime = None

    owner: dict = field(default_factory=dict)
    formula: dict = field(default_factory=dict)

    Schema: dmdsc.DomoDataset_Schema = field(default=None)
    Stream: dmdst.DomoStream = field(default=None)
    Tags: dmtg.DomoTags = field(default=None)
    PDP: dmpdp.Dataset_PDP_Policies = field(default=None)

    Certification: dmdc.DomoCertification = field(default=None)
    # Lineage: dmdl.DomoLineage = field(default=None, repr=False)

    parent_auth: DomoAuth = None

    def __post_init__(self):
        self.Lineage = dmdl.DomoLineage.from_parent(auth=self.auth, parent=self)

        self.Schema = dmdsc.DomoDataset_Schema.from_parent(parent=self)

        self.Tags = dmtg.DomoTags.from_parent(parent=self)

        self.Stream = dmdst.DomoStream.from_parent(parent=self)

        self.PDP = dmpdp.Dataset_PDP_Policies(dataset=self)

        if self.raw.get("certification"):
            self.Certification = dmdc.DomoCertification.from_parent(parent=self)

    def display_url(self):
        return f"https://{self.auth.domo_instance}.domo.com/datasources/{self.id}/details/overview"

    @classmethod
    def from_dict(
        cls,
        obj: dict,
        auth: DomoAuth,
        is_use_default_dataset_class: bool = True,
        new_cls=None,
        **kwargs,
    ):
        if not is_use_default_dataset_class:
            if not new_cls:
                raise NotImplementedError(
                    "Must provide new_cls if not using default dataset class"
                )
            cls = new_cls

        ds = cls(
            auth=auth,
            id=obj.get("id"),
            raw=obj,
            display_type=obj.get("displayType"),
            data_provider_type=obj.get("dataProviderType"),
            name=obj.get("name"),
            description=obj.get("description"),
            owner=obj.get("owner"),
            stream_id=obj.get("streamId"),
            cloud_id=obj.get("cloudId"),
            last_touched_dt=dmcv.convert_epoch_millisecond_to_datetime(
                obj.get("lastTouched")
            ),
            last_updated_dt=dmcv.convert_epoch_millisecond_to_datetime(
                obj.get("lastUpdated")
            ),
            created_dt=dmcv.convert_epoch_millisecond_to_datetime(obj.get("created")),
            row_count=int(obj.get("rowCount")),
            column_count=int(obj.get("columnCount")),
            Lineage=None,
            **kwargs,
        )

        formulas = obj.get("properties", {}).get("formulas", {}).get("formulas", {})

        if formulas:
            ds.formula = formulas

        if obj.get("tags"):
            ds.Tags.tag_ls = json.loads(obj.get("tags"))

        return ds

    @classmethod
    async def get_by_id(
        cls,
        dataset_id: str,
        auth: DomoAuth,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
        is_use_default_dataset_class: bool = False,
        parent_class: str = None,
    ):
        """retrieves dataset metadata"""

        parent_class = parent_class or cls.__name__

        res = await dataset_routes.get_dataset_by_id(
            auth=auth,
            dataset_id=dataset_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

        if return_raw:
            return res

        return cls.from_dict(
            obj=res.response,
            auth=auth,
            new_cls=cls,
            is_use_default_dataset_class=is_use_default_dataset_class,
        )

    @classmethod
    async def _get_entity_by_id(cls, entity_id: str, auth: DomoAuth, **kwargs):
        return await cls.get_by_id(dataset_id=entity_id, auth=auth, **kwargs)


async def query_dataset_private(
    self: DomoDataset_Default,
    sql: str,
    session: Optional[httpx.AsyncClient] = None,
    filter_pdp_policy_id_ls: List[int] = None,  # filter by pdp policy
    loop_until_end: bool = False,  # retrieve all available rows
    limit=100,  # maximum rows to return per request.  refers to PAGINATION
    skip=0,
    maximum=100,  # equivalent to the LIMIT or TOP clause in SQL, the number of rows to return total
    debug_api: bool = False,
    debug_loop: bool = False,
    debug_num_stacks_to_drop: int = 2,
    timeout=10,  # larger API requests may require a longer response time
    maximum_retry: int = 5,
    is_return_dataframe: bool = True,
) -> pd.DataFrame:
    res = None
    retry = 1

    if filter_pdp_policy_id_ls and not isinstance(filter_pdp_policy_id_ls, list):
        filter_pdp_policy_id_ls = [int(filter_pdp_policy_id_ls)]

    while (not res or not res.is_success) and retry <= maximum_retry:
        try:
            res = await dataset_routes.query_dataset_private(
                auth=self.auth,
                dataset_id=self.id,
                sql=sql,
                maximum=maximum,
                filter_pdp_policy_id_ls=filter_pdp_policy_id_ls,
                skip=skip,
                limit=limit,
                loop_until_end=loop_until_end,
                session=session,
                debug_loop=debug_loop,
                debug_api=debug_api,
                timeout=timeout,
                debug_num_stacks_to_drop=debug_num_stacks_to_drop,
                parent_class=self.__class__.__name__,
            )

        except DomoError as e:
            if isinstance(e, (DatasetNotFoundError, QueryRequestError)):
                raise e from e

            if retry <= maximum_retry and e:
                print(
                    f"⚠️ Error.  Attempt {retry} / {maximum_retry} - {e} - while query dataset {self.id} in {self.auth.domo_instance} with {sql}"
                )

            if retry == maximum_retry:
                raise e from e

            retry += 1

    if not is_return_dataframe:
        return res.response

    return pd.DataFrame(res.response)


async def delete(
    self: DomoDataset_Default,
    dataset_id=None,
    auth: DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    dataset_id = dataset_id or self.id
    auth = auth or self.auth

    res = await dataset_routes.delete(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )

    return res


async def share(
    self: DomoDataset_Default,
    member,  # DomoUser or DomoGroup
    auth: DomoAuth = None,
    share_type: ShareDataset_AccessLevelEnum = ShareDataset_AccessLevelEnum.CAN_SHARE,
    is_send_email=False,
    debug_api: bool = False,
    debug_prn: bool = False,
    session: httpx.AsyncClient = None,
):
    body = dataset_routes.generate_share_dataset_payload(
        entity_type="GROUP" if type(member).__name__ == "DomoGroup" else "USER",
        entity_id=int(member.id),
        access_level=share_type,
        is_send_email=is_send_email,
    )

    res = await dataset_routes.share_dataset(
        auth=auth or self.auth,
        dataset_id=self.id,
        body=body,
        session=session,
        debug_api=debug_api,
    )

    return res


async def index_dataset(
    self: DomoDataset_Default,
    auth: DomoAuth = None,
    dataset_id: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth
    dataset_id = dataset_id or self.id
    return await dataset_routes.index_dataset(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )


async def upload_data(
    self: DomoDataset_Default,
    upload_df: pd.DataFrame = None,
    upload_df_ls: list[pd.DataFrame] = None,
    upload_file: io.TextIOWrapper = None,
    upload_method: str = "REPLACE",  # APPEND or REPLACE
    partition_key: str = None,
    is_index: bool = True,
    dataset_upload_id=None,
    session: httpx.AsyncClient = None,
    debug_api: bool = False,
    debug_prn: bool = False,
):
    auth = self.auth
    dataset_id = self.id

    upload_df_ls = upload_df_ls or [upload_df]

    status_message = f"{dataset_id} {partition_key} | {auth.domo_instance}"

    # stage 1 get uploadId
    retry = 1
    while dataset_upload_id is None and retry < 5:
        try:
            if debug_prn:
                print(f"\n\n🎭 starting Stage 1 - {status_message}")

            res = await dataset_routes.upload_dataset_stage_1(
                auth=auth,
                dataset_id=dataset_id,
                session=session,
                partition_tag=partition_key,
                debug_api=debug_api,
            )
            if debug_prn:
                print(f"\n\n🎭 Stage 1 response -- {res.status} for {status_message}")

            dataset_upload_id = res.response

        except dataset_routes.UploadDataError as e:
            print(f"{e} - attempt{retry}")
            retry += 1

            if retry == 5:
                print(f"failed to upload data for {dataset_id} in {auth.domo_instance}")
                raise e
                return

            await asyncio.sleep(5)

    # stage 2 upload_dataset
    if upload_file:
        if debug_prn:
            print(f"\n\n🎭 starting Stage 2 - upload file for {status_message}")

        res = await dmce.gather_with_concurrency(
            n=60,
            *[
                dataset_routes.upload_dataset_stage_2_file(
                    auth=auth,
                    dataset_id=dataset_id,
                    upload_id=dataset_upload_id,
                    part_id=1,
                    data_file=upload_file,
                    session=session,
                    debug_api=debug_api,
                )
            ],
        )

    else:
        if debug_prn:
            print(
                f"\n\n🎭 starting Stage 2 - {len(upload_df_ls)} - number of parts for {status_message}"
            )

        res = await dmce.gather_with_concurrency(
            n=60,
            *[
                dataset_routes.upload_dataset_stage_2_df(
                    auth=auth,
                    dataset_id=dataset_id,
                    upload_id=dataset_upload_id,
                    part_id=index + 1,
                    upload_df=df,
                    session=session,
                    debug_api=debug_api,
                )
                for index, df in enumerate(upload_df_ls)
            ],
        )

    if debug_prn:
        print(f"🎭 Stage 2 - upload data: complete for {status_message}")

    # stage 3 commit_data
    if debug_prn:
        print(
            f"\n\n🎭 starting Stage 3 - commit dataset_upload_id for {status_message}"
        )

    await asyncio.sleep(5)  # wait for uploads to finish

    res = await dataset_routes.upload_dataset_stage_3(
        auth=auth,
        dataset_id=dataset_id,
        upload_id=dataset_upload_id,
        update_method=upload_method,
        partition_tag=partition_key,
        is_index=False,
        session=session,
        debug_api=debug_api,
    )

    if debug_prn:
        print(f"\n🎭 stage 3 - commit dataset: complete for {status_message} ")

    if is_index:
        await asyncio.sleep(3)
        return await self.index_dataset(
            auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
        )

    return res


async def list_partitions(
    self: DomoDataset_Default,
    auth: DomoAuth = None,
    dataset_id: str = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
):
    auth = auth or self.auth
    dataset_id = dataset_id or self.id

    res = await dataset_routes.list_partitions(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api, session=session
    )
    if res.status != 200:
        return None

    return res.response


async def create(
    cls: DomoDataset_Default,
    dataset_name: str,
    dataset_type="api",
    schema=None,
    auth: DomoAuth = None,
    debug_api: bool = False,
    session: httpx.AsyncClient = None,
    return_raw: bool = False,
):
    schema = schema or {
        "columns": [
            {"name": "col1", "type": "LONG", "upsertKey": False},
            {"name": "col2", "type": "STRING", "upsertKey": False},
        ]
    }

    res = await dataset_routes.create(
        dataset_name=dataset_name,
        dataset_type=dataset_type,
        schema=schema,
        auth=auth,
        debug_api=debug_api,
        session=session,
    )

    if return_raw:
        return res

    dataset_id = res.response.get("dataSource").get("dataSourceId")

    return await cls.get_by_id(dataset_id=dataset_id, auth=auth)


async def delete_partition(
    self: DomoDataset_Default,
    dataset_partition_id: str,
    dataset_id: str = None,
    empty_df: pd.DataFrame = None,
    auth: DomoAuth = None,
    is_index: bool = True,
    debug_api: bool = False,
    debug_prn: bool = False,
    return_raw: bool = False,
):
    auth = auth or self.auth
    dataset_id = dataset_id or self.id

    if empty_df is None:
        empty_df = await self.query_dataset_private(
            sql="SELECT * from table limit 1",
            debug_api=debug_api,
        )

        await self.upload_data(
            upload_df=empty_df.head(0),
            upload_method="REPLACE",
            is_index=is_index,
            partition_key=dataset_partition_id,
            debug_api=debug_api,
        )

    if debug_prn:
        print("\n\n🎭 starting Stage 1")

    res = await dataset_routes.delete_partition_stage_1(
        auth=auth,
        dataset_id=dataset_id,
        dataset_partition_id=dataset_partition_id,
        debug_api=debug_api,
    )
    if debug_prn:
        print(f"\n\n🎭 Stage 1 response -- {res.status}")
        print(res)

    if debug_prn:
        print("starting Stage 2")

    res = await dataset_routes.delete_partition_stage_2(
        auth=auth,
        dataset_id=dataset_id,
        dataset_partition_id=dataset_partition_id,
        debug_api=debug_api,
    )

    if debug_prn:
        print(f"\n\n🎭 Stage 2 response -- {res.status}")

    if debug_prn:
        print("starting Stage 3")

    res = await dataset_routes.index_dataset(
        auth=auth, dataset_id=dataset_id, debug_api=debug_api
    )
    if debug_prn:
        print(f"\n\n🎭 Stage 3 response -- {res.status}")

    if return_raw:
        return res

    return res.response


async def reset_dataset(
    self: DomoDataset_Default,
    is_index: bool = True,
    empty_df: pd.DataFrame = None,
    debug_api: bool = False,
):
    execute_reset = input(
        "This function will delete all rows.  Type BLOW_ME_AWAY to execute:"
    )

    if execute_reset != "BLOW_ME_AWAY":
        print("You didn't type BLOW_ME_AWAY, moving on.")
        return None

    # create empty dataset to retain schema
    empty_df = empty_df or (
        await self.query_dataset_private(
            auth=self.auth,
            dataset_id=self.id,
            sql="SELECT * from table limit 1",
            debug_api=debug_api,
        )
    )

    empty_df = pd.DataFrame(columns=empty_df.columns)

    # get partition list
    partition_list = await self.list_partitions()
    if len(partition_list) > 0:
        partition_list = dmce.chunk_list(partition_list, 100)

    for index, pl in enumerate(partition_list):
        print(f"🥫 starting chunk {index + 1} of {len(partition_list)}")

        await asyncio.gather(
            *[
                self.delete_partition(
                    auth=self.auth,
                    dataset_partition_id=partition.get("partitionId"),
                    empty_df=empty_df,
                    debug_api=debug_api,
                )
                for partition in pl
            ]
        )
        if is_index:
            await self.index_dataset()

    res = await self.upload_data(
        upload_df=empty_df,
        upload_method="REPLACE",
        is_index=is_index,
        debug_api=debug_api,
    )

    return res


async def upsert_connector(
    self,
    cnfg_body,
    auth: DomoAuth = None,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
):
    if self.stream_id:
        return await self.Stream.update_stream(
            cnfg_body,
            stream_id=self.stream_id,
            auth=auth,
            session=session,
            debug_api=False,
        )
    self.Stream = await self.Stream.create_stream(
        cnfg_body, auth=auth, session=session, debug_api=debug_api
    )

    return self.Stream


@staticmethod
def _is_federated_dataset_obj(obj: dict) -> bool:
    """Heuristic: decide if a dataset JSON represents a federated (proxy) dataset."""

    dpt = obj.get("dataProviderType", "").upper()
    disp = obj.get("displayType", "").upper()

    has_hint = any(
        [
            bool(obj.get("federation")),
            bool(obj.get("federationData")),
            bool(obj.get("federatedDatasetId")),
            bool(obj.get("publisherDomain")),
            obj.get("isFederated") is True,
        ]
    )

    has_federate = any(["FEDERAT" in dpt, "FEDERAT" in disp])
    return has_hint or has_federate


@dataclass
class FederatedDomoDataset(DomoDataset_Default, DomoFederatedEntity):
    """Federated dataset seen in a parent instance; points to a child instance's native dataset."""

    async def get_federated_parent(
        self,
        parent_auth: DomoAuth = None,
        parent_auth_retrieval_fn: Callable = None,
    ):
        raise NotImplementedError("To Do")

    @classmethod
    async def get_by_id(
        cls,
        dataset_id: str,
        auth: DomoAuth,
        debug_api: bool = False,
        return_raw: bool = False,
        session: httpx.AsyncClient = None,
        debug_num_stacks_to_drop=2,
        is_use_default_dataset_class: bool = False,
        parent_class: str = None,
    ):
        """retrieves dataset metadata"""

        parent_class = parent_class or cls.__name__

        res = await dataset_routes.get_dataset_by_id(
            auth=auth,
            dataset_id=dataset_id,
            debug_api=debug_api,
            session=session,
            debug_num_stacks_to_drop=debug_num_stacks_to_drop,
            parent_class=parent_class,
        )

        if return_raw:
            return res

        return cls.from_dict(
            obj=res.response,
            auth=auth,
            new_cls=cls,
            is_use_default_dataset_class=is_use_default_dataset_class,
        )


@dataclass
class DomoPublishDataset(FederatedDomoDataset, DomoPublishedEntity):
    async def get_subscription(self):
        return await super().get_subscription()

    async def get_parent_publication(self):
        return await super().get_parent_publication()


@dataclass
class DomoDataset(DomoDataset_Default):
    # def __post_init__(self):
    #     super().__init__(**self.__dict__)

    @classmethod
    def from_dict(
        cls,
        obj: dict,
        # is_admin_summary: bool = True,
        auth: DomoAuth = None,
        is_use_default_dataset_class=False,
        new_cls=None,
        **kwargs,
    ):
        """converts data_v1_accounts API response into an accounts class object"""

        is_federated = cls._is_federated_dataset_obj(obj)

        new_cls = DomoDataset

        if is_federated and not is_use_default_dataset_class:
            new_cls = FederatedDomoDataset

        # TO DO -- how do we know if it's published?

        return super().from_dict(
            auth=auth,
            obj=obj,
            is_use_default_dataset_class=is_use_default_dataset_class,
            new_cls=new_cls,
            **kwargs,
        )
