from dataclasses import asdict, dataclass
from datetime import datetime

from dateutil.parser import parse


@dataclass
class Delivery:
    id: int | None
    cliente_id: int | None
    angel: str | None
    polo: str | None
    data_limite: datetime | None
    data_de_atendimento: datetime | None

    @classmethod
    def from_dict(cls, data: dict) -> "Delivery":
        def handle_date(date: str) -> datetime | None:
            try:
                return parse(date)  # type: ignore
            except Exception:
                return None

        return cls(
            id=int(data.get("id_atendimento", -999)),
            cliente_id=int(data.get("cliente_id", -999)),
            angel=data.get("angel", None),
            polo=data.get("polo", None),
            data_limite=handle_date(data.get("data_limite", None)),
            data_de_atendimento=handle_date(data.get("data_de_atendimento", None)),
        )

    def to_dict(self) -> dict:
        # Only include non-None values
        dict_ = {}
        for k, v in asdict(self).items():
            if v is not None or v != -999:
                dict_[k] = v
        return dict_


@dataclass
class DeliveryDomainCreate:
    cliente_id: int
    id_angel: int
    id_polo: int
    data_limite: datetime
    data_de_atendimento: datetime

    def to_dict(self) -> dict:
        # Only include non-None values
        dict_ = {}
        for k, v in asdict(self).items():
            if v is not None:
                dict_[k] = v
        return dict_
