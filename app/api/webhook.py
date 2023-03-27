import hmac
import hashlib
from flask import request, abort, current_app

from app.api import bp


@bp.route('/webhooks/', methods=["GET"])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        abort(400, 'Missing X-Hub-Signature-256 header')
    payload = request.data
    secret_key = current_app.config["OPENAI_API_KEY"]
    expected_signature = 'sha256=' + hmac.new(secret_key.encode(), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        abort(400, 'Invalid signature')
    # payload is valid, process the event notification here
    return 'OK', 200


@bp.route('/webhooks/', methods=["GET"])
def verify():
    verify_token = request.args.get('hub.verify_token')

    if verify_token == "alca":
        challenge = request.args.get('hub.challenge')
        return challenge

    return 'Invalid verification token'
