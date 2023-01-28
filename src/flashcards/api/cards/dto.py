from flask_restx import Model
from flask_restx.fields import String, Boolean, Nested, Integer, List
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

from flashcards.api.common.dto import generate_pagination_model, validate_field

create_card_reqparser = RequestParser(bundle_errors=True)
create_card_reqparser.add_argument(
    name="term", type=validate_field, location="form", required=True, nullable=False
)
create_card_reqparser.add_argument(
    name="definition", type=validate_field, location="form", required=True, nullable=False
)
create_card_reqparser.add_argument(
    name="folder_id", type=positive, location="form", required=True, nullable=False
)

update_card_reqparser = create_card_reqparser.copy()
update_card_reqparser.remove_argument("folder_id")

card_pagination_reqparser = RequestParser(bundle_errors=True)
card_pagination_reqparser.add_argument(
    name="folder_id", location="args", type=positive, required=True, nullable=False
)
card_pagination_reqparser.add_argument(
    name="page", location="args", type=positive, required=False, default=1
)
card_pagination_reqparser.add_argument(
    name="per_page", location="args", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10
)

card_folder_model = Model(
    "Card Folder",
    {
        "id": Integer,
        "name": String,
    }
)

card_model = Model(
    "Card",
    {
        "id": Integer,
        "term": String,
        "definition": String,
        "learned": Boolean,
        "folder": Nested(card_folder_model),
    }
)

card_pagination_model = generate_pagination_model(card_model)
