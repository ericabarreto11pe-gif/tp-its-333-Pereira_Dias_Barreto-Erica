from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Fichier JSON contenant les patients
FICHIER_PATIENTS = "patients.json"

@app.route('/api/parametre', methods=['POST'])
def parametre_patient():
    """
    Attend un JSON POST avec :
    {
        "id": 103,            # ou "nom": "Erica"
        "param": "age"         # paramètre de santé à récupérer
    }
    """
    data = request.get_json()
    patient_id = str(data.get("id"))  # les clés du JSON sont des strings
    nom_patient = data.get("nom")
    param = data.get("param")

    if not param:
        return jsonify({"erreur": "Aucun paramètre demandé."}), 400

    # Lire le fichier JSON
    with open(FICHIER_PATIENTS, "r") as f:
        patients = json.load(f)

    patient = None

    # Chercher par ID
    if patient_id and patient_id in patients:
        patient = patients[patient_id]

    # Chercher par nom si ID non trouvé
    if nom_patient and not patient:
        for pid, info in patients.items():
            if info["nom"].lower() == nom_patient.lower():
                patient = info
                break

    if not patient:
        return jsonify({"erreur": "Patient non trouvé."}), 404

    # Vérifier si le paramètre existe
    if param in patient:
        return jsonify({param: patient[param]})
    else:
        return jsonify({"erreur": f"Paramètre '{param}' introuvable pour ce patient."}), 404


if __name__ == '__main__':
    app.run(debug=True)

