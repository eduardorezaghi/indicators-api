from typing import Any

import sqlalchemy.exc
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.domain import Polo as PoloDomain
from src.models import Polo
from src.repositories.base import BaseRepository


class PoloRepository(BaseRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def get_by_attribute(self, attribute: Any) -> Polo | None:
        stmt = select(Polo).where(Polo.name == attribute)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_attributes(self, attributes: list[Any]) -> list[Polo]:
        stmt = select(Polo).where(Polo.name.in_(attributes))
        result = self.session.execute(stmt)
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

    def bulk_create(self, polos: list[PoloDomain]) -> list[Polo]:
        entities = [Polo(name=polo.name) for polo in polos]

        try:
            self.session.add_all(entities)
            self.session.commit()
        except sqlalchemy.exc.DBAPIError as e:
            self.session.rollback()
            raise werkzeug.exceptions.InternalServerError(
                description="An error occurred while trying to create the entities.",
                original_exception=e,
            )

        return entities

    def get_by_id(self, id):
        raise NotImplementedError

    def get_paginated(self, page, per_page, order_by_param):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
