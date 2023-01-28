from flask_restx import Model
from flask_restx.fields import String, Integer, Nested
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

from flashcards.api.common.dto import generate_pagination_model, validate_field

create_folder_reqparser = RequestParser(bundle_errors=True)
create_folder_reqparser.add_argument(
    name="name", type=validate_field, location="form", required=True, nullable=False
)
create_folder_reqparser.add_argument(
    name="description", type=validate_field, location="form", required=True, nullable=False
)

update_folder_reqparser = create_folder_reqparser.copy()

folder_pagination_reqparser = RequestParser(bundle_errors=True)
folder_pagination_reqparser.add_argument(
    name="page", location="args", type=positive, required=False, default=1
)
folder_pagination_reqparser.add_argument(
    name="per_page", location="args", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10
)

folder_user_model = Model(
    "Folder user",
    {
        "email": String,
        "public_id": String,
    }
)

folder_model = Model(
    "Folder",
    {
        "id": Integer,
        "name": String,
        "description": String,
        "user": Nested(folder_user_model),
    },
)

folder_pagination_model = generate_pagination_model(folder_model)

