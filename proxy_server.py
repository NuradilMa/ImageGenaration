from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests

app = Flask(__name__)

# Установите лимитер
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "20 per hour"]
)

API_KEY = 'sk-proj-5Qsl6XAKAkDrhVMdC0AXT3BlbkFJ3ZZl4BujyvxsdReomILy'


@app.route('/chat', methods=['POST'])
@limiter.limit("5 per minute")
def chat():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}]
        }
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from OpenAI"}), response.status_code

    response_json = response.json()
    return jsonify({
        'response': response_json['choices'][0]['message']['content'].strip()
    })


if __name__ == '__main__':
    app.run(debug=True)
