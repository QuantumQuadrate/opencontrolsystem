import requests
import json

url = 'http://10.128.226.224/api'


def request(text):
	data = {"data":text}
	r = requests.post(url, data)
	return r.text 

def get(payload):
	r = requests.get(url, params=payload)
	



payload = {'request': 'cards'}

print(get(payload))