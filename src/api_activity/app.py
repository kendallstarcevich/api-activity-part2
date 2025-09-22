import os
from pyclbr import Class

from flask import Flask, jsonify, request, g
from flask_restful import Api, Resource, reqparse
from flask_talisman import Talisman
from api_activity._constants import PROJECT_ROOT
from api_activity.db import Database
from flask_bcrypt import Bcrypt


_KEYFILE_PATH = os.path.join(PROJECT_ROOT, "MyKey.pem")
_CERTIFICATE_PATH = os.path.join(PROJECT_ROOT, "MyCertificate.crt")


# Create the "hello" resource
class Hello(Resource):
    """A simple resource that for returning a hello message."""

    # Get is a special method for a resource.
    def get(self):
        return jsonify({"message": "Hello World!"})


class Square(Resource):
    """A simple resource that calculates the area of a square."""

    def get(self, num):
        return jsonify({"Shape": __class__.__name__, "Area": num * num})


class Echo(Resource):
    """A simple resource that echoes the arguments passed to it."""

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("arg1", type=str, location="args")
        parser.add_argument("arg2", type=str, location="args")

        arguments = parser.parse_args()

        # Return the arguments as JSON
        return jsonify(arguments)

class Register(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="Username cannot be blank")
        parser.add_argument("password", type=str, required=True, help="Password cannot be blank")
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        # Hash the password before storing it
        hashed_pwd = Bcrypt().generate_password_hash(password).decode('utf-8')
        db = get_db()
        if db.add_user(username, hashed_pwd):
            return jsonify({"message": f"User {username} registered successfully"})
        else:
            return jsonify({"message": f"User {username} already exists"}), 409


def instantiate_app() -> Flask:
    """Instantiate a new flask app"""
    # Create the flask app
    app = Flask(__name__)
    _KEYFILE_PATH = os.path.join(PROJECT_ROOT, "MyKey.pem")
    _CERTIFICATE_PATH = os.path.join(PROJECT_ROOT, "MyCertificate.crt")
    return app


def initialize_api(app: Flask) -> Api:
    """Initialize the api for the app and add resources to it"""

    # Create the API object
    api = Api(app)

    # Add the resources we want
    api.add_resource(Hello, "/")
    api.add_resource(Square, "/square/<int:num>")
    api.add_resource(Echo, "/echo")
    api.add_resource(Register, "/register")
    return api


def create_and_serve(with_ssl: bool = True):
    """Construct the app together with its api and then serves it"""
    app = instantiate_app()
    ssl_context = None if not with_ssl else (_CERTIFICATE_PATH, _KEYFILE_PATH)
    initialize_api(app)
    app.run(ssl_context=ssl_context)


def run(app, debug=True):
    """Run the app"""


if __name__ == "__main__":
    run(create_and_serve())
