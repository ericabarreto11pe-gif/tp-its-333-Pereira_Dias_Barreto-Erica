from app import app
from flask import render_template, request, jsonify

### EXO1 - simple API
@app.route('/')
def index():
    return render_template('index.html')

### EXO3 - API with parameters display 
@app.route('/api/utilisateur', methods=['GET'])
def utilisateur():
    # données FIXES dans le backend
    nom = "Erica"
    age = 23

    return jsonify(
        nom=nom,
        age=age
    )

if __name__ == '__main__':
    app.run(debug=True)



### EXO2 - API with simple display


### EXO4 - API with parameters retrieved from URL 

@app.route('/api/utilisateur/<nom>/<int:age>', methods=['GET'])
def utilisateur(nom, age):
    return jsonify(
        nom=nom,
        age=age
    )

if __name__ == '__main__':
    app.run(debug=True)