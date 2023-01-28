from http import HTTPStatus

from flask import jsonify
from flask_restx import abort, marshal

from flashcards import db
from flashcards.api.auth.decorators import token_required
from flashcards.api.cards.dto import card_pagination_model
from flashcards.api.common.business import add_nav_links
from flashcards.api.folders.business import abort_folder_response
from flashcards.models.card import Card
from flashcards.models.folder import Folder
from flashcards.models.user import User


@token_required
def create_card(request_data):
    folder_id = request_data["folder_id"]
    folder = Folder.find_by_id(folder_id)
    if not folder:
        abort_folder_response(folder_id)
    new_card = Card(**request_data)
    db.session.add(new_card)
    db.session.commit()
    response = jsonify(status="success", message=f"Card was created successfully.")
    response.status_code = HTTPStatus.CREATED
    return response


@token_required
def retrieve_card_list(folder_id, page, per_page):
    folder = Folder.find_by_id(folder_id)
    if not folder:
        error = f"Folder with id {folder_id} does not exist."
        abort(HTTPStatus.NOT_FOUND, error, status="fail")
    pagination = Card.query.filter_by(folder_id=folder_id).paginate(page=page, per_page=per_page)
    response_data = marshal(pagination, card_pagination_model)
    response_data["links"] = add_nav_links(pagination, "api.card_list")
    response = jsonify(response_data)
    return response


@token_required
def retrieve_card(card_id):
    card = _get_card(card_id, retrieve_card.public_id)
    if card:

        return card
    else:
        _abort_card_response(card_id)


@token_required
def update_card(card_id, request_data):
    card = _get_card(card_id, update_card.public_id)
    if card:
        for k, v in request_data.items():
            setattr(card, k, v)
        db.session.commit()
        message = f"'Card was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    else:
        _abort_card_response(card_id)


@token_required
def delete_card(card_id):
    card = _get_card(card_id, delete_card.public_id)
    if card:
        db.session.delete(card)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    else:
        _abort_card_response(card_id)


def _get_card(card_id, user_public_id):
    card = Card.find_by_id(card_id)
    user = User.find_by_public_id(user_public_id)
    folder = Folder.find_by_user_id(card.folder_id, user.id)
    if folder:
        return card


def _abort_card_response(card_id):
    error = f"Card with id {card_id} does not exist."
    abort(HTTPStatus.NOT_FOUND, error, status="fail")
