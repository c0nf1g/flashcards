import json
import os
from http import HTTPStatus

import requests
from flask import jsonify
from flask_restx import Namespace, Resource

sentence_ns = Namespace(name="sentence", validate=True)


@sentence_ns.route("/<word_id>", endpoint="word")
class CardList(Resource):
    @sentence_ns.doc(security="Bearer")
    @sentence_ns.response(int(HTTPStatus.OK), "Retrieved word sentences")
    def get(self, word_id):
        app_id = os.getenv('APP_ID', None)
        app_key = os.getenv('APP_KEY', None)
        language = 'en'
        strictMatch = 'false'
        url = 'https://od-api.oxforddictionaries.com:443/api/v2/sentences/' + language + '/' + word_id.lower() \
              + '?strictMatch=' + strictMatch
        response = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        sentences_description = response.json()["results"][0]["lexicalEntries"][0]["sentences"]
        sentences = []
        for desc in sentences_description:
            sentences.append(desc["text"])
        return jsonify(sentences)
