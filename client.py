import requests
import json

'''
Send a POST with the total_loss values from the metrics.json file
'''

url_metric = "http://127.0.0.1:5000/board"

def send_data(data, url):
    print(f"Sending: {data} => {url}")
    headers = {'Content-type':'application/json', 'Accept':'text/plain'}

    response = requests.post(url, data=json.dumps(data), headers=headers)

def read_json(line, key):
    data = json.loads(line)

    return data[key]

with open("metrics.json", "r") as f:
    for l in f.readlines():
        loss = read_json(l, "loss_mask")
        # mask = read_json(l, "total_loss")
        send_data(["loss_mask", loss], url_metric)
        # send_data(["total_loss", mask], url_metric)

with open("metrics.json", "r") as f:
    for l in f.readlines():
        mask = read_json(l, "total_loss")
        send_data(["total_loss", mask], url_metric)
