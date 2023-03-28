import openai

from flask import jsonify, request, current_app, abort

from app.api import bp


@bp.before_request
def authenticate_request():
    app_api_key = current_app.config['API_KEY']
    if request.path.startswith('/api/chat'):
        api_key = request.headers.get('X-API-KEY')
        if api_key != app_api_key:
            abort(401)


@bp.route('/chat/initial', methods=['GET'])
def initial_message():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": current_app.config['BOT_INITIAL_SETUP']},
            {"role": "system", "content": "Please, say hi to our customer!"},
        ],
        temperature=1
    )
    model_response = response['choices'][0]['message']
    return jsonify(model_response)


@bp.route('/chat', methods=["POST"])
def chat():
    data = request.get_json() or {}
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": current_app.config['BOT_INITIAL_SETUP']},
            {"role": "user", "content": data.get('content')}
        ],
        temperature=1
    )
    model_response = response['choices'][0]['message']
    return jsonify(model_response)
