import app.controllers.message as message_controller


def test__get_model_response__returns_model_response__when_messages_is_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        messages = []
        expected_model_response = {'choices': [{'message': {'content': 'Hello!'}}]}
        chat_completion_mock = mocker.patch(
            'app.controllers.message.openai.ChatCompletion.create',
            return_value=expected_model_response
        )

        response = message_controller.get_model_response(messages=messages)

        chat_completion_mock.assert_called_once()
        assert response == 'Hello!'


def test__get_model_response__returns_model_response__when_messages_is_not_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        messages = [
            mocker.Mock(role='user', content='Hi!'),
            mocker.Mock(role='assistant', content='Hello!'),
        ]
        expected_model_response = {'choices': [{'message': {'content': 'How are you?'}}]}
        chat_completion_mock = mocker.patch(
            'app.controllers.message.openai.ChatCompletion.create',
            return_value=expected_model_response
        )

        response = message_controller.get_model_response(messages=messages)

        chat_completion_mock.assert_called_once()
        assert response == 'How are you?'


def test__get_latest_message__returns_none__when_conversation_is_empty(
    test_app,
    mocker
):
    with test_app.app_context():
        conversation = mocker.Mock()
        conversation.messages = []

        response = message_controller.get_latest_message(conversation)

        assert response is None
