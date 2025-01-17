from typing import List

from sqlalchemy import String, Table, Column, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import default_db
from src.models.base_model import BaseModel


# mypy: ignore-errors
class Angel(BaseModel, default_db.Model):
    __tablename__ = "angel"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    atendimentos: Mapped[List["Delivery"]] = relationship(back_populates="angel") # type: ignore # noqa

angel_productivity_view = Table(
    "angel_productivity",
    default_db.metadata,
    Column("courier", Integer),
    Column("total_deliveries", Integer),
    Column("on_time_deliveries", Integer),
    Column("on_time_percentage", Float),
    extend_existing=True,
)

polo_productivity_view = Table(
    "polo_productivity",
    default_db.metadata,
    Column("polo", Integer),
    Column("weekday", String),
    Column("total_deliveries", Integer),
    extend_existing=True,
)