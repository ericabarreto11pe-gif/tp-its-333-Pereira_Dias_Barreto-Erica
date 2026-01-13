from flask_sqlalchemy import SQLAlchemy

# ⚡ on initialise seulement, app viendra après
db = SQLAlchemy()

class Groupe(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    # Relation 1 → N
    etudiants = db.relationship('Etudiant', backref='groupe', lazy=True)

    def __repr__(self):
        return f"<Groupe {self.nom}>"

class Etudiant(db.Model):
    __tablename__ = "etudiant"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def __repr__(self):
        return f"<Etudiant {self.nom}>"



