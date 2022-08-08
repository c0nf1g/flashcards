from flask import url_for

EMAIL = "test_user@email.com"
PASSWORD = "teSt1234"
USERNAME = "test_user789"
WWW_AUTH_NO_TOKEN = 'Bearer realm="Flashcards application"'


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
