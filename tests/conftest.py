from typing import Generator

import pytest
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from src.config import Settings
from src.database import destroy_db, init_db
from src.main import create_app

load_dotenv()


test_settings = Settings(
    SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    TESTING=True,
)


@pytest.fixture(scope="session")
def test_db() -> SQLAlchemy:
    return SQLAlchemy(
        engine_options={"echo": test_settings.DB_ECHO_LOG},
    )


class CustomClient(FlaskClient):
    def open(self, *args, **kwargs):  # type: ignore
        kwargs.setdefault("content_type", "application/json")
        return super().open(*args, **kwargs)


@pytest.fixture(scope="session")
def default_app() -> Flask:
    return create_app()


@pytest.fixture(scope="session", autouse=True)
def app(test_db: SQLAlchemy) -> Generator[Flask, None, None]:
    app = create_app(settings_dict=test_settings, db=test_db)

    with app.app_context():
        init_db(test_db)
        # Custom test client with default content type set to application/json.
        app.test_client_class = CustomClient
        yield app
        destroy_db(test_db)


@pytest.fixture
def client(app: Flask) -> Flask.test_client:  # type: ignore
    return app.test_client()


@pytest.fixture
def runner(app: Flask) -> Flask.test_cli_runner:  # type: ignore
    return app.test_cli_runner()
