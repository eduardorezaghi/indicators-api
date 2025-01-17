from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

import click
from flask import g  # for managing db session context.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings


# new in SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass


default_db = SQLAlchemy(
    model_class=Base,
    engine_options={"echo": settings.DB_ECHO_LOG},
)

# local async engine for Celery tasks (not attached to Flask app).
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI_ASYNC, echo=settings.DB_ECHO_LOG)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def init_app(app: Any) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def close_db(e: Optional[Exception] = None) -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()


# Inject a custom engine, if passed (mainly used in tests).
def init_db(db: SQLAlchemy = default_db) -> None:
    from src.models import Delivery, Angel, Client, Polo  # noqa

    db.create_all()


def destroy_db(db: SQLAlchemy = default_db) -> None:
    db.drop_all()


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the database.")
