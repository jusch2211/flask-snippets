from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Beispiel-Daten
mock_data = {
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ],
    "products": [
        {"id": 101, "name": "Laptop", "price": 1200.99},
        {"id": 102, "name": "Smartphone", "price": 799.49},
    ]
}

# Route 1: Gibt die Liste der Benutzer zurück
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(mock_data["users"])

# Route 2: Gibt die Liste der Produkte zurück
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(mock_data["products"])

# Nimmt Produktdaten an über einen POST-Request
@app.route('/products', methods=['POST'])
def handle_post_script():
    data = request.get_json()
    return jsonify({"received": data}), 201

@app.route('/addproducts', methods=['POST'])
def handle_post():
    # Extrahieren Sie die Daten aus dem form-Objekt
    name = request.form.get('name')
    price = request.form.get('price')
    
    data = {"name": name, "price": price}
    return jsonify({"received": data}), 201

# Nimmt Produktdaten an über einen POST-Request
@app.route('/dateneingabe', methods=['GET'])
def dateneingabe():
    return render_template('dateneingabe.html')

if __name__ == '__main__':
    app.run(debug=True)
