from flask import url_for

EMAIL = "test_user@email.com"
PASSWORD = "teSt1234"
USERNAME = "test_user789"
WWW_AUTH_NO_TOKEN = 'Bearer realm="Flashcards application"'


FOLDER_NAME = "test_folder"
FOLDER_DESCRIPTION = "test_description"


TEST_TERM = "test card"
TEST_DEFINITION = "test definition"


def register_user(test_client, email=EMAIL, username=USERNAME, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&username={username}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def login_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_login"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def get_user(test_client, access_token):
    return test_client.get(
        url_for("api.auth_user"), headers={"Authorization": f"Bearer {access_token}"}
    )


def logout_user(test_client, access_token):
    return test_client.post(
        url_for("api.auth_logout"), headers={"Authorization": f"Bearer {access_token}"}
    )


def retrieve_folder_list(test_client, access_token, page=None, per_page=None):
    return test_client.get(
        url_for("api.folder_list", page=page, per_page=per_page),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def retrieve_folder(test_client, access_token, folder_id):
    return test_client.get(
        url_for("api.folder", folder_id=folder_id),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_folder(test_client, access_token, folder_name=FOLDER_NAME, description=FOLDER_DESCRIPTION):
    return test_client.post(
        url_for("api.folder_list"),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"name={folder_name}&description={description}",
        content_type="application/x-www-form-urlencoded",
    )


def update_folder(test_client, access_token, folder_id, folder_name, description):
    return test_client.put(
        url_for("api.folder", folder_id=folder_id),
        data=f"name={folder_name}&description={description}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/x-www-form-urlencoded",
    )


def delete_folder(test_client, access_token, folder_id):
    return test_client.delete(
        url_for("api.folder", folder_id=folder_id),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_card(test_client, access_token, folder_id, term=TEST_TERM, definition=TEST_DEFINITION):
    return test_client.post(
        url_for("api.card_list"),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"term={term}&definition={definition}&folder_id={folder_id}",
        content_type="application/x-www-form-urlencoded",
    )


def retrieve_card(test_client, access_token, card_id):
    return test_client.get(
        url_for("api.card", card_id=card_id),
        headers={"Authorization": f"Bearer {access_token}"},
    )
