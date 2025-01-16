# mypy: ignore-errors

from datetime import date, datetime

from sqlalchemy.orm import Session

from src.models import Delivery


class TestDeliveryModel:
    def test_create_atendimento(
        self, session: Session, angel_fixture, polo_fixture, client_fixture
    ):
        atendimento = Delivery(
            cliente=client_fixture,
            angel=angel_fixture,
            polo=polo_fixture,
            data_limite=date(2021, 6, 30),
            data_de_atendimento=datetime(2021, 6, 29, 9, 9, 30),
        )

        session.add(atendimento)
        session.commit()

        query_obj = session.query(Delivery).filter_by(
            angel=angel_fixture, polo=polo_fixture, cliente=client_fixture
        )

        assert query_obj.count() == 1
        assert atendimento.id is not None
