import requests
import json

# TODO: replace with your own app_id and app_key
app_id = '9d21d160'
app_key = '29230cdcdb5f0a6b6cbad0770c66a17f'

language = 'en'
word_id = 'ace'
strictMatch = 'false'

url = 'https://od-api.oxforddictionaries.com:443/api/v2/sentences/' + language + '/' + word_id.lower() + '?strictMatch=' + strictMatch

r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
