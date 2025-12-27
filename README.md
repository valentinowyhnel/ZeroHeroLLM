# Laboratoire de Sécurité OWASP Top 10 pour les Applications LLM

## 1. Introduction

Ce projet est une application web interactive conçue comme un laboratoire éducatif pour les 10 principales vulnérabilités de sécurité des applications de grands modèles de langage (LLM), telles que définies par l'[OWASP](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

L'application fournit des démonstrations pratiques, des explications approfondies et des simulations de LLM vulnérables pour chaque vulnérabilité, permettant aux développeurs, aux professionnels de la sécurité et aux passionnés de comprendre et de se défendre contre ces menaces émergentes.

## 2. Architecture et technologies

L'application est construite sur une pile technologique simple et centralisée :

-   **Backend :** [Flask](https://flask.palletsprojects.com/), un micro-framework web Python léger.
-   **Frontend :** HTML standard avec des modèles [Jinja2](https://jinja.palletsprojects.com/) et du CSS simple.
-   **Serveur WSGI :** [Gunicorn](https://gunicorn.org/) est utilisé comme serveur d'application web pour le déploiement en production.

## 3. Structure des fichiers

Le projet est organisé comme suit :

```
.
├── app.py              # Le fichier principal de l'application Flask, contenant la logique du backend, le routage et la simulation des LLM.
├── requirements.txt    # Une liste des dépendances Python du projet.
├── static/
│   └── style.css       # La feuille de style CSS pour le frontend.
├── templates/
│   ├── base.html       # Le modèle HTML de base.
│   ├── index.html      # Le modèle pour la page d'accueil.
│   └── lab.html        # Le modèle générique pour toutes les pages de laboratoire.
└── .gitignore          # Spécifie les fichiers non suivis par Git.
```

## 4. Description des laboratoires de vulnérabilités

Chaque laboratoire simule une vulnérabilité spécifique du Top 10 de l'OWASP pour les LLM :

-   **LLM01: Injection de Prompt :** Démontre comment un attaquant peut manipuler l'entrée pour faire en sorte que le LLM ignore ses instructions initiales.
-   **LLM02: Gestion non sécurisée des sorties :** Montre comment une sortie non nettoyée du LLM peut conduire à des vulnérabilités comme le Cross-Site Scripting (XSS).
-   **LLM03: Empoisonnement des données d'entraînement :** Simule comment des données d'entraînement compromises peuvent introduire des biais dans le comportement du modèle.
-   **LLM04: Déni de service du modèle :** Illustre comment des requêtes gourmandes en ressources peuvent surcharger le modèle.
-   **LLM05: Vulnérabilités de la chaîne d'approvisionnement :** Simule l'utilisation d'un modèle qui expose des informations sensibles.
-   **LLM06: Divulgation d'informations sensibles :** Montre comment un LLM peut divulguer accidentellement des informations confidentielles.
-   **LLM07: Conception non sécurisée de plugins :** Démontre les risques de plugins qui peuvent être exploités pour exécuter des actions non désirées.
-   **LLM08: Agence excessive :** Simule comment un LLM avec trop d'autonomie peut prendre des décisions nuisibles.
-   **LLM09: Sur-confiance :** Met en évidence les dangers de faire aveuglément confiance au code généré par l'IA.
-   **LLM10: Vol de modèle :** Explique la menace du vol de modèles propriétaires.

## 5. Déploiement et exécution

**Prérequis :**
-   Python 3.7+
-   pip
-   [Ollama](https://ollama.com/) installé et en cours d'exécution sur votre machine locale.

**Étapes :**
1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/valentinowyhnel/ZeroHeroLLM.git
    cd ZeroHeroLLM
    ```
2.  **Téléchargez le modèle LLM requis :**
    Avant de lancer l'application, vous devez télécharger le modèle `llama3` via Ollama.
    ```bash
    ollama pull llama3
    ```
3.  **Créez et activez un environnement virtuel :**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    ```
4.  **Installez les dépendances Python :**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Exécutez l'application Flask :**
    Assurez-vous que votre application Ollama est en cours d'exécution.
    ```bash
    python3 app.py
    ```
6.  Ouvrez votre navigateur et allez à `http://127.0.0.1:5000`.

---

## 🚀 Overview

**ZeroHeroLLM** is an interactive, educational web application designed as a **hands-on security laboratory** for **Large Language Model (LLM)** applications.

This project focuses on the **OWASP Top 10 vulnerabilities for LLMs**, helping users understand:

- How LLM vulnerabilities work  
- How attackers exploit them  
- How developers can mitigate and defend against them  

&gt; Designed for **beginners, students, developers**, and **cybersecurity professionals** who want a **clear and practical introduction to LLM security**.

⚠️ **This project is educational and preventive.**  
It is **not intended for production use** without a full security review.

---

## 🎯 Project Objectives

- Explain LLM security risks in a **simple and accessible** way  
- Simulate **realistic attack scenarios**  
- Provide **hands-on labs** aligned with **OWASP standards**  
- Promote **secure-by-design** LLM applications  

&gt; All labs are inspired by the  
&gt; 👉 [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## 🧠 Architecture & Technologies

The project uses a **lightweight and beginner-friendly** tech stack:

- **Backend**: 🐍 Flask (Python micro-framework)  
- **Frontend**: HTML + Jinja2 templates + basic CSS  
- **WSGI Server**: Gunicorn (for production-like deployments)  

&gt; This minimal stack allows learners to **focus on security concepts**, not framework complexity.

---

## 🗂️ Project Structure
