import datetime
import typing


import app.controllers.lead as lead_controller
import app.controllers.message as message_controller

from app import db
from app.models import Conversation, Message, Lead


def create_conversation(
    lead: Lead,
    settings: str,
    lead_setup: str,
    message_received: str = None
) -> Conversation:

    conversation = Conversation(lead_id=lead.id)
    db.session.add(conversation)
    db.session.commit()

    messages = [
        Message(role="system", content=settings)
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


def get_notification_message(message: str) -> str:
    lead = lead_controller.find_lead_by_message(message)
    last_conversation = get_last_conversation(lead=lead)
    reminder_message = f"This is a reminder message I get from this user Insurance's application status. Create a follow up message \
        with this reminder: {message}. Don't say anything about message and data rates, or don't tell them to send STOP. Send the link \
            that is in the reminder message for payment portal ONLY if the client is missing to pay. If not, send them the booking link. We have to make \
                them continue their application, so use anything that you see in that reminder message that can work."
    last_conversation.add_message(role="system", content=reminder_message)
    notifcation_message = message_controller.get_model_response(messages=last_conversation.messages)
    last_conversation.add_message(role="assistant", content=notifcation_message)
    db.session.commit()

    return last_conversation


def get_last_conversation(lead: Lead) -> typing.Optional[Conversation]:
    return Conversation.query.filter_by(lead_id=lead.id).order_by(Conversation.id.desc()).first() or None


def finish_conversation(conversation: Conversation) -> None:
    conversation.is_finished = True
    db.session.commit()
