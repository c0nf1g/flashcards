import time

from flashcards.models.user import User
from tests.utils import EMAIL, USERNAME, PASSWORD


def test_user(user):
    assert user.email == EMAIL
    assert user.username == USERNAME
    assert user.check_password(PASSWORD)


def test_encode_access_token(user):
    access_token = user.encode_access_token()
    assert isinstance(access_token, str)


def test_decode_access_token_success(user):
    access_token = user.encode_access_token()
    result = User.decode_access_token(access_token)
    assert result.success
    user_dict = result.value
    assert user.public_id == user_dict["public_id"]


def test_decode_access_token_expired(user):
    access_token = user.encode_access_token()
    time.sleep(6)
    result = User.decode_access_token(access_token)
    assert not result.success
    assert result.error == "Access token expired."


def test_decode_access_token_invalid(user):
    access_token = user.encode_access_token()
    mod_access_token = access_token.replace(access_token[-1], "testing")
    result = User.decode_access_token(mod_access_token)
    assert not result.success
    assert result.error == "Invalid token."
