from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def default_page():
    return '<h1>Starting page</h1>'


@app.route('/api/v1/hello-world-31')
def hello_world():
    return '<h1>Hello World 31</h1>'


if __name__ == '__main__':
    serve(app, host='localhost', port=5000)
    # app.run(host="localhost", port=8000, debug=True)
