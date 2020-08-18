from flask import Flask, request, send_from_directory
from word_count import word_count

app = Flask(__name__)


@app.route('/words')
def index():
    body = request.get_json()
    la = word_count(body['url'])
    return {'hello': la}


@app.route('/files')
def get_CSV():
    return send_from_directory('..', 'words_count.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=3333)
