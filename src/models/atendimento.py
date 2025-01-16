from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import default_db
from src.models.angel import Angel
from src.models.base_model import BaseModel
from src.models.client import Client
from src.models.polo import Polo


# mypy: ignore-errors
class Delivery(BaseModel, default_db.Model):
    __tablename__ = "atendimento"

    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    angel_id: Mapped[int] = mapped_column(ForeignKey("angel.id"))
    polo_id: Mapped[int] = mapped_column(ForeignKey("polo.id"))
    data_limite: Mapped[datetime] = mapped_column()
    data_de_atendimento: Mapped[datetime] = mapped_column()

    cliente: Mapped[Client] = relationship("Client")
    angel: Mapped[Angel] = relationship("Angel")
    polo: Mapped[Polo] = relationship("Polo")
