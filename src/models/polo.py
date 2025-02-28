from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import default_db
from src.models.base_model import BaseModel

# mypy: ignore-errors
class Polo(BaseModel, default_db.Model):
    __tablename__ = "polo"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    atendimentos: Mapped[list["Delivery"]] = relationship(back_populates="polo") # type: ignore # noqa
