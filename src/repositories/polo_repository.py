from typing import Any

import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select

from src.database import default_db as db
from src.domain import Polo as PoloDomain
from src.models import Polo
from src.repositories.base import BaseRepository


class PoloRepository(BaseRepository):
    async def get_by_attribute(self, attribute: Any) -> Polo | None:
        with db.session() as session:
            stmt = select(Polo).where(Polo.name == attribute)
            return session.execute(stmt).scalar_one_or_none()

    async def create(self, polo: PoloDomain) -> Polo:
        entity = Polo(name=polo.name)

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

    async def get_by_id(self, id):
        raise NotImplementedError

    async def get_paginated(self, page, per_page, order_by_param):
        raise NotImplementedError

    async def update(self, entity):
        raise NotImplementedError

    async def delete(self, id):
        raise NotImplementedError
