from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse


def handle_date(date: str) -> datetime | None:
    try:
        return parse(date)  # type: ignore
    except Exception:
        return None


def _to_dict(obj: object) -> dict:
    dict = {}
    for k, v in asdict(obj).items():
        if v is not None or v != -999:
            dict[k] = v
    return dict


@dataclass
class Delivery:
    id: int | None
    cliente_id: int
    angel: str
    polo: str
    data_limite: datetime
    data_de_atendimento: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Delivery":
        return cls(
            id=int(data.get("id_atendimento", -999)),
            cliente_id=int(data.get("id_cliente", -999)),
            angel=data.get("angel", None),
            polo=data.get("polo", None),
            data_limite=handle_date(data.get("data_limite", None)),
            data_de_atendimento=handle_date(data.get("data_de_atendimento", None)),
        )

    def to_dict(self) -> dict:
        # Only include non-None values
        return _to_dict(self)


@dataclass
class DeliveryDomainCreate:
    cliente_id: int
    id_angel: int
    id_polo: int
    data_limite: datetime
    data_de_atendimento: datetime
    id: int | None = None

    def to_dict(self) -> dict:
        # Only include non-None values
        return _to_dict(self)


@dataclass
class DeliveryDomainUpdate:
    id: int
    data_limite: datetime
    data_de_atendimento: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "DeliveryDomainUpdate":
        return cls(
            id=int(data.get("id_atendimento", -999)),
            data_limite=handle_date(data.get("data_limite", None)),
            data_de_atendimento=handle_date(data.get("data_de_atendimento", None)),
        )

    def to_dict(self) -> dict:
        # Only include non-None values
        return _to_dict(self)
