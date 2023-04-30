import hmac
import hashlib

from flask import Request, jsonify, request, abort, current_app

import app.controllers.conversation as conversation_controller
import app.controllers.message as message_controller
import app.controllers.whatsapp as whatsapp_controller

from app.api import bp
from app.models import Conversation
from app.utils import constants, security


data_handlers = {
    'messages': whatsapp_controller.MessageHandler(),
}


@bp.errorhandler(400)
def handle_bad_request_error(e):
    return jsonify(error=str(e)), 400


@bp.errorhandler(401)
def handle_unauthorized_error(e):
    return jsonify(error=str(e)), 401


@bp.errorhandler(404)
def handle_not_found_error(e):
    return jsonify(error=str(e)), 404


def _validate_payload_signature(request):
    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.get_data()
    mac = hmac.new(current_app.config['META_APP_SECRET'].encode(), msg=payload, digestmod=hashlib.sha256)
    expected_signature = f"sha256={mac.hexdigest()}"

    if signature != expected_signature:
        abort(401)


@bp.route('/chat/initial', methods=['GET'])
def initial_message():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        abort(400, "Missing API key")
    elif api_key != current_app.config['API_KEY']:
        abort(401, "Invalid API key")
    conversation = conversation_controller.create_conversation(
        initial_messages=constants.WEB_INITIAL_MESSAGES
    )
    last_message = message_controller.get_latest_message(conversation=conversation)
    payload = {
        "user_id": conversation.user_id,
        "conversation_id": conversation.id,
    }
    token = security.encode_jwt_tokens(
        payload=payload,
        days_before_expiration=constants.GUEST_USER_TOKEN_DAYS_BEFORE_EXPIRATION,
        secret_key=current_app.config['JWT_KEY'],
        encryption_algorithm=constants.JWT_ALGORITHM
    )
    response = jsonify({'token': token, 'text': last_message.content})
    return response


@bp.route('/chat', methods=["POST"])
def chat():
    data = request.get_json() or {}
    token = data.get('token')
    message = data.get('content')
    if not token:
        abort(400, "Missing token")
    try:
        token = security.decode_jwt_tokens(
            token=token,
            secret_key=current_app.config['JWT_KEY'],
            encryption_algorithm=constants.JWT_ALGORITHM
        )
        user_id = token['user_id']
    except (security.TokenError):
        abort(401, "Invalid token")
    conversation = Conversation.query.filter_by(user_id=user_id).first()
    if not conversation:
        abort(404, "Conversation not found")
    conversation = conversation_controller.chat(conversation, message)
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'text': last_message.content})


@bp.route('/chat/whatsapp', methods=["GET"])
def verify_whatsapp_request():
    challenge = request.args.get('hub.challenge')
    token = request.args.get('hub.verify_token')
    
    if token == current_app.config['META_VERIFY_TOKEN']:
        return challenge
    
    abort(400, "Invalid token")


@bp.route('/chat/whatsapp', methods=["POST"])
def handle_whatsapp_conversation():
    _validate_payload_signature(request)
    data = request.get_json()
    value = data['entry'][0]['changes'][0]['value']
    data_type = None
    if 'messages' in value:
        data_type = 'messages'
    handler = data_handlers.get(data_type)
    if handler:
        handler.handle_data(data=value)
    return 'OK', 200
