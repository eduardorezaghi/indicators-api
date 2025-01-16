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

    def test_create_atendimento_created_at_is_not_none(
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

        query_obj = (
            session.query(Delivery)
            .filter_by(angel=angel_fixture, polo=polo_fixture, cliente=client_fixture)
            .first()
        )

        assert query_obj.created_at is not None

    def test_create_atendimento_updated_at_deleted_at_are_none(
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

        query_obj = (
            session.query(Delivery)
            .filter_by(angel=angel_fixture, polo=polo_fixture, cliente=client_fixture)
            .first()
        )

        assert query_obj.updated_at is None
        assert query_obj.deleted_at is None
