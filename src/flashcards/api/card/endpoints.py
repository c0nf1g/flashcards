from http import HTTPStatus

from flask_restx import Namespace, Resource

card_ns = Namespace(name="cards", validate=True)


@card_ns.route("", endpoint="card_list")
class CardList(Resource):
    def get(self):
        pass

    def post(self):
        pass


@card_ns.route("/<name>", endpoint="card")
class Card(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
