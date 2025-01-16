# mypy: ignore-errors

from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.database import destroy_db, init_db
from src.models import Polo


class TestPoloModel:
    @pytest.fixture
    def session(self) -> Generator[Session, None, None]:
        init_db(db)
        session = db.session
        yield session
        destroy_db(db)
        session.rollback()
        session.close()

    def test_create_polo(self, session: Session):
        polo = Polo(name="SP - SÃO PAULO")

        session.add(polo)
        session.commit()

        query_obj = session.query(Polo).filter_by(name="SP - SÃO PAULO")

        assert query_obj.count() == 1
        assert polo.id is not None

    def test_unique_constraint_polo(self, session: Session):
        polo1 = Polo(name="SP - SÃO PAULO")
        session.add(polo1)
        session.commit()

        polo2 = Polo(name="SP - SÃO PAULO")
        session.add(polo2)
        with pytest.raises(Exception):
            session.commit()

    def test_create_polo_created_at_is_not_none(self, session: Session):
        polo = Polo(name="SP - SÃO PAULO")

        session.add(polo)
        session.commit()

        query_obj = session.query(Polo).filter_by(name="SP - SÃO PAULO").first()

        assert query_obj.created_at is not None
        
    def test_create_polo_updated_at_deleted_at_are_none(self, session: Session):
        polo = Polo(name="SP - SÃO PAULO")

        session.add(polo)
        session.commit()

        query_obj = session.query(Polo).filter_by(name="SP - SÃO PAULO").first()

        assert query_obj.updated_at is None
        assert query_obj.deleted_at is None