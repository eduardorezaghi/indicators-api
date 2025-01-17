from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import default_db
from src.models.angel import Angel
from src.models.base_model import BaseModel, timestamp
from src.models.client import Client
from src.models.polo import Polo


# mypy: ignore-errors
class Delivery(BaseModel, default_db.Model):
    __tablename__ = "atendimento"

    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    id_angel: Mapped[int] = mapped_column(ForeignKey("angel.id"))
    id_polo: Mapped[int] = mapped_column(ForeignKey("polo.id"))
    data_limite: Mapped[timestamp] = mapped_column(index=True)
    data_de_atendimento: Mapped[timestamp] = mapped_column(index=True)

    cliente: Mapped[Client] = relationship("Client")
    angel: Mapped[Angel] = relationship("Angel")
    polo: Mapped[Polo] = relationship("Polo")
