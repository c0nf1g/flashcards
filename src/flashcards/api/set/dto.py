from flask_restx import Model
from flask_restx.fields import String, Integer, Nested
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

from flashcards.api.common.dto import generate_pagination_model, validate_field

create_set_reqparser = RequestParser(bundle_errors=True)
create_set_reqparser.add_argument(
    name="name", type=validate_field, location="json", required=True, nullable=False
)

update_set_reqparser = create_set_reqparser.copy()

set_pagination_reqparser = RequestParser(bundle_errors=True)
set_pagination_reqparser.add_argument(
    name="page", location="args", type=positive, required=False, default=1
)
set_pagination_reqparser.add_argument(
    name="per_page", location="args", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10
)

set_user_model = Model(
    "Set User",
    {
        "email": String,
        "public_id": String,
    }
)

set_model = Model(
    "Set",
    {
        "id": Integer,
        "name": String,
        "user": Nested(set_user_model),
    },
)

set_pagination_model = generate_pagination_model(set_model)

