# Utiliser une image Python officielle et légère comme image de base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances en premier pour profiter de la mise en cache de Docker
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Ajouter un utilisateur non-root pour des raisons de sécurité
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Définir la commande pour exécuter l'application lorsque le conteneur démarre
# Utilise gunicorn pour un serveur de production plus robuste que le serveur de développement de Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Corriger les permissions pour les commandes nécessitant des privilèges root
USER root
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
USER appuser

# Ajouter des variables d'environnement pour éviter les fuites d'informations sensibles
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Ajouter une variable d'environnement pour définir l'hôte
ENV FLASK_RUN_HOST=0.0.0.0
