import requests

BASE = "http://127.0.0.1:5000/"
r = requests.delete(BASE + "Ahmedabad/Area1/Pipe3")
print(r.json())