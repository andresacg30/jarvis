import typing
import random

from flask import current_app

import app.controllers.user as user_controller
import app.controllers.message as message_controller

from app import db
from app.models import Conversation, Message, User


def create_conversation(user: User = None) -> Conversation:
    if not user:
        user = user_controller.create_guest_user()
    conversation = Conversation(user_id=user.id)
    db.session.add(conversation)
    db.session.commit()

    initial_messages = [
        "Hello! How can I assist you with ALCA's AI solutions today?",
        "Hello! How may I assist you with our AI solutions for business?",
        "Hello! Welcome to ALCA, how can I assist you today?",
    ]
    messages = [
        Message(role="system", content=current_app.config['BOT_INITIAL_SETUP']),
    ]
    choosen_message = random.choice(initial_messages)
    messages.append(Message(role="assistant", content=choosen_message))

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
    model_response = message_controller.get_model_response(messages=conversation.messages)
    conversation.add_message(role="assistant", content=model_response)
    db.session.commit()

    return conversation
