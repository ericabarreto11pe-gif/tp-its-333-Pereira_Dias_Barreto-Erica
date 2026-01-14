from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps

# -----------------------
# Flask & DB setup
# -----------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

db = SQLAlchemy(app)

# -----------------------
# Models
# -----------------------
class Groupe(db.Model):
    nom = db.Column(db.String(50), primary_key=True)
    etudiants = db.relationship("Etudiant", backref="groupe", lazy=True)

    def to_dict(self):
        return {"nom": self.nom, "etudiants": [e.nom for e in self.etudiants]}

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    groupe_nom = db.Column(db.String(50), db.ForeignKey("groupe.nom"), nullable=True)

    def to_dict(self):
        return {"nom": self.nom, "groupe_nom": self.groupe_nom}

# -----------------------
# Create tables
# -----------------------
with app.app_context():
    db.create_all()

# -----------------------
# JWT decorator
# -----------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token manquant"}), 401
        token = auth_header.split(" ")[1]
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

# -----------------------
# Login route
# -----------------------
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

# -----------------------
# Groupes routes
# -----------------------
@app.route("/groupes", methods=["GET"])
def get_groupes():
    groupes = Groupe.query.all()
    return jsonify([g.to_dict() for g in groupes])

@app.route("/groupes", methods=["POST"])
@token_required
def add_groupe():
    data = request.get_json()
    nom = data.get("nom")
    if Groupe.query.filter_by(nom=nom).first():
        return jsonify({"message": "Groupe déjà existant"}), 400
    groupe = Groupe(nom=nom)
    db.session.add(groupe)
    db.session.commit()
    return jsonify({"message": "Groupe créé"}), 201

# -----------------------
# Etudiants routes
# -----------------------
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([e.to_dict() for e in etudiants])

@app.route("/etudiants", methods=["POST"])
@token_required
def add_etudiant():
    data = request.get_json()
    nom = data.get("nom")
    groupe_nom = data.get("groupe_nom")

    # Vérifie que le groupe existe si fourni
    if groupe_nom:
        groupe = Groupe.query.filter_by(nom=groupe_nom).first()
        if not groupe:
            return jsonify({"message": "Groupe non trouvé"}), 404

    etudiant = Etudiant(nom=nom, groupe_nom=groupe_nom)
    db.session.add(etudiant)
    db.session.commit()
    return jsonify({"message": "Étudiant ajouté"}), 201

# -----------------------
# Run app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)

