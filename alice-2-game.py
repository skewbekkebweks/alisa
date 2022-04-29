import json
import logging
import os

import requests
import waitress
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    text = req['request']['command'].lower()
    if 'переведи слово' in text:
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

        querystring = {"langpair": 'ru|en', "q": text.replace('переведи слово', ''), "mt": "1",
                       "onlyprivate": "0", "de": "a@b.c"}

        headers = {
            "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com",
            "X-RapidAPI-Key": "a00beb8a82msh3fae25f95213675p1ec1fejsndcdfd1aa707b"
        }

        response = requests.get(url, headers=headers, params=querystring).json()

        res['response']['text'] = response['responseData']['translatedText']
    else:
        res['response']['text'] = 'У меня есть только команда "Переведи слово <слово>"'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    waitress.serve(app, host='0.0.0.0', port=port)
