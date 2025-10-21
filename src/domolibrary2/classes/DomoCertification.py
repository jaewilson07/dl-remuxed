__all__ = ["DomoCertificationState", "DomoCertification"]

import datetime as dt
from dataclasses import dataclass
from enum import Enum

from ..client.entities import DomoEnumMixin, DomoSubEntity
from ..utils import convert as cd


class DomoCertificationState(DomoEnumMixin, Enum):
    CERTIFIED = "certified"
    PENDING = "PENDING"
    EXPIRED = "EXPIRED"


@dataclass
class DomoCertification(DomoSubEntity):
    certification_state: DomoCertificationState
    last_updated: dt.datetime
    certification_type: str
    certification_name: str

    @classmethod
    def from_parent(cls, parent):
        certification = parent.raw["certification"]

        cert_state = None

        if isinstance(certification.get("state"), dict):
            cert_state = DomoCertificationState[certification.get["state"].get("value")]

        if isinstance(certification.get("state"), str):
            cert_state = DomoCertificationState[certification["state"]]

        return cls(
            auth=parent.auth,
            parent=parent,
            parent_id=parent.id,
            certification_state=cert_state,
            last_updated=cd.convert_epoch_millisecond_to_datetime(
                certification.get("lastUpdated")
            ),
            certification_type=certification.get("processType"),
            certification_name=certification.get("processName"),
        )

    @classmethod
    def from_dict(
        cls,
        data,
        parent=None,
        parent_id=None,
        auth=None,
    ):
        """
        Create a DomoCertification from a dictionary.
        """
        return cls(
            auth=auth,
            parent=parent,
            parent_id=parent_id,
            certification_state=DomoCertificationState[data["state"]],
            last_updated=cd.convert_epoch_millisecond_to_datetime(data["lastUpdated"]),
            certification_type=data["processType"],
            certification_name=data["processName"],
        )
