# mypy: ignore-errors

from collections.abc import Generator

import pytest
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.database import destroy_db, init_db
from src.models import Angel


class TestAngelModel:
    @pytest.fixture
    def session(self) -> Generator[Session, None, None]:
        init_db(db)
        session = db.session
        yield session
        destroy_db(db)
        session.rollback()
        session.close()

    def test_create_angel(self, session: Session):
        angel = Angel(name="Angel A")

        session.add(angel)
        session.commit()

        query_obj = session.query(Angel).filter_by(name="Angel A")

        assert query_obj.count() == 1
        assert angel.id is not None

    def test_created_at_is_not_none(self, session: Session):
        angel = Angel(name="Angel A")

        session.add(angel)
        session.commit()

        query_obj = session.query(Angel).filter_by(name="Angel A").first()

        assert query_obj.created_at is not None

    def test_updated_at_deleted_at_are_none(self, session: Session):
        angel = Angel(name="Angel A")

        session.add(angel)
        session.commit()

        query_obj = session.query(Angel).filter_by(name="Angel A").first()

        assert query_obj.updated_at is None
        assert query_obj.deleted_at is None

    def test_unique_constraint_angel(self, session: Session):
        angel1 = Angel(name="Angel A")
        session.add(angel1)
        session.commit()

        angel2 = Angel(name="Angel A")
        session.add(angel2)
        with pytest.raises(sqlalchemy.exc.IntegrityError) as exc_info:
            session.commit()

        assert "UNIQUE constraint failed: angel.name" in str(exc_info.value)
