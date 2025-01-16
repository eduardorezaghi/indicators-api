# mypy: ignore-errors

from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.database import destroy_db, init_db
from src.models import Client


class TestClientModel:
    @pytest.fixture
    def session(self) -> Generator[Session, None, None]:
        init_db(db)
        session = db.session
        yield session
        destroy_db(db)
        session.rollback()
        session.close()

    def test_create_client(self, session: Session):
        client = Client(id=1012349)

        session.add(client)
        session.commit()

        query_obj = session.query(Client).filter_by(id=1012349)

        assert query_obj.count() == 1
        assert client.id is not None
