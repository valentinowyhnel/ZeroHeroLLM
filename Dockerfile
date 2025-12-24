# Utiliser une image Python officielle et légère comme image de base
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_RUN_HOST=0.0.0.0

# Déclarer l'argument pour le GID du groupe Docker
ARG DOCKER_GID

# Mettre à jour l'index des paquets
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer un groupe docker avec le GID de l'hôte
RUN if [ -z "$DOCKER_GID" ]; then echo "Warning: DOCKER_GID not set. Using default."; groupadd docker; else groupadd -g $DOCKER_GID docker; fi

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances en premier pour profiter de la mise en cache de Docker
COPY requirements.txt requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install docker

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Créer un utilisateur non-root et l'ajouter au groupe docker
RUN useradd -m appuser && usermod -aG docker appuser

# Changer pour l'utilisateur non-root
USER appuser

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Définir la commande pour exécuter l'application lorsque le conteneur démarre
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
