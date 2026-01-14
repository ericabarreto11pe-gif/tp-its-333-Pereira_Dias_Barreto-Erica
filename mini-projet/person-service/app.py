from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flasgger import Swagger

app = Flask(__name__)

# ----------------- Configurations -----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'  # clé secrète JWT
app.config['SWAGGER'] = {
    "title": "Person Service API",
    "uiversion": 3
}

db = SQLAlchemy(app)
jwt = JWTManager(app)
swagger = Swagger(app)

# ----------------- Modèle Person -----------------
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Création de la base de données si elle n'existe pas
with app.app_context():
    db.create_all()

# ----------------- Endpoints -----------------

# Générer un token JWT
@app.route('/token', methods=['GET'])
def get_token():
    """
    Récupérer un token JWT
    ---
    tags:
      - Auth
    responses:
      200:
        description: JWT token
        schema:
          type: object
          properties:
            token:
              type: string
    """
    token = create_access_token(identity='client')
    return jsonify(token=token)

# Créer une personne
@app.route('/persons', methods=['POST'])
@jwt_required()
def create_person():
    """
    Crée une nouvelle personne
    ---
    tags:
      - Person
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          id: Person
          required:
            - name
          properties:
            name:
              type: string
    responses:
      200:
        description: Person created
        schema:
          id: Person
          properties:
            id:
              type: integer
            name:
              type: string
      400:
        description: Name required
    """
    data = request.json
    if 'name' not in data:
        return jsonify({"error": "Name required"}), 400
    person = Person(name=data['name'])
    db.session.add(person)
    db.session.commit()
    return jsonify({"id": person.id, "name": person.name})

# Récupérer une personne par ID
@app.route('/persons/<int:id>', methods=['GET'])
@jwt_required()
def get_person(id):
    """
    Récupère une personne par ID
    ---
    tags:
      - Person
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Person found
        schema:
          id: Person
          properties:
            id:
              type: integer
            name:
              type: string
      404:
        description: Person not found
    """
    person = Person.query.get(id)
    if person:
        return jsonify({"id": person.id, "name": person.name})
    return jsonify({"error": "Person not found"}), 404

# Supprimer une personne par ID
@app.route('/persons/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_person(id):
    """
    Supprime une personne par ID
    ---
    tags:
      - Person
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Person deleted
      404:
        description: Person not found
    """
    person = Person.query.get(id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted"})
    return jsonify({"error": "Person not found"}), 404

# Lister toutes les personnes
@app.route('/persons', methods=['GET'])
@jwt_required()
def list_persons():
    """
    Liste toutes les personnes
    ---
    tags:
      - Person
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
    responses:
      200:
        description: Liste des personnes
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
    """
    persons = Person.query.all()
    result = [{"id": p.id, "name": p.name} for p in persons]
    return jsonify(result)

# ----------------- Main -----------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)




