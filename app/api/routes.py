from flask import jsonify, request, abort, current_app

from app.api import bp
from app.controllers import conversation as conversation_controller
from app.controllers import message as message_controller
from app.models import Conversation
from app.utils import constants, security


@bp.before_request
def authenticate_request():
    if request.method == "OPTIONS":
        return
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        abort(401)
    elif api_key != current_app.config['API_KEY']:
        abort(403)


@bp.route('/chat/initial', methods=['GET'])
def initial_message():
    conversation = conversation_controller.create_conversation()
    last_message = message_controller.get_latest_message(conversation=conversation)
    payload = {
        "user_id": conversation.user_id,
    }
    token = security.encode_jwt_tokens(
        payload=payload,
        days_before_expiration=constants.GUEST_USER_TOKEN_DAYS_BEFORE_EXPIRATION,
        encryption_algorithm=constants.GUEST_USER_ENCRYPTATION,
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
        user_id = security.decode_jwt_tokens(
            token=token,
            encryption_algorithm=constants.GUEST_USER_ENCRYPTATION,
        )
    except (security.TokenError):
        abort(401, "Invalid token")
    conversation = Conversation.query.filter_by(user_id=user_id).first()
    if not conversation:
        abort(404, "Conversation not found")
    conversation = conversation_controller.chat(conversation, message)
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'text': last_message.content})
