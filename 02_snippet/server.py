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

# Route 3: Nimmt POST-Daten entgegen und gibt sie zurück
@app.route('/test', methods=['POST'])
def handle_post():
    data = request.get_json()
    return jsonify({"received": data}), 201

# Route 4: HTML-Seite mit Materialize-CSS und Mock-Daten
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', users=mock_data["users"], products=mock_data["products"])

if __name__ == '__main__':
    app.run(debug=True)
