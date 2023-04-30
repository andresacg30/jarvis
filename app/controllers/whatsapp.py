import datetime

import app.controllers.conversation as conversation_controller
import app.controllers.user as user_controller
import app.controllers.message as message_controller
from app.models.message import Message
from app.models.user import User
import app.utils.constants as constants


class DataHandlerStrategy:
    def handle_data(self, data):
        raise NotImplementedError


class MessageHandler(DataHandlerStrategy):
    def handle_data(self, data):
        message_body = data['messages'][0]['text']['body']
        sender_number = data['messages'][0]['from']
        sender_name = data['contacts'][0]['profile']['name']
        user = self.get_or_create_user(
            name=sender_name,
            sender_number=sender_number
        )
        message_to_send = self.get_message_to_send(user=user, received_message=message_body)
        
        message_controller.send_whatsapp_message(
            recipient_number=sender_number,
            message=message_to_send.content
        )

    def get_or_create_user(self, name: str, sender_number: str) -> User:
        user = user_controller.get_user_by_phone_number(phone_number=sender_number)
        if not user:
            user = user_controller.create_user(
                name=name,
                phone_number=sender_number,
                origin="whatsapp"
            )
        return user


    def get_message_to_send(self, user: User, received_message: str) -> Message:
        conversation = conversation_controller.get_last_conversation(user=user)
        if conversation and conversation.last_updated < datetime.datetime.utcnow() - datetime.timedelta(minutes=1):
            conversation_controller.finish_conversation(conversation=conversation)
        if not conversation or conversation.is_finished:
            chat = conversation_controller.create_conversation(
                initial_messages=constants.WHATSAPP_INITIAL_MESSAGES,
                received_message=received_message,
                user=user
            )
        else:
            chat = conversation_controller.chat(conversation, received_message)
        last_message = message_controller.get_latest_message(conversation=chat)
        return last_message
