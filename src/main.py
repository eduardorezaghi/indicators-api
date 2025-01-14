# main.py


from flask import Flask


from .config import settings

# from .presentation.api.routes import bp as user_routes

# app.register_blueprint(user_routes, url_prefix=f"{settings.API_V1_PREFIX}/users")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=settings.DATABASE,
    )

    from src.database import init_app

    init_app(app)

    @app.route("/")
    def index() -> str:
        return "Hello, World!"

    return app
