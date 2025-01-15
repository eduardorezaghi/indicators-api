# mypy: ignore-errors
def test_db_connection_string_is_correct_default_app(default_app):
    import os
    assert default_app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("SQLALCHEMY_DATABASE_URI")


def test_db_connection_string_is_correct_test_app(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
