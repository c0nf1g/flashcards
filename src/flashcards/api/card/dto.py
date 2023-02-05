from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, List, Nested
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

from flashcards.api.common.dto import generate_pagination_model

create_card_model = Model(
    "Create card",
    {
        "word": String,
        "definition": String,
        "set_id": Integer,
        "sentences": List(String)
    }
)

create_card_reqparser = RequestParser(bundle_errors=True)
create_card_reqparser.add_argument(
    name="word", location="json", required=True, nullable=False
)
create_card_reqparser.add_argument(
    name="definition", location="json", required=True, nullable=False
)
create_card_reqparser.add_argument(
    name="set_id", type=positive, location="json", required=True, nullable=False
)
create_card_reqparser.add_argument(
    name="sentences", type=list, location='json', required=True, nullable=False
)

update_card_model = create_card_model.clone("Updated card")
update_card_model.pop("set_id")
update_card_model.update({"learned": Boolean})

update_card_reqparser = create_card_reqparser.copy()
update_card_reqparser.remove_argument("set_id")
update_card_reqparser.add_argument(
    name="learned", type=bool, location="json", required=False
)

card_pagination_reqparser = RequestParser(bundle_errors=True)
card_pagination_reqparser.add_argument(
    name="set_id", location="args", type=positive, required=True, nullable=False
)
card_pagination_reqparser.add_argument(
    name="page", location="args", type=positive, required=False, default=1
)
card_pagination_reqparser.add_argument(
    name="per_page", location="args", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10
)


card_set_model = Model(
    "Card Set",
    {
        "id": Integer,
        "name": String
    }
)

card_sentence_model = Model(
    "Card Sentence",
    {
        "id": Integer,
        "value": String
    }
)

card_model = Model(
    "Card",
    {
        "id": Integer,
        "set": Nested(card_set_model),
        "word": String,
        "definition": String,
        "learned": Boolean,
        "learned_at": String(attribute="learned_at"),
        "sentences": List(Nested(card_sentence_model))
    }
)

card_pagination_model = generate_pagination_model(card_model)
