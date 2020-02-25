import requests
import json

url = "http://127.0.0.1:5000/board"

data = {'loss':0.4}
headers = {'Content-type':'application/json', 'Accept':'text/plain'}

print(data)

response = requests.post(url, data = json.dumps(data), headers = headers)

print(response.text)