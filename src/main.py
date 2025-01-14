# main.py

from flask import Flask

import src.database as db
from src.api import base_routes

from .config import Settings, settings

# app.register_blueprint(user_routes, url_prefix=f"{settings.API_V1_PREFIX}/users")


def create_app(settings_dict: Settings) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=settings_dict.DATABASE,
    )

    db.init_app(app)

    # Blueprints (routes)
    app.register_blueprint(base_routes)

    return app


if __name__ == "__main__":
    settings_dict = settings
    app = create_app(settings_dict)

    # context manager block to initialize the database.
    with app.app_context():
        db.init_db(engine=db.engine)

    app.run(port=settings.PORT, debug=settings.DEBUG)
