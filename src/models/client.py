from typing import List

from sqlalchemy.orm import relationship, Mapped

from src.database import default_db
from src.models.base_model import BaseModel


# mypy: ignore-errors
class Client(BaseModel, default_db.Model):
    __tablename__ = "cliente"
    atendimentos: Mapped[List["Delivery"]] = relationship(back_populates="cliente") # type: ignore
