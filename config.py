import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    BOT_INITIAL_SETUP = os.environ.get("BOT_INITIAL_SETUP")
    IS_DEV = os.environ.get('IS_DEV')
    API_KEY = os.environ.get("API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') if not \
        IS_DEV else 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
