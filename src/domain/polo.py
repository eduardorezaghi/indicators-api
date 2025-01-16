from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse


@dataclass
class Polo:
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Polo":
        return cls(
            name=data["name"],
            created_at=parse(data.get("created_at", None)),
            updated_at=parse(data.get("updated_at", None)),
            deleted_at=parse(data.get("deleted_at", None)),
        )

    def to_dict(self) -> dict:
        dict_ = {}
        # Only include non-None values
        for k,v in asdict(self).items():
            if v is not None:
                dict_[k] = v

        return dict_
