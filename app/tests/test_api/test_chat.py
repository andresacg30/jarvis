from flask import current_app

from app.utils import constants
from app.utils import security


def _build_jwt_token(expected_payload):
    jwt_token = security.encode_jwt_tokens(
        payload=expected_payload,
        days_before_expiration=constants.GUEST_USER_TOKEN_DAYS_BEFORE_EXPIRATION,
        secret_key=current_app.config['JWT_KEY'],
        encryption_algorithm=constants.JWT_ALGORITHM,
    )
    return jwt_token


def test__chat__returns_expected_message__when_has_valid_token(
    test_client,
    mocker,
    conversation_factory,
):
    user_id = "test_user_id"
    conversation = conversation_factory(user_id)
    expected_model_response = "Bot response"
    model_response = {
        "choices": [{"message": {"content": expected_model_response}}]
    }
    mocker.patch('openai.ChatCompletion.create', return_value=model_response)
    encoded_token = _build_jwt_token(
        expected_payload={"user_id": conversation.user_id}
    )
    response = test_client.post(
        '/api/chat',
        json={'content': 'Test message', 'token': encoded_token},
    )
    first_message = list(conversation.messages)[0].content
    last_message = list(conversation.messages)[-1].content

    assert response.status_code == 200
    assert response.json['text'] == expected_model_response
    assert len(conversation.messages.all()) == 2
    assert first_message == 'Test message'
    assert last_message == expected_model_response


def test__chat__returns_bad_request_error__when_missing_token(
    test_client,
):
    response = test_client.post(
        '/api/chat',
        json={'content': 'hello'},
    )
    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: Missing token'


def test__chat__returns_unauthorized_error__when_invalid_token(
    test_client,
):
    invalid_token = 'invalid_token'
    response = test_client.post(
        '/api/chat',
        json={'content': 'hello', 'token': invalid_token},
    )

    assert response.status_code == 401
    assert response.json['error'] == '401 Unauthorized: Invalid token'


def test__chat__returns_not_found_error__when_conversation_not_found(
    test_client,
    mocker,
):
    user_id = "test_user_id"
    expected_model_response = "Bot response"
    model_response = {
        "choices": [{"message": {"content": expected_model_response}}]
    }
    mocker.patch('openai.ChatCompletion.create', return_value=model_response)
    encoded_token = _build_jwt_token(
        expected_payload={"user_id": user_id}
    )
    response = test_client.post(
        '/api/chat',
        json={'content': 'Test message', 'token': encoded_token},
    )

    assert response.status_code == 404
    assert response.json['error'] == '404 Not Found: Conversation not found'


def test__initial_message__returns_greetings_message__if_is_authenticated_request(
        test_client,
        mocker,
        api_key
):
    greetings_message = {
        "choices": [{"message": {"content": "Hello! How may asist you today?"}}]
    }
    headers = {'X-API-KEY': api_key}
    mocker.patch('openai.ChatCompletion.create', return_value=greetings_message)

    response = test_client.get('/api/chat/initial', headers=headers)

    assert response.status_code == 200
    assert 'Hello' in response.json['text']


def test__initial_message__returns_bad_request_error__if_is_not_authenticated_request(
        test_client,
):
    response = test_client.get('/api/chat/initial')

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: Missing API key'


def test__initial_message__returns_unauthorized_error__if_is_invalid_api_key(
        test_client
):
    headers = {'X-API-KEY': 'invalid'}
    response = test_client.get('/api/chat/initial', headers=headers)

    assert response.status_code == 401
    assert response.json['error'] == '401 Unauthorized: Invalid API key'


def test__verify_whatsapp_request__returns_challange__when_valid_request(
        test_client
):
    challenge = 'test_challenge'
    token = 'test'

    response = test_client.get(
        f'/api/chat/whatsapp?hub.verify_token={token}&hub.challenge={challenge}'
    )

    assert response.status_code == 200
    assert response.text == challenge


def test__verify_whatsapp_request__returns_bad_request_error__when_invalid_token(
        test_client
):
    response = test_client.get('/api/chat/whatsapp')

    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: Invalid token'
