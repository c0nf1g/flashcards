from http import HTTPStatus

from tests.utils import login_user, create_folder, register_user, FOLDER_NAME


def test_create_folder_valid_data(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_folder(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"Folder {FOLDER_NAME} was created successfully."
    assert "message" in response.json and response.json["message"] == success


def test_create_folder_invalid_data(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_folder(client, access_token, folder_name='', description='')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    message = "Input payload validation failed"
    assert "message" in response.json and response.json["message"] == message

