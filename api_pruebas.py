import requests
import json

url = "http://127.0.0.1:5000/login"

payload = json.dumps({
  "corr": "pruebastresil.com",
  "pas": "pruebas"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
