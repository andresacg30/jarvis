import openai

from flask import jsonify, request, current_app

from app.api import bp


@bp.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json() or {}
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                current_app.config.get('BOT_INITIAL_SETUP'),
                {"role": "user", "content": data.get('content')}
            ],
            temperature=1
        )
        model_response = response['choices'][0]['message']
        return jsonify(model_response)
