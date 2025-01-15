from dataclasses import dataclass
from datetime import datetime

from dateutil.parser import parse


@dataclass
class Atendimento:
    id_atendimento: int | None
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
            id_atendimento=int(data.get("id_atendimento", 0)),
            id_cliente=int(data.get("id_cliente", 0)),
            angel=data.get("angel", ""),
            polo=data.get("polo", ""),
            data_limite=handle_date(data.get("data_limite", datetime.now().isoformat())),
            data_de_atendimento=handle_date(data.get("data_de_atendimento", datetime.now().isoformat())),
        )

    def to_dict(self) -> dict:
        return {
            "id_cliente": self.id_cliente,
            "angel": self.angel,
            "polo": self.polo,
            "data_limite": self.data_limite,
            "data_de_atendimento": self.data_de_atendimento,
        }
