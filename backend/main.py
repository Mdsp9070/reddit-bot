import random
import pathlib
import os
from flask import Flask, request, send_file, make_response
from word_count import word_count
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})


@app.route('/api/words', methods=['POST'])
def index():
    body = request.get_json()
    code = word_count(body['url'], body['filter'], body['uppercase'])

    if code > 0:
        return {'error': 'subreddit link, not submission!'}, 400

    return {'message': 'successfully counted words!'}


@app.route('/api/files')
def get_CSV():
    crypto = random.getrandbits(32)
    res = make_response(send_file('./csv/words_count.csv', as_attachment=True))
    res.headers['Cache-Control'] = 'no-cache'
    res.headers['Cache-Control'] = 'max-age=0'
    return res


if __name__ == '__main__':
    port = 3333 or os.getenv("PORT")
    app.run(debug=False, port=port, host='0.0.0.0')
