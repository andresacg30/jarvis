from flask import jsonify, request, abort, current_app

from app.api import bp
from app.controllers import conversation as conversation_controller
from app.controllers import message as message_controller
from app.models import Conversation


@bp.before_request
def authenticate_request():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        abort(401)
    elif api_key != current_app.config['API_KEY']:
        abort(403)


@bp.route('/chat/initial', methods=['GET'])
def initial_message():
    conversation = conversation_controller.create_conversation()
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'user_id': conversation.user_id, 'text': last_message.content})


@bp.route('/chat', methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    message = data.get('content')
    if not user_id:
        abort(400, "Missing user")
    conversation = Conversation.query.filter_by(user_id=user_id).first()
    if not conversation:
        abort(404, "Conversation not found")
    conversation = conversation_controller.chat(conversation, message)
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'text': last_message.content})
