import requests
import json

'''
Send a POST with the total_loss values from the metrics.json file
'''

url = "http://127.0.0.1:5000/metrics/loss"

def send_data(data):
    headers = {'Content-type':'application/json', 'Accept':'text/plain'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

def read_json(line, key):
    data = json.loads(line)

    send_data(data[key])

with open("metrics.json", "r") as f:
    for l in f.readlines():
        read_json(l, "total_loss")