from flask import Blueprint
from flask_restx import Api

from flashcards.api.auth.endpoints import auth_ns
from flashcards.api.cards.endpoints import card_ns
from flashcards.api.folders.endpoints import folder_ns

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_blueprint,
    version="1.0",
    title="Flashcards API",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(folder_ns, path="/folder")
api.add_namespace(card_ns, path="/card")
