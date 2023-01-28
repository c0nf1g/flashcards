from http import HTTPStatus

from tests.utils import register_user, login_user, create_card, create_folder, TEST_TERM, TEST_DEFINITION, retrieve_card


def test_retrieve_card_success(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = create_card(client, access_token, 1)
    assert response.status_code == HTTPStatus.CREATED

    response = retrieve_card(client, access_token, 1)
    assert response.status_code == HTTPStatus.OK

    assert "id" in response.json and response.json["id"] == 1
    assert "term" in response.json and response.json["term"] == TEST_TERM
    assert "definition" in response.json and response.json["definition"] == TEST_DEFINITION
    assert "folder" in response.json and response.json["folder"]["id"] == 1


def test_retrieve_card_does_not_exist(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = retrieve_card(client, access_token, 1)
    assert response.status_code == HTTPStatus.NOT_FOUND
    message = f"Card with id {1} does not exist."
    assert "message" in response.json and message in response.json["message"]
