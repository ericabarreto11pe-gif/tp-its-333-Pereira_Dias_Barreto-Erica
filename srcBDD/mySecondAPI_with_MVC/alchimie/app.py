from flask import Flask, jsonify, request
from models import db, Groupe, Etudiant
import jwt, datetime
from functools import wraps
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Flask setup
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

db.init_app(app)

# Création des tables
with app.app_context():
    db.create_all()

# JWT decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token manquant"}), 401
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "admin":
        token = jwt.encode(
            {"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({"token": token})
    return jsonify({"message": "Identifiants invalides"}), 401

# Routes Groupes
@app.route("/groupes", methods=["GET"])
def get_groupes():
    groupes = Groupe.query.all()
    return jsonify([g.to_dict() for g in groupes])

@app.route("/groupes", methods=["POST"])
@token_required
def add_groupe():
    data = request.get_json()
    nom = data.get("nom")
    if Groupe.query.get(nom):
        return jsonify({"message": "Groupe déjà existant"}), 400
    groupe = Groupe(nom=nom)
    db.session.add(groupe)
    db.session.commit()
    return jsonify({"message": "Groupe créé"}), 201

# Routes Étudiants
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([e.to_dict() for e in etudiants])

@app.route("/etudiants", methods=["POST"])
@token_required
def add_etudiant():
    data = request.get_json()
    nom = data.get("nom")
    groupe_nom = data.get("groupe_nom")  # facultatif
    etudiant = Etudiant(nom=nom, groupe_nom=groupe_nom)
    db.session.add(etudiant)
    db.session.commit()
    return jsonify({"message": "Étudiant ajouté"}), 201

# Swagger UI
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "API Gestion Groupes & Étudiants"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
