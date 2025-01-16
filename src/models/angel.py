from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import default_db
from src.models.base_model import BaseModel


# mypy: ignore-errors
class Angel(BaseModel, default_db.Model):
    __tablename__ = "angel"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
