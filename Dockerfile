# Utiliser une image Python officielle et légère comme image de base
FROM python:3.9-slim

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_RUN_HOST=0.0.0.0

# Mettre à jour l'index des paquets et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends docker.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

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
# Le groupe docker est créé lors de l'installation de docker.io
RUN useradd -m appuser && usermod -aG docker appuser

# Changer pour l'utilisateur non-root
USER appuser

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Définir la commande pour exécuter l'application lorsque le conteneur démarre
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
