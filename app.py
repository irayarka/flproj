from flask import Flask
from flask_bcrypt import Bcrypt
from waitress import serve
from bprint import api_blueprint
from errors import invalid_id, not_found, invalid_input, internal_server_error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'needs-to-be-changed'

app.register_blueprint(api_blueprint, url_prefix="/api/v1")

app.register_error_handler(400, invalid_id)
app.register_error_handler(404, not_found)
app.register_error_handler(405, invalid_input)
app.register_error_handler(500, internal_server_error)

bcrypt = Bcrypt(app)

if __name__ == "__main__":
    # app.run(debug=True, host='localhost', port=5050)
    serve(app, host='localhost', port=5050)
