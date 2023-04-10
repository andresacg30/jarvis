import typing

from flask import current_app

from app import db
from app.models import Conversation, Message, User
from app.controllers.user import create_guest_user
from app.controllers.message import get_model_response


def create_conversation(user: User = None) -> Conversation:
    if not user:
        user = create_guest_user()
    conversation = Conversation(user_id=user.id)
    db.session.add(conversation)
    db.session.commit()

    messages = [
        Message(role="system", content=current_app.config['BOT_INITIAL_SETUP']),
        Message(role="system", content="Please, say hi to our customer!"),
    ]
    model_response = get_model_response(messages=messages)
    messages.append(Message(role="assistant", content=model_response))

    for message in messages:
        message.conversation_id = conversation.id

    db.session.add_all(messages)
    db.session.commit()

    return conversation


def chat(
    conversation,
    message: typing.Optional[Message]
) -> Conversation:
    conversation.add_message(role="user", content=message)
    model_response = get_model_response(messages=conversation.messages)
    conversation.add_message(role="assistant", content=model_response)
    db.session.commit()

    return conversation
