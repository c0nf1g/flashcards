from http import HTTPStatus

from flask_restx import Namespace, Resource

from flashcards.api.auth.dto import (
    auth_reqparser,
    login_reqparser,
    user_model,
)
from flashcards.api.auth.business import (
    process_registration_request,
    process_login_request,
    get_logged_in_user,
    process_logout_request,
)

auth_ns = Namespace(name="auth", validate=True)
auth_ns.models[user_model.name] = user_model


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


@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    @auth_ns.expect(login_reqparser)
    @auth_ns.response(int(HTTPStatus.OK), "Login succeeded.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Email or password does not match.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        request_data = login_reqparser.parse_args()
        email = request_data.get("email")
        password = request_data.get("password")
        return process_login_request(email=email, password=password)


@auth_ns.route("/user", endpoint="auth_user")
class GetUser(Resource):
    @auth_ns.doc(security="Bearer")
    @auth_ns.response(int(HTTPStatus.OK), "Token is valid.", user_model)
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    @auth_ns.marshal_with(user_model)
    def get(self):
        return get_logged_in_user()


@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    @auth_ns.doc(security="Bearer")
    @auth_ns.response(
        int(HTTPStatus.OK), "Log out succeeded, token is no longer valid.", user_model
    )
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        return process_logout_request()
