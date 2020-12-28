from flask import Flask
from flask_bcrypt import Bcrypt
from waitress import serve
from bprint import api_blueprint
from errors import invalid_id, not_found, invalid_input, internal_server_error, unauthorized_access
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'needs-to-be-changed'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

app.register_blueprint(api_blueprint)

app.register_error_handler(400, invalid_id)
app.register_error_handler(401, unauthorized_access)
app.register_error_handler(404, not_found)
app.register_error_handler(405, invalid_input)
app.register_error_handler(500, internal_server_error)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

if __name__ == "__main__":
    # app.run(debug=True, host='localhost', port=5050)
    serve(app, host='localhost', port=5050)
