import app.controllers.conversation as conversation_controller
import app.controllers.message as message_controller


def test__create_conversation__returns_conversation_with_chat_response__when_user_is_guest(
    test_app,
    mocker
):
    with test_app.app_context():
        initial_messages = [
            "test",
            "test2"
        ]
        create_guest_user_mock = mocker.patch(
            'app.controllers.user.create_guest_user',
            return_value=mocker.Mock(id=1)
        )

        response = conversation_controller.create_conversation(
            initial_messages=initial_messages
        )
        latest_message = message_controller.get_latest_message(
            conversation=response
        ).to_dict()['content']

        create_guest_user_mock.assert_called_once()
        assert latest_message in initial_messages


def test__create_conversation__returns_conversation_with_chat_response__when_user_is_not_guest(
    test_app,
    mocker
):
    with test_app.app_context():
        initial_messages = [
            "test",
            "test2"
        ]
        user = mocker.Mock(id=1)
        create_guest_user_mock = mocker.patch(
            'app.controllers.user.create_guest_user',
            return_value=mocker.Mock(id=1)
        )
        response = conversation_controller.create_conversation(user=user, initial_messages=initial_messages)
        latest_message = message_controller.get_latest_message(
            conversation=response
        ).to_dict()['content']

        create_guest_user_mock.assert_not_called()
        assert latest_message in initial_messages


def test__chat__returns_conversation_with_chat_response__when_conversation_is_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        conversation = mocker.Mock()
        conversation.messages = []
        get_model_response_mock = mocker.patch(
            'app.controllers.message.get_model_response',
            return_value='Hello!'
        )

        conversation_controller.chat(conversation, 'Hi!')

        get_model_response_mock.assert_called_once()


def test__chat__returns_conversation_with_chat_response__when_conversation_is_not_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        conversation = mocker.Mock()
        conversation.messages = [
            mocker.Mock(role='user', content='Hi!'),
            mocker.Mock(role='assistant', content='Hello!'),
        ]
        get_model_response_mock = mocker.patch(
            'app.controllers.message.get_model_response',
            return_value='How are you?'
        )

        conversation_controller.chat(conversation, 'How are you?')

        get_model_response_mock.assert_called_once()
