from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Groupe(db.Model):
    __tablename__ = "groupe"
    nom = db.Column(db.String(50), primary_key=True)

    etudiants = db.relationship("Etudiant", backref="groupe", lazy=True)

    def __repr__(self):
        return f"<Groupe {self.nom}>"

    def to_dict(self):
        return {
            "nom": self.nom,
            "etudiants": [e.nom for e in self.etudiants]
        }

class Etudiant(db.Model):
    __tablename__ = "etudiant"
    nom = db.Column(db.String(50), primary_key=True)
    groupe_nom = db.Column(db.String(50), db.ForeignKey("groupe.nom"))

    def __repr__(self):
        return f"<Etudiant {self.nom}>"

    def to_dict(self):
        return {
            "nom": self.nom,
            "groupe": self.groupe.nom if self.groupe else None
        }




