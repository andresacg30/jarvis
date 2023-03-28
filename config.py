import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    BOT_INITIAL_SETUP = os.environ.get("BOT_INITIAL_SETUP")
    API_KEY = os.environ.get("API_KEY")
