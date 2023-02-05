from http import HTTPStatus

from flask_restx import Namespace, Resource

from flashcards.api.common.dto import nav_links_model
from flashcards.api.set.business import (
    retrieve_set_list,
    create_set,
    retrieve_set,
    update_set,
    delete_set,
)
from flashcards.api.set.dto import (
    set_pagination_model,
    set_model,
    set_user_model,
    set_pagination_reqparser,
    create_set_reqparser,
    update_set_reqparser,
)

set_ns = Namespace(name="sets", validate=True)
set_ns.models[set_pagination_model.name] = set_pagination_model
set_ns.models[nav_links_model.name] = nav_links_model
set_ns.models[set_model.name] = set_model
set_ns.models[set_user_model.name] = set_user_model


@set_ns.route("", endpoint="set_list")
@set_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@set_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@set_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class SetList(Resource):
    @set_ns.doc(security="Bearer")
    @set_ns.response(int(HTTPStatus.OK), "Retrieved set list.", set_pagination_model)
    @set_ns.expect(set_pagination_reqparser)
    def get(self):
        request_data = set_pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_set_list(page, per_page)

    @set_ns.doc(security="Bearer")
    @set_ns.response(int(HTTPStatus.OK), "Successfully created set.", set_model)
    @set_ns.marshal_with(set_model)
    @set_ns.expect(create_set_reqparser)
    def post(self):
        request_data = create_set_reqparser.parse_args()
        return create_set(request_data)


@set_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@set_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@set_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@set_ns.response(int(HTTPStatus.NOT_FOUND), "Set does not exist.")
@set_ns.route("/<set_id>", endpoint="set")
class Set(Resource):
    @set_ns.doc(security="Bearer")
    @set_ns.response(int(HTTPStatus.OK), "Retrieved set.", set_model)
    @set_ns.marshal_with(set_model)
    def get(self, set_id):
        return retrieve_set(set_id)

    @set_ns.doc(security="Bearer")
    @set_ns.response(int(HTTPStatus.OK), "Updated set.")
    @set_ns.expect(update_set_reqparser)
    def put(self, set_id):
        request_data = update_set_reqparser.parse_args()
        return update_set(set_id, request_data)

    @set_ns.doc(security="Bearer")
    @set_ns.response(int(HTTPStatus.NO_CONTENT), "Set was deleted.")
    def delete(self, set_id):
        return delete_set(set_id)
