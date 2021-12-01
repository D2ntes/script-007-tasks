import json

import requests
from Utils import to_json

response = requests.get('http://127.0.0.1:8080/get_files')
print(f'code: {response.status_code}')
pretty_response = to_json(json.loads(response.text))
print(f'body: {pretty_response}')
