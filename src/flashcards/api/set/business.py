from http import HTTPStatus

from flask import jsonify
from flask_restx import marshal, abort

from flashcards import db
from flashcards.api.auth.decorators import token_required
from flashcards.api.common.business import add_nav_links
from flashcards.api.set.dto import set_pagination_model
from flashcards.models.set import Set
from flashcards.models.user import User


@token_required
def create_set(request_data):
    name = request_data["name"]
    set = Set.find_by_name(name)
    if set and get_set(set.id, create_set.public_id):
        abort_set_exist(name)
    user_public_id = create_set.public_id
    user = User.find_by_public_id(user_public_id)
    new_set = Set(**request_data)
    new_set.user_id = user.id
    db.session.add(new_set)
    db.session.commit()
    return new_set


@token_required
def retrieve_set_list(page, per_page):
    user = User.find_by_public_id(retrieve_set_list.public_id)
    pagination = Set.query.filter_by(user_id=user.id).paginate(
        page=page, per_page=per_page
    )
    response_data = marshal(pagination, set_pagination_model)
    response_data["links"] = add_nav_links(pagination, "api.set_list")
    response = jsonify(response_data)
    return response


@token_required
def retrieve_set(set_id):
    set = get_set(set_id, retrieve_set.public_id)
    if set:
        return set
    else:
        abort_set_not_exist(set_id)


@token_required
def update_set(set_id, request_data):
    set = get_set(set_id, update_set.public_id)
    if set:
        for k, v in request_data.items():
            setattr(set, k, v)
        db.session.commit()
        message = f"Set {set.name} was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    else:
        abort_set_not_exist(set_id)


@token_required
def delete_set(set_id):
    current_set = get_set(set_id, delete_set.public_id)
    if current_set:
        db.session.delete(current_set)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    else:
        abort_set_not_exist(set_id)


def get_set(set_id, user_public_id):
    user = User.find_by_public_id(user_public_id)
    set = Set.find_by_user_id(set_id, user.id)
    if set:
        return set


def abort_set_not_exist(set_id):
    error = f"Set with id {set_id} does not exist."
    abort(HTTPStatus.NOT_FOUND, error, status="fail")


def abort_set_exist(name):
    error = f"Set with name {name} already exists."
    abort(HTTPStatus.CONFLICT, error, status="fail")
