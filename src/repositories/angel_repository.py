from typing import Any

import sqlalchemy
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import default_db as db
from src.domain import Angel as AngelDomain
from src.models import Angel
from src.repositories.base import BaseRepository


class AngelRepository(BaseRepository):
    def __init__(self, session: Session = db.session, async_session: AsyncSession = None):
        self.session = session
        self.async_session = async_session

    def get_by_name(self, name: str) -> Angel | None:
        stmt = select(Angel).where(Angel.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    async def get_by_name_async(self, name: str) -> Angel | None:
        stmt = select(Angel).where(Angel.name == name)
        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_names_async(self, names: list[str]) -> list[Angel]:
        stmt = select(Angel).where(Angel.name.in_(names))
        result = await self.async_session.execute(stmt)
        return result.scalars().all()

    def create(self, angel: AngelDomain) -> Angel:
        entity = self.get_by_name(angel.name)
        entity = Angel(name=angel.name)

        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e
            )

        return entity

    async def create_async(self, angel: AngelDomain) -> Angel:
        entity = await self.get_by_name_async(angel.name)
        entity = Angel(name=angel.name)

        try:
            self.async_session.add(entity)
            await self.async_session.commit()
            await self.async_session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e
            )

        return entity

    async def bulk_create_async(self, angels: list[AngelDomain]) -> list[Angel]:
        entities = [Angel(name=angel.name) for angel in angels]

        try:
            self.async_session.add_all(entities)
            await self.async_session.commit()
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entities.",
                original_exception=e
            )

        return entities

    def get_by_attribute(self, attribute: Any) -> Angel | None:
        pass

    def get_by_id(self, id: int) -> Angel | None:
        pass

    def get_paginated(
        self, page: int, per_page: int, order_by_param: str
    ) -> list[Angel]:
        raise NotImplementedError

    def update(self, entity: Angel) -> Angel:
        raise NotImplementedError

    def delete(self, id: int) -> bool:
        raise NotImplementedError
