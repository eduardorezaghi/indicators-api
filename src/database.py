from typing import Any, Optional

import click
from flask import g  # for managing db session context.
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from .config import settings

engine = create_engine(
    settings.DATABASE,
    echo=settings.DB_ECHO_LOG,
)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)


# new in SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass


Base.query = db_session.query_property()


def init_app(app: Any) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db() -> scoped_session | Any:
    if "db" not in g:
        g.db = db_session()

    return g.db


def close_db(e: Optional[Exception] = None) -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Inject a custom engine, if passed (mainly used in tests).
def init_db(engine: Engine = engine) -> None:
    from src.models import Person  # noqa

    Base.metadata.create_all(bind=engine)


def destroy_db(engine: Engine = engine) -> None:
    Base.metadata.drop_all(bind=engine)


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the database.")
