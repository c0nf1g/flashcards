from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .config import get_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask('flashcards')
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app)

    return app
