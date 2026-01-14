from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from flasgger import Swagger
import requests, json, os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['SWAGGER'] = {
    "title": "Health Service API",
    "uiversion": 3
}

jwt = JWTManager(app)
swagger = Swagger(app)

PERSON_SERVICE_URL = "http://person-service:5001/persons/"
DATA_FILE = "data.json"

# ----------------- Fonctions utilitaires -----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def person_exists(person_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{PERSON_SERVICE_URL}{person_id}", headers=headers)
    return r.status_code == 200

# ----------------- Lire les données de santé -----------------
@app.route('/health/<int:person_id>', methods=['GET'])
@jwt_required()
def get_health(person_id):
    """
    Récupère les données de santé d'une personne
    ---
    tags:
      - Health
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: person_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Health data
      404:
        description: Person not found
    """
    token = request.headers.get("Authorization").split()[1]
    if not person_exists(person_id, token):
        return jsonify({"error": "Person not found"}), 404
    data = load_data()
    return jsonify(data.get(str(person_id), {}))

# ----------------- Créer ou mettre à jour les données -----------------
@app.route('/health/<int:person_id>', methods=['POST', 'PUT'])
@jwt_required()
def create_or_update_health(person_id):
    """
    Crée ou met à jour les données de santé
    ---
    tags:
      - Health
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: person_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: Health
          properties:
            poids:
              type: number
            taille:
              type: number
            frequence_cardiaque:
              type: number
            tension:
              type: string
    responses:
      200:
        description: Health data created/updated
      404:
        description: Person not found
    """
    token = request.headers.get("Authorization").split()[1]
    if not person_exists(person_id, token):
        return jsonify({"error": "Person not found"}), 404
    data = load_data()
    data[str(person_id)] = request.json
    save_data(data)
    return jsonify({"message": "Health data created"})

# ----------------- Supprimer les données -----------------
@app.route('/health/<int:person_id>', methods=['DELETE'])
@jwt_required()
def delete_health(person_id):
    """
    Supprime les données de santé
    ---
    tags:
      - Health
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: person_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Health data deleted
      404:
        description: Person not found
    """
    token = request.headers.get("Authorization").split()[1]
    if not person_exists(person_id, token):
        return jsonify({"error": "Person not found"}), 404
    data = load_data()
    if str(person_id) in data:
        del data[str(person_id)]
        save_data(data)
        return jsonify({"message": "Health data deleted"})
    return jsonify({"error": "Health data not found"}), 404

if __name__ == '__main__':
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            f.write("{}")
    app.run(host='0.0.0.0', port=5002)

