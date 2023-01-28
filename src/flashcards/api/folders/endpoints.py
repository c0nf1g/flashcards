from http import HTTPStatus

from flask_restx import Resource, Namespace

from flashcards.api.common.dto import nav_links_model
from flashcards.api.folders.business import create_folder, retrieve_folder_list, retrieve_folder, delete_folder, \
    update_folder
from flashcards.api.folders.dto import create_folder_reqparser, folder_pagination_reqparser, folder_pagination_model, \
    folder_model, folder_user_model, update_folder_reqparser

folder_ns = Namespace(name="folder", validate=True)
folder_ns.models[folder_pagination_model.name] = folder_pagination_model
folder_ns.models[nav_links_model.name] = nav_links_model
folder_ns.models[folder_model.name] = folder_model
folder_ns.models[folder_user_model.name] = folder_user_model


@folder_ns.route("", endpoint="folder_list")
@folder_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@folder_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@folder_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class FolderList(Resource):
    @folder_ns.doc(security="Bearer")
    @folder_ns.response(int(HTTPStatus.OK), "Retrieved folder list.", folder_pagination_model)
    @folder_ns.expect(folder_pagination_reqparser)
    def get(self):
        request_data = folder_pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_folder_list(page, per_page)

    @folder_ns.doc(security="Bearer")
    @folder_ns.response(int(HTTPStatus.OK), "Successfully created folder.")
    @folder_ns.expect(create_folder_reqparser)
    def post(self):
        request_data = create_folder_reqparser.parse_args()
        return create_folder(request_data)


@folder_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@folder_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@folder_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@folder_ns.response(int(HTTPStatus.NOT_FOUND), "Folder does not exist.")
@folder_ns.route("/<folder_id>", endpoint="folder")
class Folder(Resource):
    @folder_ns.doc(security="Bearer")
    @folder_ns.response(int(HTTPStatus.OK), "Retrieved folder.", folder_model)
    @folder_ns.marshal_with(folder_model)
    def get(self, folder_id):
        return retrieve_folder(folder_id)

    @folder_ns.doc(security="Bearer")
    @folder_ns.response(int(HTTPStatus.OK), "Updated folder.")
    @folder_ns.expect(update_folder_reqparser)
    def put(self, folder_id):
        request_data = update_folder_reqparser.parse_args()
        return update_folder(folder_id, request_data)

    @folder_ns.doc(security="Bearer")
    @folder_ns.response(int(HTTPStatus.NO_CONTENT), "Folder was deleted.")
    def delete(self, folder_id):
        return delete_folder(folder_id)
