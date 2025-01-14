# main.py

from typing import Any

from flask import Flask

from src.api import base_routes
from src.database import default_db, init_db

from .config import Settings, settings


def create_app(settings_dict: Settings = settings, db: Any = default_db) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=settings_dict.SQLALCHEMY_DATABASE_URI,
    )

    db.init_app(app)

    # Blueprints (routes)
    app.register_blueprint(base_routes)

    return app


if __name__ == "__main__":
    # use default settings if no custom one is provided, for now.
    app = create_app(db=default_db)

    # context manager block to initialize the database.
    with app.app_context():
        init_db(db=default_db)

    app.run(port=settings.PORT, debug=settings.DEBUG)
