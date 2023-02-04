from http import HTTPStatus

import requests
from flask import jsonify
from flask_restx import Namespace, Resource

sentence_ns = Namespace(name="sentence", validate=True)


@sentence_ns.route("/<word>", endpoint="word")
class CardList(Resource):
    @sentence_ns.doc(security="Bearer")
    @sentence_ns.response(int(HTTPStatus.OK), "Retrieved word sentences")
    def get(self, word):
        app_id = '9d21d160'
        app_key = '29230cdcdb5f0a6b6cbad0770c66a17f'
        language = 'en'
        word_id = 'ace'
        strictMatch = 'false'
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/sentences/' + language + '/' + word_id.lower() \
              + '?strictMatch=' + strictMatch
        response = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        return jsonify(response.json())
