from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import Engine, create_engine

from src.config import Settings
from src.database import destroy_db, init_db
from src.main import create_app

test_settings = Settings(
    DATABASE="sqlite:///:memory:",
    TESTING=True,
)


class CustomClient(FlaskClient):
    def open(self, *args, **kwargs):  # type: ignore
        kwargs.setdefault("content_type", "application/json")
        return super().open(*args, **kwargs)


@pytest.fixture(scope="session")
def sqlalchemy_custom_engine() -> Generator[Engine, None, None]:
    engine = create_engine(
        test_settings.DATABASE,
        echo=test_settings.DB_ECHO_LOG,
    )

    yield engine


@pytest.fixture(scope="session", autouse=True)
def app(sqlalchemy_custom_engine: Engine) -> Generator[Flask, None, None]:
    app = create_app(test_settings)

    init_db(engine=sqlalchemy_custom_engine)
    # Custom test client with default content type set to application/json.
    app.test_client_class = CustomClient
    yield app
    destroy_db(engine=sqlalchemy_custom_engine)


@pytest.fixture
def client(app: Flask) -> Flask.test_client:
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> Flask.test_cli_runner:
    return app.test_cli_runner()
