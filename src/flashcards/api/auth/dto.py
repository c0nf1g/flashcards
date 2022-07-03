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
