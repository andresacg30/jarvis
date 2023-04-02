import app.controllers.conversation as conversation_controller


def test__create_conversation__returns_conversation_with_chat_response__when_user_is_guest(
    test_app,
    mocker
):
    with test_app.app_context():
        create_guest_user_mock = mocker.patch(
            'app.controllers.conversation.create_guest_user',
            return_value=mocker.Mock(id=1)
        )
        get_model_response_mock = mocker.patch(
            'app.controllers.conversation.get_model_response',
            return_value='Hello!'
        )

        conversation_controller.create_conversation()

        create_guest_user_mock.assert_called_once()
        get_model_response_mock.assert_called_once()


def test__create_conversation__returns_conversation_with_chat_response__when_user_is_not_guest(
    test_app,
    mocker
):
    with test_app.app_context():
        user = mocker.Mock(id=1)
        create_guest_user_mock = mocker.patch(
            'app.controllers.conversation.create_guest_user',
            return_value=mocker.Mock(id=1)
        )
        get_model_response_mock = mocker.patch(
            'app.controllers.conversation.get_model_response',
            return_value='Hello!'
        )

        conversation_controller.create_conversation(user=user)

        create_guest_user_mock.assert_not_called()
        get_model_response_mock.assert_called_once()


def test__chat__returns_conversation_with_chat_response__when_conversation_is_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        conversation = mocker.Mock()
        conversation.messages = []
        get_model_response_mock = mocker.patch(
            'app.controllers.conversation.get_model_response',
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
            'app.controllers.conversation.get_model_response',
            return_value='How are you?'
        )

        conversation_controller.chat(conversation, 'How are you?')

        get_model_response_mock.assert_called_once()
