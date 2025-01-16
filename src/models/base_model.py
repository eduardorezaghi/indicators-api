from datetime import UTC, datetime
from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

timestamp = Annotated[
    datetime,
    mapped_column(DateTime),
]

class BaseModel:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[timestamp] = mapped_column(server_default=func.current_timestamp(),default=datetime.now(UTC), nullable=False)
    updated_at: Mapped[timestamp] = mapped_column(server_onupdate=func.now(), onupdate=datetime.now(UTC), nullable=True)
    deleted_at: Mapped[timestamp] = mapped_column(server_default=None, nullable=True)
