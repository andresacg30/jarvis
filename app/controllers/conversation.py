import datetime
import typing
import random

from flask import current_app

import app.controllers.user as user_controller
import app.controllers.message as message_controller

from app import db
from app.models import Conversation, Message, User


def create_conversation(
    initial_messages: list,
    received_message: str = None,
    user: User = None
) -> Conversation:
    if not user:
        user = user_controller.create_guest_user()
    conversation = Conversation(user_id=user.id)
    db.session.add(conversation)
    db.session.commit()

    messages = [
        Message(role="system", content=current_app.config['BOT_INITIAL_SETUP']),
    ]
    if received_message:
        messages.append(Message(role="user", content=received_message))
    choosen_message = random.choice(initial_messages)
    messages.append(Message(role="assistant", content=choosen_message))

    for message in messages:
        message.conversation_id = conversation.id

    db.session.add_all(messages)
    db.session.commit()

    return conversation


def chat(
    conversation: Conversation,
    message: typing.Optional[Message]
) -> Conversation:
    conversation.add_message(role="user", content=message)
    model_response = message_controller.get_model_response(messages=conversation.messages)
    conversation.add_message(role="assistant", content=model_response)
    conversation.last_updated = datetime.datetime.utcnow()
    db.session.commit()

    return conversation


def get_last_conversation(user: User) -> typing.Optional[Conversation]:
    return Conversation.query.filter_by(user_id=user.id).order_by(Conversation.id.desc()).first() or None


def finish_conversation(conversation: Conversation) -> None:
    conversation.is_finished = True
    db.session.commit()

