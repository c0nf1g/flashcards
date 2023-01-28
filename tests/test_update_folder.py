from http import HTTPStatus

from tests.utils import register_user, login_user, create_folder, update_folder, EMAIL, retrieve_folder

NEW_FOLDER_NAME = "new_folder_name"
NEW_DESCRIPTION = "new_description"


def test_update_folder_success(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = update_folder(client, access_token, 1, NEW_FOLDER_NAME, NEW_DESCRIPTION)
    assert response.status_code == HTTPStatus.OK

    assert "status" in response.json and response.json["status"] == "success"
    message = "Folder was successfully updated"
    assert "message" in response.json and response.json["message"] == message

    response = retrieve_folder(client, access_token, 1)
    assert response.status_code == HTTPStatus.OK

    assert "name" in response.json and response.json["name"] == NEW_FOLDER_NAME
    assert "description" in response.json and response.json["description"] == NEW_DESCRIPTION
    assert "user" in response.json and "email" in response.json["user"]
    assert response.json["user"]["email"] == EMAIL


def test_update_folder_does_not_exist(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = update_folder(client, access_token, 1, NEW_FOLDER_NAME, NEW_DESCRIPTION)
    assert response.status_code == HTTPStatus.NOT_FOUND
    message = f"Folder with id {1} does not exist."
    assert "message" in response.json and message in response.json["message"]
