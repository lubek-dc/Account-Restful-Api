import base64
import requests
import json
username = "admin"
password = "admin"
message = username+':'+password
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
def login():
  url = "http://127.0.0.1:5000/login"

  payload = json.dumps({
    "name": username,
    "password": password
  })
  headers = {
    'Authorization': 'Basic bHViZWs6ZHVwYQ==',
    'Content-Type': 'application/json'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response
if __name__ == '__main__':
  token = login().json()['token']