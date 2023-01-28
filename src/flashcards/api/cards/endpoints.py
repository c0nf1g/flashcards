from http import HTTPStatus

from flask_restx import Resource, Namespace

from flashcards.api.cards.business import create_card, retrieve_card_list, retrieve_card, update_card, delete_card
from flashcards.api.cards.dto import create_card_reqparser, card_model, card_folder_model, \
    card_pagination_reqparser, update_card_reqparser, card_pagination_model
from flashcards.api.common.dto import nav_links_model

card_ns = Namespace(name="card", validate=True)

card_ns.models[card_pagination_model.name] = card_pagination_model
card_ns.models[nav_links_model.name] = nav_links_model
card_ns.models[card_model.name] = card_model
card_ns.models[card_folder_model.name] = card_folder_model


@card_ns.route("", endpoint="card_list")
@card_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@card_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@card_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class CardList(Resource):
    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Retrieved card list.", card_pagination_model)
    @card_ns.expect(card_pagination_reqparser)
    def get(self):
        request_data = card_pagination_reqparser.parse_args()
        folder_id = request_data.get("folder_id")
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_card_list(folder_id, page, per_page)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Successfully created folder.")
    @card_ns.response(int(HTTPStatus.CONFLICT), "Folder already exists.")
    @card_ns.expect(create_card_reqparser)
    def post(self):
        request_data = create_card_reqparser.parse_args()
        return create_card(request_data)


@card_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@card_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@card_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@card_ns.response(int(HTTPStatus.NOT_FOUND), "Card does not exist.")
@card_ns.route("/<int:card_id>", endpoint="card")
class Card(Resource):
    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Retrieved card.", card_model)
    @card_ns.marshal_with(card_model)
    def get(self, card_id):
        return retrieve_card(card_id)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.OK), "Updated folder.")
    @card_ns.expect(update_card_reqparser)
    def put(self, card_id):
        request_data = update_card_reqparser.parse_args()
        return update_card(card_id, request_data)

    @card_ns.doc(security="Bearer")
    @card_ns.response(int(HTTPStatus.NO_CONTENT), "Card was deleted.")
    def delete(self, card_id):
        return delete_card(card_id)
