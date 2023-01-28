from http import HTTPStatus

from flask import jsonify
from flask_restx import marshal, abort

from flashcards import db
from flashcards.api.auth.decorators import token_required
from flashcards.api.common.business import add_nav_links
from flashcards.api.folders.dto import folder_pagination_model
from flashcards.models.folder import Folder
from flashcards.models.user import User


@token_required
def create_folder(request_data):
    name = request_data["name"]
    user_public_id = create_folder.public_id
    user = User.find_by_public_id(user_public_id)
    new_folder = Folder(**request_data)
    new_folder.user_id = user.id
    db.session.add(new_folder)
    db.session.commit()
    response = jsonify(status="success", message=f"Folder {name} was created successfully.")
    response.status_code = HTTPStatus.CREATED
    return response


@token_required
def retrieve_folder_list(page, per_page):
    user = User.find_by_public_id(retrieve_folder_list.public_id)
    pagination = Folder.query.filter_by(user_id=user.id).paginate(page=page, per_page=per_page)
    response_data = marshal(pagination, folder_pagination_model)
    response_data["links"] = add_nav_links(pagination, "api.folder_list")
    response = jsonify(response_data)
    return response


@token_required
def retrieve_folder(folder_id):
    folder = _get_folder(folder_id, retrieve_folder.public_id)
    if folder:
        return folder
    else:
        abort_folder_response(folder_id)


@token_required
def update_folder(folder_id, request_data):
    folder = _get_folder(folder_id, update_folder.public_id)
    if folder:
        for k, v in request_data.items():
            setattr(folder, k, v)
        db.session.commit()
        message = f"Folder was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    else:
        abort_folder_response(folder_id)


@token_required
def delete_folder(folder_id):
    folder = _get_folder(folder_id, delete_folder.public_id)
    if folder:
        db.session.delete(folder)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    else:
        abort_folder_response(folder_id)


def _get_folder(folder_id, user_public_id):
    user = User.find_by_public_id(user_public_id)
    return Folder.find_by_user_id(folder_id, user.id)


def abort_folder_response(folder_id):
    error = f"Folder with id {folder_id} does not exist."
    abort(HTTPStatus.NOT_FOUND, error, status="fail")
