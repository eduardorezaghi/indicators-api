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

    def get_by_id(self, id):
        raise NotImplementedError

    def get_paginated(self, page, per_page, order_by_param):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError
