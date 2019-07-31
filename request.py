import requests
import json

#url = 'http://127.0.0.1:8080/predict'
url = 'https://gcp-hello-ml.appspot.com/predict'

data = [[0.23529412, 0.35483871, 0.525, 0.15132924, 0.08989726, 0.11666667]]
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)
