from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------------------
# Création de la base et table
# ---------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS etudiants (nom TEXT, addr TEXT, pin TEXT)'
    )
    conn.close()

init_db()

# ---------------------------
# Page d'accueil avec formulaire
# ---------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------------------
# Ajouter un étudiant
# ---------------------------
@app.route('/new', methods=['POST'])
def add_etudiant():
    nom = request.form.get('name')
    addr = request.form.get('addr')
    pin = request.form.get('pincode')

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO etudiants (nom, addr, pin) VALUES (?, ?, ?)",
            (nom, addr, pin)
        )
        con.commit()

    return f"Étudiant {nom} ajouté avec succès !"

# ---------------------------
# Afficher les étudiants
# ---------------------------
@app.route('/etudiants')
def liste_etudiants():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row   # ⭐ important
    cur = conn.cursor()
    cur.execute("SELECT nom, addr, pin FROM etudiants")
    rows = cur.fetchall()
    conn.close()

    return render_template("base.html", etudiants=rows)

# ---------------------------
# Lancement de l'app
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
