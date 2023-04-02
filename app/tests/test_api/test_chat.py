def test__chat__returns_expected_message__when_has_valid_api_key(
    test_client,
    mocker,
    api_key,
    conversation_factory
):
    headers = {'X-API-KEY': api_key}
    user_id = "test_user_id"
    conversation = conversation_factory(user_id)
    expected_model_response = "Bot response"
    model_response = {
        "choices": [{"message": {"content": expected_model_response}}]
    }
    headers = {'X-API-KEY': api_key}
    mocker.patch('openai.ChatCompletion.create', return_value=model_response)
    user_message = "Test message"

    data = {
        'user_id': user_id,
        'content': user_message
    }
    response = test_client.post('/api/chat', json=data, headers=headers)
    first_message = list(conversation.messages)[0].content
    last_message = list(conversation.messages)[-1].content

    assert response.status_code == 200
    assert response.json['text'] == expected_model_response
    assert len(conversation.messages.all()) == 2
    assert first_message == user_message
    assert last_message == expected_model_response


def test__chat__returns_unauthorized_error__when_has_invalid_api_key(test_client, mocker):
    api_key = 'invalid_api_key'
    headers = {'X-API-KEY': api_key}
    message = {'content': 'hello'}
    mocker.patch('openai.ChatCompletion.create')

    response = test_client.post('/api/chat', json=message, headers=headers)

    assert response.status_code == 403


def test__chat__returns_forbidden__when_has_invalid_api_key(test_client, mocker):
    message = {'content': 'hello'}
    mocker.patch('openai.ChatCompletion.create')

    response = test_client.post('/api/chat', json=message)

    assert response.status_code == 401


def test__initial_message__returns_greetings_message(test_client, mocker, api_key):
    greetings_message = {
        "choices": [{"message": {"content": "Hello! How may asist you today?"}}]
    }
    headers = {'X-API-KEY': api_key}
    mocker.patch('openai.ChatCompletion.create', return_value=greetings_message)

    response = test_client.get('/api/chat/initial', headers=headers)

    assert response.status_code == 200
    assert 'Hello' in response.json['text']
