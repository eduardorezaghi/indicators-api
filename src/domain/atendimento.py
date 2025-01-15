from dataclasses import dataclass
from datetime import datetime


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
        return cls(
            id_atendimento=int(data["id_atendimento"]),
            id_cliente=int(data["id_cliente"]),
            angel=data["angel"],
            polo=data["polo"],
            data_limite=datetime.strptime(data["data_limite"], "%d/%m/%Y"),
            data_de_atendimento=datetime.strptime(data["data_de_atendimento"], "%Y-%m-%d %H:%M:%S"),
        )