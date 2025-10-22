"""a class based approach for interacting with Domo Datasets"""

__all__ = [
    "DatasetSchema_Types",
    "DomoDataset_Schema_Column",
    "DomoDataset_Schema",
    "DatasetSchema_InvalidSchema",
    "CRUD_Dataset_Error",
]

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional

import pandas as pd

from ...client.auth import DomoAuth
from ...client.entities import DomoSubEntity
from ...client.exceptions import DomoError
from ...routes import dataset as dataset_routes
from ...routes.dataset import Dataset_CRUDError, Dataset_GetError


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

    auth: DomoAuth = field(repr=False)
    parent: Any = field(repr=False)

    parent_id: str

    columns: List[DomoDataset_Schema_Column] = field(default_factory=list)

    def __post_init__(self):
        if self.parent:
            self.auth = self.parent.auth
            self.parent_id = self.parent.id

    # @classmethod
    # def from_parent(cls, parent):
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
        self,
        df: pd.DataFrame,
        dataset_id: Optional[str] = None,
        auth: Optional[DomoAuth] = None,
    ):
        """Test if DataFrame columns match schema columns."""
        dataset_id = dataset_id or self.parent_id
        auth = auth or self.auth

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

    async def reset_col_order(self, df: pd.DataFrame):
        """Reset column order to match DataFrame."""
        await self.get()

        if len(self.columns) != len(df.columns):
            raise Exception(
                f"Column count mismatch: schema has {len(self.columns)} columns, "
                f"but DataFrame has {len(df.columns)} columns. "
                f"Schema columns: {[col.name for col in self.columns]}, "
                f"DataFrame columns: {list(df.columns)}"
            )

        for index, col in enumerate(self.columns):
            col.order = col.order if col.order > 0 else index

        schema_obj = self.to_dict()
        
        return await dataset_routes.alter_schema(
            auth=self.auth, dataset_id=self.parent_id, schema_obj=schema_obj
        )

    def add_col(
        self,
        col: DomoDataset_Schema_Column,
        debug_prn: bool = False,
    ):
        """Add a column to the schema."""
        if col in self.columns and debug_prn:
            print(
                f"column - {col.name} already in dataset {self.parent.name if self.parent else ''}"
            )

        if col not in self.columns:
            self.columns.append(col)

        return self.columns

    def remove_col(
        self,
        col_to_remove: DomoDataset_Schema_Column,
        debug_prn: bool = False,
    ):
        """Remove a column from the schema."""
        [
            self.columns.pop(index)
            for index, col in enumerate(self.columns)
            if col == col_to_remove
        ]

        return self.columns

    async def alter_schema(
        self,
        dataset_id: Optional[str] = None,
        auth: Optional[DomoAuth] = None,
        return_raw: bool = False,
        debug_api: bool = False,
    ):
        """Alter the schema for a dataset (does not alter descriptions)."""
        dataset_id = dataset_id or self.parent_id
        auth = auth or self.auth

        schema_obj = self.to_dict()

        if return_raw:
            return schema_obj

        res = await dataset_routes.alter_schema(
            auth=auth, dataset_id=dataset_id, schema_obj=schema_obj, debug_api=debug_api
        )

        if not res.is_success:
            raise CRUD_Dataset_Error(
                auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
            )

        return res

    async def alter_schema_descriptions(
        self,
        dataset_id: Optional[str] = None,
        auth: Optional[DomoAuth] = None,
        return_raw: bool = False,
        debug_api: bool = False,
    ):
        """Alter the description of schema columns."""
        dataset_id = dataset_id or self.parent_id
        auth = auth or self.auth

        schema_obj = self.to_dict()

        if return_raw:
            return schema_obj

        res = await dataset_routes.alter_schema_descriptions(
            auth=auth, dataset_id=dataset_id, schema_obj=schema_obj, debug_api=debug_api
        )

        if not res.is_success:
            raise CRUD_Dataset_Error(
                auth=auth, res=res, message=f"unable to alter schema for {dataset_id}"
            )

        return res


class DatasetSchema_InvalidSchema(DomoError):
    def __init__(
        self,
        domo_instance: str,
        dataset_id: str,
        missing_columns: List[str],
        **kwargs
    ):
        super().__init__(
            domo_instance=domo_instance,
            message=f"Dataset {dataset_id} schema invalid. Missing columns: {', '.join(missing_columns)}",
            **kwargs
        )


class CRUD_Dataset_Error(DomoError):
    def __init__(
        self,
        auth: DomoAuth,
        res,
        message: str,
        **kwargs
    ):
        super().__init__(
            status=res.status,
            domo_instance=auth.domo_instance,
            message=message or str(res.response),
            **kwargs
        )



