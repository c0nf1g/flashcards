from http import HTTPStatus

from flask import jsonify, current_app
from flask_restx import abort

from flashcards import db
from flashcards.models.user import User


def process_registration_request(email, username, password):
    if User.find_by_email(email):
        abort(
            HTTPStatus.CONFLICT,
            f"User with email {email} is already registered",
            status="fail",
        )
    if User.find_by_username(username):
        abort(
            HTTPStatus.CONFLICT,
            f"User with username {username} is already registered",
            status="fail",
        )
    new_user = User(email=email, password=password, username=username)
    db.session.add(new_user)
    db.session.commit()
    access_token = new_user.encode_access_token()
    response = jsonify(
        status="success",
        message="successfully registered",
        access_token=access_token,
        token_type="bearer",
        expires_in=_get_token_expire_time(),
    )
    response.status_code = HTTPStatus.CREATED
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds if not current_app.config["TESTING"] else 5
