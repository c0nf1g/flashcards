from http import HTTPStatus

from flask_restx import Namespace, Resource

from flashcards.api.common.dto import nav_links_model
from flashcards.api.card.business import create_card, update_card, retrieve_card_list, retrieve_card, delete_card
from flashcards.api.card.dto import card_pagination_model, card_model, card_set_model, \
    card_sentence_model, create_card_model, create_card_reqparser, update_card_model, update_card_reqparser, \
    card_pagination_reqparser

card_ns = Namespace(name="cards", validate=True)
card_ns.models[card_pagination_model.name] = card_pagination_model
card_ns.models[nav_links_model.name] = nav_links_model
card_ns.models[card_model.name] = card_model
card_ns.models[card_set_model.name] = card_set_model
card_ns.models[card_sentence_model.name] = card_sentence_model
card_ns.models[create_card_model.name] = create_card_model
card_ns.models[update_card_model.name] = update_card_model


@card_ns.route("", endpoint="card_list")
class CardList(Resource):
    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Retrieved card list.", card_pagination_model)
    @card_ns.expect(card_pagination_reqparser)
    def get(self):
        request_data = card_pagination_reqparser.parse_args()
        set_id = request_data.get("set_id")
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_card_list(set_id, page, per_page)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Successfully created card.", card_model)
    @card_ns.marshal_with(card_model)
    @card_ns.expect(create_card_model, validate=True)
    def post(self):
        request_data = create_card_reqparser.parse_args()
        return create_card(request_data)


@card_ns.route("/<card_id>", endpoint="card")
class Card(Resource):
    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Retrieved model.", card_model)
    @card_ns.marshal_with(card_model)
    def get(self, card_id):
        return retrieve_card(card_id)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Successfully updated card.", card_model)
    @card_ns.marshal_with(card_model)
    @card_ns.expect(update_card_model, validate=True)
    def put(self, card_id):
        request_data = update_card_reqparser.parse_args()
        return update_card(card_id, request_data)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.NO_CONTENT), "Card was deleted.")
    def delete(self, card_id):
        return delete_card(card_id)
