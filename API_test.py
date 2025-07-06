import requests

response = requests.get("http://randomfox.ca/floof")
print(response.status_code)
data = response.json()

fox = response.json()

print(response.json())
print(fox['image'])
