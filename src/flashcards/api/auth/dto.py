from flask_restx import Model
from flask_restx.fields import String
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import email

auth_reqparser = RequestParser(bundle_errors=True)
auth_reqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
auth_reqparser.add_argument(
    name="username", type=str, location="form", required=True, nullable=False
)
auth_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)

login_reqparser = RequestParser(bundle_errors=True)
login_reqparser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
login_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)

user_model = Model(
    "User",
    {
        "email": String,
        "public_id": String,
        "registered_on": String(attribute="registered_on"),
        "token_expires_in": String,
    },
)
