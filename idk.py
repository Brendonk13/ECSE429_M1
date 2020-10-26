import requests

url = "http://localhost:4567/todos/"

data = {'id': '2', 'title': 'new title'}
r = requests.post(url = url, json = data)
print(r.status_code)
print(r.json())

if r.ok:
    data = r.json()
    print(data)
