from dataclasses import dataclass
from datetime import datetime

from dateutil.parser import parse


@dataclass
class Atendimento:
    id_atendimento: int
    id_cliente: int
    angel: str
    polo: str
    data_limite: datetime
    data_de_atendimento: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Atendimento":
        def handle_date(date: str) -> datetime:
            return parse(date)  # type: ignore

        return cls(
            id_atendimento=int(data["id_atendimento"]),
            id_cliente=int(data["id_cliente"]),
            angel=data["angel"],
            polo=data["polo"],
            data_limite=handle_date(data["data_limite"]),
            data_de_atendimento=handle_date(data["data_de_atendimento"]),
        )
