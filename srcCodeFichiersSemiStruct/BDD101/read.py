import json

# 1️⃣ Ouvrir et lire le fichier JSON
with open("data.json", "r") as f:
    data = json.load(f)

print("Avant modification :")
print(data)

# 2️⃣ Modifier les données
for feature in data["features"]:
    # Modifier les coordonnées
    feature["geometry"]["coordinates"] = [110.0, 90.0]

    # Ajouter une propriété
    feature["properties"]["prop34"] = True

# 3️⃣ Réécrire le JSON dans le fichier (MODIFICATION PERMANENTE)
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("\nAprès modification (fichier mis à jour) :")
print(data)

