from typing import Any

import sqlalchemy
import werkzeug.exceptions
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.domain import Angel as AngelDomain
from src.models import Angel
from src.repositories.base import BaseRepository


class AngelRepository(BaseRepository):
    def __init__(self, session: Session = db.session):
        self.session = session

    def get_by_name(self, name: str) -> Angel | None:
        stmt = select(Angel).where(Angel.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    def bulk_create(self, angels: list[AngelDomain]) -> list[Angel]:  # pragma: no cover
        entities = [Angel(name=angel.name) for angel in angels]

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


    def get_by_names(self, names: list[str]) -> list[Angel]:  # pragma: no cover
        stmt = select(Angel).where(Angel.name.in_(names))
        result = self.session.execute(stmt)
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
                original_exception=e,
            )

        return entity

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
