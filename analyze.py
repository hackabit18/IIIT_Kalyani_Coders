import requests
import json
from pprint import pprint

with open("news.json", "r") as f:
    data = json.load(f)

for article in data["articles"]:
    

'''
r = requests.post("http://localhost:8080/fakebox/check", data={
    "url" : u,
    "title": t,
	"content": c
})
print(r.text)
'''