from http import HTTPStatus

from tests.utils import register_user, login_user, create_folder, retrieve_folder_list

NAMES = [
    "folder1",
    "test_folder",
    "new-folder",
    "2folder",
    "folder3",
    "my_folder",
    "folder"
]

DESCRIPTIONS = [
    "folder 1 description",
    "test_folder description",
    "new-folder description",
    "2folder description",
    "folder3 description",
    "my_folder description",
    "folder description"
]


def test_retrieve_paginated_folder_list(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    for i in range(len(NAMES)):
        response = create_folder(
            client,
            access_token,
            folder_name=NAMES[i],
            description=DESCRIPTIONS[i]
        )
        assert response.status_code == HTTPStatus.CREATED

    response = retrieve_folder_list(client, access_token, page=1, per_page=5)
    assert response.status_code == HTTPStatus.OK

    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 2
    assert "items_per_page" in response.json and response.json["items_per_page"] == 5
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 5

    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "description" in item and item["description"] == DESCRIPTIONS[i]
