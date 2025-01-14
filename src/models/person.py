from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import default_db
from src.models.base_model import BaseModel


class Person(BaseModel, default_db.Model): # mypy: ignore
    __tablename__ = "person"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)

    def __repr__(self) -> str:
        return f"<Person(name={self.name}, email={self.email})>"
