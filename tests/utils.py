from flask import url_for

EMAIL = "test_user@email.com"
PASSWORD = "teSt1234"
USERNAME = "test_user789"


def register_user(test_client, email=EMAIL, username=USERNAME, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&username={username}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )
