from typing import Any

import sqlalchemy
import werkzeug.exceptions
from sqlalchemy import select

from src.database import default_db as db
from src.domain import Angel as AngelDomain
from src.models import Angel
from src.repositories.base import BaseRepository


class AngelRepository(BaseRepository):
    async def get_by_name(self, name: str) -> Angel | None:
        with db.session() as session:
            stmt = select(Angel).where(Angel.name == name)
            return session.execute(stmt).scalar_one_or_none()

    async def create(self, angel: AngelDomain) -> Angel:
        entity = await self.get_by_name(angel.name)
        entity = Angel(name=angel.name)

        try:
            with db.session() as session:
                session.add(entity)
                session.commit()
                session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e
            )

        return entity

    async def get_by_attribute(self, attribute: Any) -> Angel | None:
        pass

    async def get_by_id(self, id: int) -> Angel | None:
        pass

    async def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Angel]:
        raise NotImplementedError

    async def update(self, entity: Angel) -> Angel:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError
