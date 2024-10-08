import hmac
import hashlib
from pathlib import Path
from openai import OpenAI

from flask import jsonify, request, abort, current_app

import app.controllers.conversation as conversation_controller
import app.controllers.message as message_controller
import app.controllers.whatsapp as whatsapp_controller
import app.controllers.lead as lead_controller

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


@bp.route('/chat/initial', methods=['POST'])
def initial_message():
    data = request.get_json() or {}
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        abort(400, "Missing API key")
    elif api_key != current_app.config['API_KEY']:
        abort(401, "Invalid API key")
    lead = lead_controller.get_lead_by_email(data.get('email'))
    if not lead:
        lead = lead_controller.create_lead(
            name=data.get('name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            birthday=data.get('birthday'),
            have_iul=data.get('have_iul'),
            primary_goal=data.get('primary_goal'),
            state=data.get('state'),
            campaign=data.get('campaign'),
            lead_type=data.get('lead_type'),
            other_fields=data.get('other_fields')
        )
    settings = data.get('settings')
    lead_setup = data.get('lead_setup')
    conversation = conversation_controller.create_conversation(
        lead=lead, settings=settings, lead_setup=lead_setup
    )
    last_message = message_controller.get_latest_message(conversation=conversation)
    payload = {
        "lead_id": conversation.lead_id,
        "conversation_id": conversation.id,
    }
    token = security.encode_jwt_tokens(
        payload=payload,
        days_before_expiration=constants.TOKEN_DAYS_BEFORE_EXPIRATION,
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
        lead_id = token['lead_id']
    except (security.TokenError):
        abort(401, "Invalid token")
    conversation = Conversation.query.filter_by(lead_id=lead_id).first()
    if not conversation:
        abort(404, "Conversation not found")
    conversation = conversation_controller.chat(conversation, message)
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'text': last_message.content})


@bp.route('/chat/assistant', methods=["POST"])
def chat_assistant():
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
        conversation_id = token['conversation_id']
    except (security.TokenError):
        abort(401, "Invalid token")
    conversation = Conversation.query.filter_by(id=conversation_id).first()
    if not conversation:
        abort(404, "Conversation not found")
    conversation = conversation_controller.chat_assistant(conversation, message)
    last_message = message_controller.get_latest_message(conversation=conversation)
    return jsonify({'text': last_message.content})


@bp.route('/chat/assistant/notification', methods=["POST"])
def notification():
    try:
        data = request.get_json() or {}
        message = data.get('content')
        conversation = conversation_controller.get_notification_message(message)
        lead = lead_controller.get_lead_by_id(conversation.lead_id)
        last_message = message_controller.get_latest_message(conversation=conversation)
        return jsonify({'text': last_message.content, 'lead': lead.email})
    except lead_controller.LeadNotFoundError:
        abort(404, "Lead not found")


@bp.route('/chat/assistant/internal', methods=["POST"])
def internal():
    try:
        data = request.get_json() or {}
        message = data.get('content')
        response = conversation_controller.get_internal_message(message)
        return jsonify({'text': response})
    except lead_controller.LeadNotFoundError:
        abort(404, "Lead not found")


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


@bp.route("/voice", methods=["POST"])
def generate_voice_message():
    client = OpenAI()
    speech_file_path = Path(__file__).parent / "speecsd.mp3"
    voice = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="U don't recognize me? I'm jarvis, the new chick."
    )

    voice.stream_to_file(speech_file_path)
