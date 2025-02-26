import requests

# URL für den POST-Request
url = "http://127.0.0.1:5000/products"

# Daten, die im Request-Body gesendet werden
data = {
    "product": "Gaggia Classic Evo",
    "price": "123"
}

# POST-Request absenden
response = requests.post(url, json=data)

# Antwort ausgeben
print("Status Code:", response.status_code)
print("Response Body:", response.json())
