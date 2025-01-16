from datetime import datetime
from typing import Generator

import pytest
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from src.config import Settings
from src.database import destroy_db, init_db
from src.app import create_app

load_dotenv()


test_settings = Settings(
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    TESTING=True,
)


class CustomClient(FlaskClient):
    def open(self, *args, **kwargs):  # type: ignore
        kwargs.setdefault("content_type", "application/json")
        return super().open(*args, **kwargs)


@pytest.fixture(scope="session")
def default_app() -> Flask:
    return create_app()


@pytest.fixture(scope="function", autouse=True)
def app() -> Generator[Flask, None, None]:
    app = create_app(settings_dict=test_settings)

    with app.app_context():
        init_db()
        # Custom test client with default content type set to application/json.
        app.test_client_class = CustomClient
        yield app
        destroy_db()


@pytest.fixture
def session() -> Generator[Session, None, None]:
    from src.database import default_db as db

    init_db(db)
    session = db.session
    yield session
    destroy_db(db)
    session.rollback()
    session.close()


@pytest.fixture
def client(app: Flask) -> Flask.test_client:  # type: ignore
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> Flask.test_cli_runner:  # type: ignore
    return app.test_cli_runner()


@pytest.fixture
def angel_fixture(session: Session) -> Generator:
    from src.models import Angel

    angel = Angel(name="John Doe")
    session.add(angel)
    session.commit()

    return angel


@pytest.fixture
def polo_fixture(session: Session) -> Generator:
    from src.models import Polo

    polo = Polo(name="SP - SÃO PAULO")
    session.add(polo)
    session.commit()

    return polo


@pytest.fixture
def client_fixture(session: Session) -> Generator:
    from src.models import Client

    client = Client(id=123456)
    session.add(client)
    session.commit()

    return client


# mypy: ignore-errors
@pytest.fixture
def atendimentos_fixture(
    session: Session, angel_fixture, polo_fixture, client_fixture
) -> Generator:
    from src.models import Delivery

    atendimentos = [
        Delivery(
            cliente=client_fixture,
            angel=angel_fixture,
            polo=polo_fixture,
            data_limite=datetime(2024, 6, 30),
            data_de_atendimento=datetime(2024, 6, 29, 9, 9, 30),
        ),
        Delivery(
            cliente=client_fixture,
            angel=angel_fixture,
            polo=polo_fixture,
            data_limite=datetime(2024, 6, 30),
            data_de_atendimento=datetime(2024, 6, 29, 9, 9, 30),
        ),
    ]

    session.add_all(atendimentos)
    session.commit()

    return atendimentos
