# Laboratoire de Sécurité OWASP Top 10 pour les Applications LLM

## 1. Introduction

Ce projet est une application web interactive conçue comme un laboratoire éducatif pour les 10 principales vulnérabilités de sécurité des applications de grands modèles de langage (LLM), telles que définies par l'[OWASP](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

L'application fournit des démonstrations pratiques, des explications approfondies et des stratégies d'atténuation pour chaque vulnérabilité, permettant aux développeurs, aux professionnels de la sécurité et aux passionnés de comprendre et de se défendre contre ces menaces émergentes.

## 2. Architecture et technologies

L'application est construite sur une pile technologique simple mais robuste :

-   **Backend :** [Flask](https://flask.palletsprojects.com/), un micro-framework web Python léger.
-   **Frontend :** HTML standard avec des modèles [Jinja2](https://jinja.palletsprojects.com/) et du CSS simple.
-   **Serveur WSGI :** [Gunicorn](https://gunicorn.org/) est utilisé comme serveur d'application web pour le déploiement en production, offrant de meilleures performances et une meilleure stabilité que le serveur de développement de Flask.
-   **Conteneurisation :** [Docker](https://www.docker.com/) est utilisé pour empaqueter l'application et ses dépendances dans une image portable et cohérente, facilitant ainsi un déploiement facile sur n'importe quelle machine.

## 3. Structure des fichiers

Le projet est organisé comme suit pour une séparation claire des préoccupations :

```
.
├── app.py              # Le fichier principal de l'application Flask, contenant la logique du backend et le routage.
├── Dockerfile          # Les instructions pour construire l'image Docker de l'application.
├── requirements.txt    # Une liste des dépendances Python du projet.
├── static/
│   └── style.css       # La feuille de style CSS pour le frontend.
├── templates/
│   ├── base.html       # Le modèle HTML de base dont héritent toutes les autres pages.
│   ├── index.html      # Le modèle pour la page d'accueil.
│   └── llm01.html ...  # Les modèles pour chaque laboratoire de vulnérabilité.
├── .dockerignore       # Spécifie les fichiers à exclure du contexte de construction de Docker.
└── .gitignore          # Spécifie les fichiers non suivis par Git.
```

## 4. Description des laboratoires de vulnérabilités

Chaque laboratoire simule une vulnérabilité spécifique du Top 10 de l'OWASP pour les LLM :

-   **LLM01: Injection de Prompt :** Démontre comment un attaquant peut manipuler l'entrée pour faire en sorte que le LLM ignore ses instructions initiales et exécute des commandes involontaires.
-   **LLM02: Gestion non sécurisée des sorties :** Montre comment une sortie non nettoyée du LLM peut conduire à des vulnérabilités côté client comme le Cross-Site Scripting (XSS).
-   **LLM03: Empoisonnement des données d'entraînement :** Simule comment des données d'entraînement compromises peuvent introduire des portes dérobées ou des biais dans le comportement du modèle.
-   **LLM04: Déni de service du modèle :** Illustre comment des requêtes gourmandes en ressources peuvent surcharger le modèle, entraînant des temps de réponse lents et des coûts élevés.
-   **LLM05: Vulnérabilités de la chaîne d'approvisionnement :** Simule l'utilisation d'un modèle tiers compromis qui contient une porte dérobée cachée pour exfiltrer des données.
-   **LLM06: Divulgation d'informations sensibles :** Montre comment un LLM peut divulguer accidentellement des informations confidentielles sur lesquelles il a été entraîné.
-   **LLM07: Conception non sécurisée de plugins :** Démontre les risques de plugins mal conçus qui peuvent être exploités pour exécuter du code arbitraire sur le serveur.
-   **LLM08: Agence excessive :** Simule comment donner trop d'autonomie ou de permissions à un LLM pour interagir avec d'autres systèmes peut être abusé.
-   **LLM09: Sur-confiance :** Met en évidence les dangers de faire aveuglément confiance au code généré par l'IA, qui peut contenir des vulnérabilités de sécurité.
-   **LLM10: Vol de modèle :** Explique la menace du vol de modèles propriétaires et les différentes techniques utilisées par les attaquants.

## 5. Déploiement et exécution

Vous pouvez exécuter cette application localement pour le développement ou en utilisant Docker pour un déploiement plus cohérent.

### 5.1. Exécution locale

Cette méthode est idéale pour le développement et le test.

**Prérequis :**
-   Python 3.7+
-   pip

**Étapes :**
1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```
2.  **Créez et activez un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```
3.  **Installez les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Exécutez l'application :**
    ```bash
    python app.py
    ```
5.  Ouvrez votre navigateur et allez à `http://127.0.0.1:5000`.

### 5.2. Exécution avec Docker

Cette méthode est recommandée pour la production et pour garantir un environnement d'exécution cohérent.

**Prérequis :**
-   Docker

**Étapes :**
1.  **Construisez l'image Docker :**
    À la racine du projet, exécutez la commande suivante. Cela créera une image nommée `owasp-llm-lab`.
    ```bash
    DOCKER_GID=$(getent group docker | cut -d: -f3)
    docker build --build-arg DOCKER_GID=$DOCKER_GID -t owasp-llm-lab .
    ```
2.  **Exécutez le conteneur Docker :**
    Lancez un conteneur à partir de l'image nouvellement construite. L'application sera accessible sur le port 5000 de votre machine hôte.
    ```bash
    docker run -d -p 5000:5000 --rm --name owasp_main_app -v /var/run/docker.sock:/var/run/docker.sock owasp-llm-lab
    ```
3.  **Accédez à l'application :**
    Ouvrez votre navigateur et allez à `http://localhost:5000`.

---
*Ce projet est à des fins éducatives uniquement et n'est pas destiné à être utilisé en production sans un examen de sécurité approfondi.*
