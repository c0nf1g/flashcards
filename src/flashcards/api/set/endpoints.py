from http import HTTPStatus

from flask_restx import Namespace, Resource

set_ns = Namespace(name="sets", validate=True)


@set_ns.route("", endpoint="set_list")
class SetList(Resource):
    def get(self):
        pass

    def post(self):
        pass


@set_ns.route("/<name>", endpoint="set")
class Set(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
