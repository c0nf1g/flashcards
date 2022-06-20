import os

from flashcards import create_app


def test_config_testing():
    app = create_app("testing")
    assert app.config["SECRET_KEY"] != "my code"
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("TEST_DATABASE_URI")
    assert app.config["TOKEN_EXPIRE_HOURS"] == 0
    assert app.config["TOKEN_EXPIRE_MINUTES"] == 0


def test_config_development():
    app = create_app("development")
    assert app.config["SECRET_KEY"] != "my code"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DEV_DATABASE_URI")
    assert app.config["TOKEN_EXPIRE_HOURS"] == 0
    assert app.config["TOKEN_EXPIRE_MINUTES"] == 15


def test_config_production():
    app = create_app("production")
    assert app.config["SECRET_KEY"] != "my code"
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("PROD_DATABASE_URI")
    assert app.config["TOKEN_EXPIRE_HOURS"] == 1
    assert app.config["TOKEN_EXPIRE_MINUTES"] == 0
