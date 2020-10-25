import requests

url = "http://localhost:4567/todos/1"

r = requests.get(url = url)

data = r.json()

print(data)
