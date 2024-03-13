import google.cloud.logging
import openai

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


client = google.cloud.logging.Client()
client.setup_logging()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    if not app.testing:
        openai.api_key = app.config['OPENAI_API_KEY']

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models  # noqa:E402
