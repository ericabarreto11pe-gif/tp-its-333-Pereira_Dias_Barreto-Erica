from flask import Flask
from models import db, Groupe, Etudiant  # ✅ ici seulement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alchimie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    if not Groupe.query.filter_by(nom="ITS2").first():
        its2 = Groupe(nom="ITS2")
        db.session.add(its2)
        db.session.commit()

        e1 = Etudiant(nom="Erica", groupe=its2)
        e2 = Etudiant(nom="Farah", groupe=its2)
        e3 = Etudiant(nom="Bob", groupe=its2)
        db.session.add_all([e1, e2, e3])
        db.session.commit()

@app.route("/test")
def test():
    groupe = Groupe.query.filter_by(nom="ITS2").first()
    return {
        "groupe": groupe.nom,
        "etudiants": [e.nom for e in groupe.etudiants]
    }

if __name__ == "__main__":
    app.run(debug=True)


