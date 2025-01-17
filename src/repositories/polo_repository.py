from typing import Any

import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import default_db as db
from src.domain import Polo as PoloDomain
from src.models import Polo
from src.repositories.base import BaseRepository


class PoloRepository(BaseRepository):
    def __init__(self, session: Session = db.session, async_session: AsyncSession = None):
        self.session = session
        self.async_session = async_session

    def get_by_attribute(self, attribute: Any) -> Polo | None:
        stmt = select(Polo).where(Polo.name == attribute)
        return self.session.execute(stmt).scalar_one_or_none()

    async def get_by_attribute_async(self, attribute: Any) -> Polo | None:
        stmt = select(Polo).where(Polo.name == attribute)
        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_attributes_async(self, attributes: list[Any]) -> list[Polo]:
        stmt = select(Polo).where(Polo.name.in_(attributes))
        result = await self.async_session.execute(stmt)
        return result.scalars().all()

    def create(self, polo: PoloDomain) -> Polo:
        entity = Polo(name=polo.name)

        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def create_async(self, polo: PoloDomain) -> Polo:
        entity = Polo(name=polo.name)

        try:
            self.async_session.add(entity)
            await self.async_session.commit()
            await self.async_session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def bulk_create_async(self, polos: list[PoloDomain]) -> list[Polo]:
        entities = [Polo(name=polo.name) for polo in polos]

        try:
            self.async_session.add_all(entities)
            await self.async_session.commit()
        except sqlalchemy.exc.DBAPIError as e:
            await self.async_session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entities.",
                original_exception=e,
            )

        return entities

    def get_by_id(self, id):
        raise NotImplementedError

    async def get_by_id_async(self, id: int):
        try:
            stmt = select(Polo).where(Polo.id == id)
            result = await self.async_session.execute(stmt)
            return result.scalar_one()
        except sqlalchemy.exc.DBAPIError as e:
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to get the entity.",
                original_exception=e,
            )

    def get_paginated(self, page, per_page, order_by_param):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
