from typing import Any

import werkzeug
import werkzeug.exceptions
from flask import Flask
from flask_alembic import Alembic
from flask_celeryext import FlaskCeleryExt
from flask_sqlalchemy import SQLAlchemy

from src.api import atendimento_routes, base_routes
from src.celery_utils import make_celery
from src.database import default_db

from .config import Settings, settings


def handle_exception(e: Exception) -> Any:
    return {"error": str(e)}, 500


def handle_bad_request(e: Exception) -> Any:
    return {"error": str(e)}, 400

def handle_not_found(e: Exception) -> Any:
    return {"error": str(e)}, 404

alembic = Alembic()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)

def create_app(
    settings_dict: Settings = settings,
    db: SQLAlchemy = default_db,
) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=settings_dict.SQLALCHEMY_DATABASE_URI,
        CELERY=dict(
            broker_url=settings_dict.CELERY_BROKER_URL,
            result_backend=settings_dict.CELERY_RESULT_BACKEND,
        )
    )

    # alembic extension
    alembic.init_app(app)
    # SQLAlchemy extension
    db.init_app(app)
    # Celery
    ext_celery.init_app(app)

    # Blueprints (routes)
    app.register_blueprint(base_routes)
    app.register_blueprint(
        atendimento_routes, url_prefix=f"{settings_dict.API_V1_PREFIX}/atendimento"
    )

    app.register_error_handler(code_or_exception=Exception, f=handle_exception)
    app.register_error_handler(code_or_exception=werkzeug.exceptions.BadRequest, f=handle_bad_request)
    app.register_error_handler(code_or_exception=werkzeug.exceptions.InternalServerError, f=handle_exception)
    app.register_error_handler(code_or_exception=werkzeug.exceptions.NotFound, f=handle_not_found)

    return app


