from typing import Any, Sequence
import sqlalchemy
import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import default_db as db
from src.domain import Client as ClientDomain
from src.models import Client
from src.repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    def __init__(self, session: Session = db.session, async_session: AsyncSession = None):
        self.session = session
        self.async_session = async_session

    def get_by_id(self, id: int) -> Client | None:
        stmt = select(Client).where(Client.id == id)
        return self.session.execute(stmt).scalar_one_or_none()

    async def get_by_id_async(self, id: int) -> Client | None:
        stmt = select(Client).where(Client.id == id)
        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ids_async(self, ids: list[int]) -> Sequence[Client]:
        stmt = select(Client).where(Client.id.in_(ids))
        result = await self.async_session.execute(stmt)
        return result.scalars().all()

    def create(self, client: ClientDomain) -> Client:
        entity = Client(**client.to_dict())

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

    async def create_async(self, client: ClientDomain) -> Client:
        entity = Client(**client.to_dict())

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

    async def bulk_create_async(self, clients: list[ClientDomain]) -> list[Client]:
        entities = [Client(**client.to_dict()) for client in clients]

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

    def get_by_attribute(self, attribute: Any) -> Client | None:
        raise NotImplementedError

    def get_paginated(self, page: int, per_page: int, order_by_param: str) -> list[Client]:
        raise NotImplementedError

    def update(self, entity: Client) -> Client | None:
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
