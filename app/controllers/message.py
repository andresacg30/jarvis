import typing

import openai

from app.models import Message, Conversation


class ModelResponseError(Exception):
    """
    Raised if JWT can not be decoded or signature is expired.
    """


def get_model_response(messages: typing.List[Message]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.to_dict() for message in messages],
        temperature=0.7,
    )
    model_response = response['choices'][0]['message']['content']
    return model_response


def get_latest_message(conversation: Conversation) -> Message:
    if not conversation.messages:
        return
    latest_message = Message.query.filter_by(
        conversation_id=conversation.id
    ).order_by(Message.created_at.desc()).first()
    if not latest_message.role == "assistant":
        raise ModelResponseError

    return latest_message
