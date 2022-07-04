from flask import Blueprint
from flask_restx import Api

from flashcards.api.auth.endpoints import auth_ns

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
