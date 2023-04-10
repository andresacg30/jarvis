import pytest
import secrets

from app import create_app, db

from .fixtures import *  # noqa F401, F403


@pytest.fixture
def test_app():

    class Config:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        OPENAI_API_KEY = "test_api_key"
        API_KEY = "test"
        BOT_INITIAL_SETUP = "bot"
        BOT_INITIAL_SETUP = "This is for test purposes"
        JWT_KEY = "test"

    flask_app = create_app(Config)
    flask_app.app_context().push()
    flask_app.secret_key = secrets.token_urlsafe(32)

    db.create_all()

    yield flask_app

    db.session.remove()
    db.drop_all()


@pytest.fixture
def test_client(test_app):
    client = test_app.test_client()
    return client


@pytest.fixture
def db_session(test_app):
    with test_app.app_context():
        db.session.begin_nested()
        yield db.session
