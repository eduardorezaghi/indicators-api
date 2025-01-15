# mypy: ignore-errors

from collections.abc import Generator
from datetime import date, datetime

import pytest
from sqlalchemy.orm import Session

from src.database import default_db as db
from src.database import destroy_db, init_db
from src.models import Atendimento


class TestAtendimentoModel:
    @pytest.fixture
    def session(self) -> Generator[Session, None, None]:
        init_db(db)
        session = db.session
        yield session
        destroy_db(db)
        session.rollback()
        session.close()

    def test_create_atendimento(self, session: Session):
        atendimento = Atendimento(
            id_cliente=123456,
            angel="John Doe",
            polo="SP - SÃO PAULO",
            data_limite=date(2021, 6, 30),
            data_de_atendimento=datetime(2021, 6, 29, 9, 9, 30),
        )

        session.add(atendimento)
        session.commit()

        query_obj = session.query(Atendimento).filter_by(angel="John Doe")

        assert query_obj.count() == 1
        assert atendimento.id is not None
