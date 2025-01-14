# mypy: ignore-errors


def test_db_connection_string_is_correct_default_app(default_app):
    assert default_app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///./test.sqlite3"


def test_db_connection_string_is_correct_test_app(
    app,
):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
