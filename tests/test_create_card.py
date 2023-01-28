from http import HTTPStatus

from tests.utils import login_user, create_card, register_user, TEST_TERM, TEST_DEFINITION, create_folder


def test_create_card_valid_data(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = create_card(client, access_token, folder_id=1)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"Card was created successfully."
    assert "message" in response.json and response.json["message"] == success


def test_create_card_invalid_folder_id(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_card(client, access_token, folder_id=2)
    assert response.status_code == HTTPStatus.NOT_FOUND
    message = f"Folder with id {2} does not exist."
    assert "status" in response.json and response.json["status"] == "fail"
    assert "message" in response.json and message in response.json["message"]


def test_create_card_invalid_data(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = create_card(client, access_token, term='', definition='', folder_id=1)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    message = "Input payload validation failed"
    assert "message" in response.json and response.json["message"] == message
