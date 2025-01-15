from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import default_db
from src.models.base_model import BaseModel


# mypy: ignore-errors
class Atendimento(BaseModel, default_db.Model):
    __tablename__ = "atendimento"
    
    id_cliente: Mapped[int] = mapped_column()
    angel: Mapped[str] = mapped_column(String(255))
    polo: Mapped[str] = mapped_column(String(255))
    data_limite: Mapped[date] = mapped_column()
    data_de_atendimento: Mapped[date] = mapped_column()
