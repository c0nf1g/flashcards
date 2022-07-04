from http import HTTPStatus

from flask_restx import Namespace, Resource

from flashcards.api.auth.business import process_registration_request
from flashcards.api.auth.dto import auth_reqparser

auth_ns = Namespace(name="auth", validate=True)


@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    """/api/v1/auth/register"""

    @auth_ns.expect(auth_reqparser)
    @auth_ns.response(int(HTTPStatus.CREATED), "New user was successfully created.")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "User already exists.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        request_data = auth_reqparser.parse_args()
        email = request_data.get("email")
        username = request_data.get("username")
        password = request_data.get("password")
        return process_registration_request(email, username, password)
