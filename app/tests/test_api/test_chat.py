
def test__chat__returns_expected_message__when_has_valid_api_key(test_app, mocker, api_key):
    headers = {'X-API-KEY': api_key}
    message = {"content": "Hello!"}
    expected_message = {
        "choices": [{"message": {"text":  "Thanks for testing!"}}]
    }
    mocker.patch('openai.ChatCompletion.create', return_value=expected_message)

    response = test_app.post('/api/chat', json=message, headers=headers)

    assert response.status_code == 200
    assert response.json.get('text') == "Thanks for testing!"


def test__chat__returns_unauthorized_error__when_has_invalid_api_key(test_app, mocker):
    api_key = 'invalid_api_key'
    headers = {'X-API-KEY': api_key}
    message = {'content': 'hello'}
    mocker.patch('openai.ChatCompletion.create')

    response = test_app.post('/api/chat', json=message, headers=headers)

    assert response.status_code == 401


def test__initial_message__returns_greetings_message(test_app, mocker, api_key):
    greetings_message = {
        "choices": [{"message": {"text":  "Hello! How may asist you today?"}}]
    }

    headers = {'X-API-KEY': api_key}
    mocker.patch('openai.ChatCompletion.create', return_value=greetings_message)

    response = test_app.get('/api/chat/initial', headers=headers)

    assert response.status_code == 200
    assert 'Hello' in response.json.get('text')
