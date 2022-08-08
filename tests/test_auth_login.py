from http import HTTPStatus

from flashcards.models.user import User
from tests.utils import register_user, login_user, EMAIL

SUCCESS = "successfully logged in"
UNAUTHORISED = "Email or password is not correct"


def test_login(client, db):
    register_user(client)
    response = login_user(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    result = User.decode_access_token(access_token)
    assert result.success
    user_dict = result.value
    user = User.find_by_public_id(user_dict["public_id"])
    assert user and user.email == EMAIL


def test_login_email_does_not_exist(client, db):
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == UNAUTHORISED
    assert "access_token" not in response.json
