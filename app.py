from flask import Flask

app = Flask(__name__)


@app.route('/')
def default_page():
    return '<h1>Starting page</h1>'


@app.route('/v1/hello-world-31')
def hello_world():
    return '<h1>Hello World 31</h1>'


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)