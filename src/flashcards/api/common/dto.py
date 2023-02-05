import re

from flask_restx import Model
from flask_restx.fields import String, Integer, Nested, Boolean, List

nav_links_model = Model(
    "Nav links",
    {
        "self": String,
        "prev": String,
        "next": String,
        "first": String,
        "last": String,
    },
)


def generate_pagination_model(model):
    return Model(
        f"{model.name} Pagination",
        {
            "links": Nested(nav_links_model),
            "has_prev": Boolean,
            "has_next": Boolean,
            "page": Integer,
            "total_pages": Integer(attribute="pages"),
            "items_per_page": Integer(attribute="per_page"),
            "total_items": Integer(attribute="total"),
            "items": List(Nested(model)),
        },
    )


def validate_field(field):
    if not re.compile(r"^[\w-]+[\S\s]+[\S]+").match(field):
        raise ValueError(
            f"'{field}' contains one or more invalid characters. Name name must "
            "contain only letters, numbers, hyphen and underscore characters."
        )
    return field
