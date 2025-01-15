
from flask import Flask
from flask_alembic import Alembic
from flask_sqlalchemy import SQLAlchemy

from src.api import atendimento_routes, base_routes
from src.database import default_db, init_db

from .config import Settings, settings


def create_app(
    settings_dict: Settings = settings,
    db: SQLAlchemy = default_db,
) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    alembic = Alembic()

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=settings_dict.SQLALCHEMY_DATABASE_URI,
    )

    # alembic extension
    alembic.init_app(app)
    # SQLAlchemy extension
    db.init_app(app)

    # Blueprints (routes)
    app.register_blueprint(base_routes)
    app.register_blueprint(
        atendimento_routes, url_prefix=f"{settings_dict.API_V1_PREFIX}/atendimento"
    )

    return app


if __name__ == "__main__":
    # use default settings if no custom one is provided, for now.
    app = create_app(db=default_db)

    # context manager block to initialize the database.
    with app.app_context():
        init_db(db=default_db)

    app.run(
        host=settings.FLASK_RUN_HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )
