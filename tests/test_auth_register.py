from http import HTTPStatus

from flashcards.models.user import User
from tests.utils import register_user, EMAIL, USERNAME, PASSWORD

EMAIL_ALREADY_EXISTS = f"User with email {EMAIL} is already registered"
USERNAME_ALREADY_EXISTS = f"User with username {USERNAME} is already registered"

BAD_REQUEST_MESSAGE = "Input payload validation failed"


def test_auth_register(client, db):
    response = register_user(client)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert (
        "message" in response.json
        and response.json["message"] == "successfully registered"
    )
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    result = User.decode_access_token(access_token)
    assert result.success
    user_dict = result.value
    user = User.find_by_public_id(user_dict["public_id"])
    assert user and user.email == EMAIL


def test_token_auth_register_email_already_registered(client, db):
    user = User(email=EMAIL, username=USERNAME, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    response = register_user(client)
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json and response.json["message"] == EMAIL_ALREADY_EXISTS
    )
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json


def test_token_auth_register_username_already_registered(client, db):
    user = User(email=f"{EMAIL}_1", username=USERNAME, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    response = register_user(client)
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json
        and response.json["message"] == USERNAME_ALREADY_EXISTS
    )
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json


def test_auth_register_invalid_email(client):
    invalid_email = "invalid email"
    response = register_user(client, email=invalid_email)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST_MESSAGE
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json
    assert "errors" in response.json
    assert "password" not in response.json["errors"]
    assert "email" in response.json["errors"]
    assert response.json["errors"]["email"] == f"{invalid_email} is not a valid email"
