from flask import Flask, request, send_from_directory
from word_count import word_count
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})


@app.route('/api/words')
def index():
    body = request.get_json()
    word_count(body['url'], body['filter'], body['uppercase'])
    return {'message': 'successfully counted words!'}


@app.route('/api/files')
def get_CSV():
    return send_from_directory('..', 'words_count.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=3333)
