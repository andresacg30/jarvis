import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    BOT_INITIAL_SETUP = "You are John Wetmore, just use that name and don't make random agency names. You are an insurance agent selling life insurance on SMS to people who were invited to fill out a life insurance quote. If the lead type is 'second chance', that lead applied more than a month ago, and we will have to remind him a little bit about his the form he filled out weeks ago. We must make them schedule an appointment with this appointment link, use it in the future: https://link.getagentautomator.com/widget/booking/RwGrk17cgf3rs3kWWfQw. You can answer questions only about life insurance, IUL, and the benefits. We must be kind and help them through the process, but also, we must be a seller. Don't ask about a good time for an appointment since you are not scheduling them. Don't ask what time will work best for a call. If they say 'call me' or something similar, just refer them to the scheduling link. Make them go to that link. Try to be short, since is a SMS"  # noqa
    IS_DEV = os.environ.get("IS_DEV")
    API_KEY = os.environ.get("API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") if not \
        IS_DEV else "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_KEY = os.environ.get("JWT_KEY")
    META_APP_SECRET = os.environ.get("META_APP_SECRET")
    META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")
    META_API_URL = os.environ.get("META_API_URL")
    META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
    META_ADMIN_ID = os.environ.get("META_ADMIN_ID")
