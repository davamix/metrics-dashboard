import requests
import json

'''
Send a POST with the total_loss values from the metrics.json file
'''

url_total = "http://127.0.0.1:5000/metrics/loss"
url_mask = "http://127.0.0.1:5000/metrics/mask"

def send_data(data, url):
    headers = {'Content-type':'application/json', 'Accept':'text/plain'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

def read_json(line, key):
    data = json.loads(line)

    return data[key]

with open("metrics.json", "r") as f:
    for l in f.readlines():
        loss = read_json(l, "total_loss")
        mask = read_json(l, "loss_mask")
        
        send_data(loss, url_total)
        send_data(mask, url_mask)