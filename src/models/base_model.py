from datetime import datetime, UTC, date

from sqlalchemy.orm import Mapped, mapped_column


class BaseModel:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[date] = mapped_column(default=datetime.now(UTC), index=True)
    updated_at: Mapped[date] = mapped_column(nullable=True, index=True)
    deleted_at: Mapped[date] = mapped_column(nullable=True, default=None, index=True)
