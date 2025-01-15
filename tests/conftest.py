from typing import Generator

import pytest
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from src.config import Settings
from src.database import destroy_db, init_db
from src.main import create_app

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
