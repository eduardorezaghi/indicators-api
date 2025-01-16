import sqlalchemy
import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select

from src.database import default_db as db
from src.domain import Client as ClientDomain
from src.models import Client
from src.repositories.base import BaseRepository


class ClientRepository(BaseRepository):
    async def get_by_id(self, id: int) -> Client | None:
        with db.session() as session:
            stmt = select(Client).where(Client.id == id)
            return session.execute(stmt).scalar_one_or_none()

    async def create(self, client: ClientDomain) -> Client:
        entity = Client(**client.to_dict())

        try:
            with db.session() as session:
                session.add(entity)
                session.commit()
                session.refresh(entity)
        except sqlalchemy.exc.DBAPIError as e:
            session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entity.",
                original_exception=e,
            )

        return entity

    async def get_by_attribute(self, attribute):
        raise NotImplementedError

    async def get_paginated(self, page, per_page, order_by_param):
        raise NotImplementedError

    async def update(self, entity):
        raise NotImplementedError

    async def delete(self, id):
        raise NotImplementedError
