from http import HTTPStatus

from tests.utils import register_user, login_user, create_folder, delete_folder


def test_delete_folder_success(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = delete_folder(client, access_token, 1)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_folder_does_not_exist(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    response = delete_folder(client, access_token, 1)
    assert response.status_code == HTTPStatus.NOT_FOUND
    message = f"Folder with id {1} does not exist."
    assert "message" in response.json and message in response.json["message"]
