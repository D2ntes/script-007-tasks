import requests
from Utils import to_json

response = requests.post('http://127.0.0.1:8080/create_file', data=to_json({
    'filename': '/\/.txt',
    'content': 'New file content\r\nIn two lines!',
}))
print(f'code: {response.status_code}')
print(f'body: {response.text}')
