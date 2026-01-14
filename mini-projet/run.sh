#!/bin/bash

# Supprime les anciens conteneurs
docker rm -f person-service health-service 2>/dev/null

# Crée le réseau si pas déjà créé
docker network inspect micro-net >/dev/null 2>&1 || docker network create micro-net

# Lancer Person-service
docker build -t person-service ./person-service
docker run -d --name person-service --network micro-net -p 5001:5001 person-service

# Lancer Health-service
docker build -t health-service ./health-service
docker run -d --name health-service --network micro-net -p 5002:5002 health-service

echo "Les deux services sont démarrés !"
echo "Person-service: http://localhost:5001/apidocs"
echo "Health-service: http://localhost:5002/apidocs"
