import datetime
import typing

from flask import current_app

import app.controllers.message as message_controller
import app.controllers.lead as lead_controller

from app import db
from app.models import Conversation, Message, Lead


def create_conversation(
    lead: Lead,
    settings: str,
    message_received: str = None
) -> Conversation:

    conversation = Conversation(lead_id=lead.id)
    db.session.add(conversation)
    db.session.commit()

    lead_setup = lead_controller.get_lead_setup(lead)
    messages = [
        Message(role="system", content=settings),
    ]
    if message_received:
        messages.append(Message(role="user", content=message_received))
    else:
        messages.append(Message(role="assistant", content=lead_setup))
    model_response = message_controller.get_model_response(messages=messages)
    messages.append(Message(role="assistant", content=model_response))

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


def chat_assistant(
    conversation: Conversation,
    message: typing.Optional[Message]
) -> Conversation:
    conversation.add_message(role="system", content=message)
    model_response = message_controller.get_model_response(messages=conversation.messages)
    conversation.add_message(role="assistant", content=model_response)
    conversation.last_updated = datetime.datetime.utcnow()
    db.session.commit()

    return conversation


def get_last_conversation(lead: Lead) -> typing.Optional[Conversation]:
    return Conversation.query.filter_by(lead_id=lead.id).order_by(Conversation.id.desc()).first() or None


def finish_conversation(conversation: Conversation) -> None:
    conversation.is_finished = True
    db.session.commit()
