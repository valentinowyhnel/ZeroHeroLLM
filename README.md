# Laboratoire de Sécurité OWASP Top 10 pour les Applications LLM

Ce projet est une application web interactive conçue pour être un laboratoire éducatif sur les 10 principales vulnérabilités de sécurité pour les applications de grands modèles de langage (LLM), telles que définies par l'OWASP.

L'application fournit une démonstration pratique et des explications pour chaque vulnérabilité, ainsi que des stratégies d'atténuation.

## Fonctionnalités

-   Une page d'accueil répertoriant les 10 principales vulnérabilités de l'OWASP pour les LLM.
-   Des laboratoires interactifs ou explicatifs dédiés à chaque vulnérabilité.
-   Des simulations claires pour démontrer comment chaque vulnérabilité peut être exploitée.
-   Des explications détaillées et des stratégies d'atténuation pour chaque faille de sécurité.
-   Une interface utilisateur propre et stylisée pour une expérience d'apprentissage agréable.

## Vulnérabilités couvertes

1.  **LLM01:** Injection de Prompt
2.  **LLM02:** Gestion non sécurisée des sorties
3.  **LLM03:** Empoisonnement des données d'entraînement
4.  **LLM04:** Déni de service du modèle
5.  **LLM05:** Vulnérabilités de la chaîne d'approvisionnement
6.  **LLM06:** Divulgation d'informations sensibles
7.  **LLM07:** Conception non sécurisée de plugins
8.  **LLM08:** Agence excessive
9.  **LLM09:** Sur-confiance
10. **LLM10:** Vol de modèle

## Installation et exécution locale

### Prérequis

-   Python 3.7+
-   pip

### Étapes

1.  **Clonez le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT>
    cd <NOM_DU_DEPOT>
    ```

2.  **Créez un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
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

## Exécution avec Docker

### Prérequis

-   Docker

### Étapes

1.  **Construisez l'image Docker :**
    À la racine du projet (où se trouve le `Dockerfile`), exécutez la commande suivante :
    ```bash
    docker build -t owasp-llm-lab .
    ```

2.  **Exécutez le conteneur Docker :**
    Une fois l'image construite, lancez un conteneur :
    ```bash
    docker run -p 5000:5000 owasp-llm-lab
    ```

3.  **Accédez à l'application :**
    Ouvrez votre navigateur et allez à `http://localhost:5000`.
