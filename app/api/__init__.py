from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import chat, webhook  # noqa:E402, F401
