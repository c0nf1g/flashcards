from http import HTTPStatus

from flask import jsonify
from flask_restx import abort, marshal

from flashcards.api.common.decorators import token_required
from flashcards.api.card.dto import card_pagination_model
from flashcards.api.common.business import add_nav_links
from flashcards.api.set.business import get_set, abort_set_not_exist
from flashcards import db

from flashcards.models import Card, Sentence
from flashcards.utils.datetime_util import utc_now


@token_required
def create_card(request_data):
    set_id = request_data["set_id"]
    if not get_set(set_id, create_card.public_id):
        abort_set_not_exist(set_id)
    sentences = request_data.pop("sentences")
    new_card = Card(**request_data)
    db.session.add(new_card)
    db.session.commit()
    for s in sentences:
        sentence = Sentence(value=s, card_id=new_card.id)
        db.session.add(sentence)
        db.session.commit()
    return new_card


@token_required
def retrieve_card_list(set_id, page, per_page):
    if not get_set(set_id, retrieve_card_list.public_id):
        error = f"Set with id {set_id} does not exist."
        abort(HTTPStatus.NOT_FOUND, error, status="fail")
    pagination = Card.query.filter_by(set_id=set_id).paginate(
        page=page, per_page=per_page
    )
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
        abort_card_not_exist(card_id)


@token_required
def update_card(card_id, request_data):
    request_data = check_request_data(request_data)
    card = _get_card(card_id, update_card.public_id)
    sentences = []
    if request_data.get("sentences"):
        sentences = request_data.pop("sentences")
    if card:
        for key, value in request_data.items():
            setattr(card, key, value)
            check_learned(card, key, value)
        update_sentences(card, sentences)
        db.session.commit()
        return card
    else:
        abort_card_not_exist(card_id)


@token_required
def delete_card(card_id):
    card = _get_card(card_id, delete_card.public_id)
    if card:
        db.session.delete(card)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT
    else:
        abort_card_not_exist(card_id)


def check_request_data(request_data):
    new_request_data = {}
    for key, value in request_data.items():
        if value is not None:
            new_request_data[key] = request_data[key]
    return new_request_data


def check_learned(card, key, value):
    if key == "learned" and value:
        setattr(card, "learned_at", utc_now())
    elif key == "learned" and not value:
        setattr(card, "learned_at", None)


def update_sentences(card, sentences):
    if sentences:
        for s in card.sentences:
            db.session.delete(s)
        for s in sentences:
            sentence = Sentence(value=s, card_id=card.id)
            db.session.add(sentence)


def _get_card(card_id, user_public_id):
    card = Card.find_by_id(card_id)
    if card:
        set = get_set(card.set_id, user_public_id)
        if set:
            return card


def abort_card_not_exist(card_id):
    error = f"Card with id {card_id} does not exist."
    abort(HTTPStatus.NOT_FOUND, error, status="fail")
