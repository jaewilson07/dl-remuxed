"""a class based approach for interacting with Domo Datasets"""

__all__ = [
    "DatasetSchema_Types",
    "DomoDataset_Schema_Column",
    "DomoDataset_Schema",
    "DatasetSchema_InvalidSchema",
]

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, TYPE_CHECKING

import pandas as pd

from ..client import auth as dmda
from ..client import exceptions as dmde
from ..routes import dataset as dataset_routes
from ..client.entities import DomoSubEntity


class DatasetSchema_Types(Enum):
    STRING = "STRING"
    DOUBLE = "DOUBLE"
    LONG = "LONG"
    DATE = "DATE"
    DATETIME = "DATETIME"


@dataclass
class DomoDataset_Schema_Column:
    name: str
    id: str
    type: DatasetSchema_Types
    order: int = 0
    visible: bool = True
    upsert_key: bool = False
    tags: List[Any] = field(default_factory=list)  # DomoTag

    def __eq__(self, other):
        return self.id == other.id

    def replace_tag(self, tag_prefix, new_tag):
        tags_copy = self.tags.copy()

        for tag in tags_copy:
            if tag.startswith(tag_prefix):
                self.tags.remove(tag)
                self.tags.append(new_tag)
                return True

    @classmethod
    def from_dict(cls, obj: dict):
        # from . import DomoTag as dmtg

        return cls(
            name=obj.get("name"),
            id=obj.get("id"),
            type=obj.get("type"),
            visible=obj.get("visible") or obj.get("isVisible") or True,
            upsert_key=obj.get("upsertKey") or False,
            order=obj.get("order") or 0,
            tags=obj.get("tags", []),  # Assuming tags are a list of objects
        )

    def to_dict(self):
        s = self.__dict__
        s["upsertKey"] = s.pop("upsert_key") if "upsert_key" in s else False
        s["tags"] = list(set(s["tags"]))  # Convert to set to remove duplicates
        return s


@dataclass
class DomoDataset_Schema(DomoSubEntity):
    """class for interacting with dataset schemas"""

    auth: dmda.DomoAuth = field(repr=False)
    parent: Any = field(repr=False)

    parent_id: str

    columns: List[DomoDataset_Schema_Column] = field(default_factory=list)

    def __post_init__(self):
        if self.parent:
            self.auth = self.parent.auth
            self.parent_id = self.parent.id

    # @classmethod
    # def _from_parent(cls, parent):
    #     schema = cls(
    #         parent = parent,
    #         auth = parent.auth,
    #         parent_id = parent.id,
    #     )

    #     parent.Schema = schema
    #     return schema

    def to_dict(self):
        return {"columns": [col.to_dict() for col in self.columns]}

    async def get(
        self,
        debug_api: bool = False,
        return_raw: bool = False,  # return the raw response
    ) -> List[DomoDataset_Schema_Column]:
        """method that retrieves schema for a dataset"""

        res = await dataset_routes.get_schema(
            auth=self.auth, dataset_id=self.parent_id, debug_api=debug_api
        )

        self.raw = res.response

        if return_raw:
            return res

        self.columns = [
            DomoDataset_Schema_Column.from_dict(obj=obj)
            for obj in res.response.get("tables")[0].get("columns")
        ]

        return self.columns

    async def _test_missing_columns(
        self: "DomoDataset_Schema",
        df: pd.DataFrame,
        dataset_id=None,
        auth: "dmda.DomoAuth" = None,
    ):

        dataset_id = dataset_id or self.parent.id
        auth = auth or self.parent.auth

        await self.get()

        missing_columns = [
            col for col in df.columns if col not in [scol.name for scol in self.columns]
        ]

        if len(missing_columns) > 0:
            raise DatasetSchema_InvalidSchema(
                domo_instance=auth.domo_instance,
                dataset_id=dataset_id,
                missing_columns=missing_columns,
            )

        return True


class DatasetSchema_InvalidSchema(dmde.DomoError):
    async def reset_col_order(self: "DomoDataset_Schema", df: pd.DataFrame):
        from ..routes import dataset as dataset_routes

        await self.get()

        if len(self.columns) != len(df.columns):
            raise Exception("")

        for index, col in enumerate(self.schema.columns):
            col.order = col.order if col.order > 0 else index

        return await dataset_routes.alter_schema(
            auth=self.auth, dataset_id=self.parent.id, schema_obj=self.schema
        )

    def add_col(
        self: "DomoDataset_Schema",
        col: "DomoDataset_Schema_Column",
        debug_prn: bool = False,
    ):

        if col in self.columns and debug_prn:
            print(
                f"column - {col.name} already in dataset {self.parent.name if self.parent else '' }"
            )

        if col not in self.columns:
            self.columns.append(col)

        return self.columns

    def remove_col(
        self: "DomoDataset_Schema",
        col_to_remove: "DomoDataset_Schema_Column",
        debug_prn: bool = False,
    ):

        [
            self.columns.pop(index)
            for index, col in enumerate(self.columns)
            if col == col_to_remove
        ]

        return self.columns

    async def alter_schema(
        self: "DomoDataset_Schema",
        dataset_id: str = None,
        auth: "dmda.DomoAuth" = None,
        return_raw: bool = False,
        debug_api: bool = False,
    ):

        dataset_id = dataset_id or self.parent.id
        auth = auth or self.parent.auth

        schema_obj = self.to_dict()

        if return_raw:
            return schema_obj

        res = await dataset_routes.alter_schema(
            dataset_id=dataset_id, auth=auth, schema_obj=schema_obj, debug_api=debug_api
        )

        if not res.is_success:
            raise CRUD_Dataset_Error(
                auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
            )

        return res

    async def alter_schema_descriptions(
        self: "DomoDataset_Schema",
        dataset_id: str = None,
        auth: "dmda.DomoAuth" = None,
        return_raw: bool = False,
        debug_api: bool = False,
    ):

        dataset_id = dataset_id or self.parent.id
        auth = auth or self.parent.auth

        schema_obj = self.to_dict()

        if return_raw:
            return schema_obj

        res = await dataset_routes.alter_schema_descriptions(
            dataset_id=dataset_id, auth=auth, schema_obj=schema_obj, debug_api=debug_api
        )

        if not res.is_success:
            raise CRUD_Dataset_Error(
                auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
            )

        return res


@patch_to(DomoDataset_Schema)
async def _test_missing_columns(
    self: DomoDataset_Schema,
    df: pd.DataFrame,
    dataset_id=None,
    auth: dmda.DomoAuth = None,
):
    dataset_id = dataset_id or self.parent.id
    auth = auth or self.parent.auth

    await self.get()

    missing_columns = [
        col for col in df.columns if col not in [scol.name for scol in self.columns]
    ]

    if len(missing_columns) > 0:
        raise DatasetSchema_InvalidSchema(
            domo_instance=auth.domo_instance,
            dataset_id=dataset_id,
            missing_columns=missing_columns,
        )

    return False


@patch_to(DomoDataset_Schema)
async def reset_col_order(self: DomoDataset_Schema, df: pd.DataFrame):
    from ..routes import dataset as dataset_routes

    await self.get()

    if len(self.columns) != len(df.columns):
        raise Exception("")

    for index, col in enumerate(self.schema.columns):
        col.order = col.order if col.order > 0 else index

    return await dataset_routes.alter_schema(
        auth=self.auth, dataset_id=self.parent.id, schema_obj=self.schema
    )


@patch_to(DomoDataset_Schema)
def add_col(
    self: DomoDataset_Schema, col: DomoDataset_Schema_Column, debug_prn: bool = False
):
    if col in self.columns and debug_prn:
        print(
            f"column - {col.name} already in dataset {self.parent.name if self.parent else ''}"
        )

    if col not in self.columns:
        self.columns.append(col)

    return self.columns


@patch_to(DomoDataset_Schema)
def remove_col(
    self: DomoDataset_Schema,
    col_to_remove: DomoDataset_Schema_Column,
    debug_prn: bool = False,
):
    [
        self.columns.pop(index)
        for index, col in enumerate(self.columns)
        if col == col_to_remove
    ]

    return self.columns


class CRUD_Dataset_Error(dmde.DomoError):
    def __init__(self, auth, res, message):
        super().__init__(
            status=res.status,
            function_name=res.traceback_details.function_name,
            parent_class=res.traceback_details.parent_class,
            message=message or res.response,
            domo_instance=auth.domo_instance,
        )


@patch_to(DomoDataset_Schema)
async def alter_schema(
    self: DomoDataset_Schema,
    dataset_id: str = None,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    dataset_id = dataset_id or self.parent.id
    auth = auth or self.parent.auth

    schema_obj = self.to_dict()

    if return_raw:
        return schema_obj

    res = await dataset_routes.alter_schema(
        dataset_id=dataset_id, auth=auth, schema_obj=schema_obj, debug_api=debug_api
    )

    if not res.is_success:
        raise CRUD_Dataset_Error(
            auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
        )

    return res


@patch_to(DomoDataset_Schema)
async def alter_schema_descriptions(
    self: DomoDataset_Schema,
    dataset_id: str = None,
    auth: dmda.DomoAuth = None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    dataset_id = dataset_id or self.parent.id
    auth = auth or self.parent.auth

    schema_obj = self.to_dict()

    if return_raw:
        return schema_obj

    res = await dataset_routes.alter_schema_descriptions(
        dataset_id=dataset_id, auth=auth, schema_obj=schema_obj, debug_api=debug_api
    )

    if not res.is_success:
        raise CRUD_Dataset_Error(
            auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
        )

    return res
