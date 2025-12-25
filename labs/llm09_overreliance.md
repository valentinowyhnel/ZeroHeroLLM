# Lab LLM09: Overreliance

## 1️⃣ Description du risque (OWASP-style)

La sur-confiance (Overreliance) se produit lorsque les humains ou les systèmes automatisés font une confiance excessive aux sorties d'un LLM sans une supervision ou une validation adéquate. Les LLM peuvent "halluciner" (inventer des faits), générer des informations incorrectes, du code non sécurisé, ou des conseils trompeurs. Si ces sorties sont utilisées aveuglément, cela peut conduire à de graves erreurs.

-   **Impact Sécurité :** Introduction de vulnérabilités dans le code (par exemple, injection SQL, XSS) si un développeur copie-colle du code généré par un LLM sans le vérifier. Diffusion de désinformation. Prise de mauvaises décisions de sécurité basées sur des analyses erronées du LLM.
-   **Impact Business :** Erreurs factuelles dans des documents publics, mauvaise prise de décision stratégique, perte de productivité due à la correction de code bogué, et responsabilité légale si des conseils incorrects sont fournis aux clients.
-   **Impact Conformité :** Si un LLM génère une procédure non conforme (par exemple, pour la gestion de données personnelles) et qu'elle est appliquée, cela peut entraîner une violation réglementaire.

Cette vulnérabilité est l'une des plus répandues et insidieuses, car elle est de nature humaine et organisationnelle. La facilité et l'apparente autorité des réponses du LLM encouragent les utilisateurs à baisser leur garde et à négliger la diligence raisonnable.

## 2️⃣ Contexte du lab (scénario réel)

-   **Entreprise :** Une équipe de développement logiciel dans une grande entreprise.
-   **Rôle du LLM :** L'entreprise a fourni à tous ses développeurs un accès à un assistant de codage IA de pointe (similaire à GitHub Copilot) pour accélérer le développement. Les développeurs l'utilisent pour générer des extraits de code, écrire des fonctions, et obtenir de l'aide sur des tâches de programmation.
-   **Culture d'entreprise :** La pression pour livrer rapidement de nouvelles fonctionnalités est intense. Les développeurs, en particulier les plus juniors, sont encouragés à utiliser l'assistant IA autant que possible pour respecter les délais serrés.

## 3️⃣ Mauvaise implémentation (VOLONTAIRE)

L'erreur n'est pas technique mais **procédurale et culturelle**. Il n'y a aucune politique, formation ou processus de revue de code en place pour gérer l'utilisation des assistants de codage IA.

-   **Processus Vulnérable :**
    `Developer Task → Prompt to AI Assistant → **AI-generated Code** → **Copy-Paste into Codebase** → Commit → No Specific Security Review`
-   **Hypothèse Dangereuse :** "L'assistant IA a été entraîné sur d'énormes quantités de code, il doit donc connaître les bonnes pratiques de sécurité."
-   **Décision Managériale Incorrecte :**
    1.  Déployer un outil puissant sans former les employés à ses risques (hallucinations, code non sécurisé).
    2.  Ne pas adapter les processus de revue de code (Code Review) pour inclure une vérification sceptique spécifique du code généré par l'IA.
    3.  Mettre la pression sur la vitesse de livraison au détriment de la qualité et de la sécurité.
-   **Mitigations Actives :** Aucune.

## 4️⃣ Implémentation technique vulnérable

Le "code vulnérable" ici est le résultat de l'interaction entre un développeur junior et l'assistant IA.

-   **Tâche du Développeur :** Un développeur junior, Alex, doit créer une nouvelle fonctionnalité : une page d'administration qui permet de rechercher des utilisateurs dans la base de données de l'application.

-   **Interaction avec l'IA (Prompt) :**
    Alex, pressé par le temps, demande à l'assistant IA :
    `"Écris-moi une fonction Flask en Python qui prend un nom d'utilisateur depuis un paramètre de requête d'URL et renvoie les informations de cet utilisateur depuis une base de données SQLite."`

-   **Code Généré par l'IA :**
    L'assistant IA, pour être rapide et direct, génère le code suivant, qui est fonctionnel mais gravement non sécurisé :
    ```python
    # Code généré par l'IA
    import sqlite3
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/user_search')
    def search_user():
        username = request.args.get('username')
        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        # ❌ CRITICAL FLAW: SQL Injection vulnerability
        # The AI used an f-string to build the query, which is a common but
        # dangerous pattern it might have learned from insecure public code.
        query = f"SELECT * FROM users WHERE username = '{username}'"

        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return str(user)
        else:
            return "User not found", 404
    ```
-   **Action du Développeur :** Alex, voyant que le code semble simple et fonctionne lors d'un test rapide avec un nom d'utilisateur valide, le copie-colle directement dans la base de code de l'application et le commite.

## 5️⃣ Scénario d’attaque

-   **Objectif de l’attaquant :** Un attaquant a découvert la nouvelle page `/user_search` et suspecte qu'elle a été développée à la hâte. Il veut exploiter une vulnérabilité d'injection SQL pour extraire toutes les données de la table des utilisateurs.
-   **Étapes de l’attaque :**
    1.  L'attaquant envoie une requête normale pour voir comment la page réagit : `/user_search?username=alice`.
    2.  Il crafte ensuite une charge utile d'injection SQL et l'insère dans le paramètre `username` de l'URL.
-   **Payload / URL Malveillante :**
    `/user_search?username=' OR 1=1 --`
-   **Comment ça marche :**
    -   Le `username` reçu par Flask est `' OR 1=1 --`.
    -   La requête SQL devient : `SELECT * FROM users WHERE username = '' OR 1=1 --'`
    -   La condition `1=1` est toujours vraie, donc la clause `WHERE` est toujours satisfaite pour chaque ligne.
    -   `--` commente le reste de la requête, ignorant le `'` final.
    -   La requête renvoie donc **tous les utilisateurs** de la base de données.

## 6️⃣ Résultat attendu (attaque réussie)

-   **Comportement dangereux observé :** Le développeur, faisant trop confiance à l'IA, a introduit une vulnérabilité critique dans l'application.
-   **Données exposées :** L'attaquant réussit à contourner la logique de recherche et exfiltre les données de tous les utilisateurs (noms, mots de passe hashés, e-mails, etc.).
-   **Logs :** Les logs de l'application montreront une requête `200 OK` sur l'endpoint `/user_search`, ce qui ne semble pas suspect à première vue sans une inspection détaillée des paramètres de la requête.

## 7️⃣ Mission de l’apprenant (LAB TASK)

"Vous êtes un relecteur de code (Code Reviewer) senior. Une nouvelle fonctionnalité a été développée par un membre junior de l'équipe à l'aide d'un assistant IA.
Votre mission :
1.  **Examinez** le code de la fonction `search_user` généré par l'IA.
2.  **Identifiez** la vulnérabilité d'injection SQL et expliquez pourquoi l'utilisation de f-strings pour construire des requêtes SQL est dangereuse.
3.  **Démontrez** l'exploit en créant une URL qui renvoie les données de plusieurs utilisateurs.
4.  **Corrigez** le code en utilisant des pratiques de codage sécurisées (requêtes paramétrées).
5.  **Rédigez** une courte politique de revue de code pour votre équipe, décrivant comment examiner de manière critique le code généré par l'IA."

## 8️⃣ Correction sécurisée (BEST PRACTICES)

La correction est à la fois technique et organisationnelle.

-   **Correction Technique (Code) :**
    -   **Requêtes Paramétrées (Prepared Statements) :** C'est la défense fondamentale contre l'injection SQL. Le driver de la base de données est responsable de la sanitarisation des entrées.
-   **Correction Organisationnelle (Processus) :**
    -   **Formation à la Sécurité :** Formez les développeurs à ne jamais faire confiance au code généré par l'IA. Il doit être traité comme le code d'un stagiaire : une suggestion à vérifier, pas une vérité à accepter.
    -   **Checklists de Revue de Code :** Mettez à jour vos checklists de revue de code pour inclure des points spécifiques à l'IA, tels que : "Le code généré par l'IA a-t-il été vérifié pour des vulnérabilités communes (Top 10 OWASP) ?" et "Le code gère-t-il correctement les entrées utilisateur ?".
    -   **Outils SAST :** Intégrez des outils d'analyse de code statique (SAST) dans votre pipeline CI/CD pour détecter automatiquement les vulnérabilités comme l'injection SQL avant que le code n'atteigne la production.

## 9️⃣ Version sécurisée (implémentation corrigée)

-   **Code Corrigé :**
    ```python
    # Code corrigé par le relecteur
    import sqlite3
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/user_search_secure')
    def search_user_secure():
        username = request.args.get('username')
        db = sqlite3.connect('users.db')
        cursor = db.cursor()

        # ✅ SECURE FIX: Parameterized query
        # The '?' is a placeholder. The database driver will safely
        # substitute the 'username' variable, preventing injection.
        query = "SELECT * FROM users WHERE username = ?"

        cursor.execute(query, (username,)) # The arguments are passed as a tuple
        user = cursor.fetchone()

        if user:
            return str(user)
        else:
            return "User not found", 404
    ```
-   **Explication :** La version sécurisée utilise une requête paramétrée. La requête SQL et les données de l'utilisateur sont envoyées séparément à la base de données. Le driver de la base de données s'assure que les données de la variable `username` sont traitées comme des données littérales et non comme une partie de la commande SQL, ce qui neutralise complètement l'attaque par injection.

## 🔟 Critères de validation du lab

-   **Test 1 (Attaque) :** L'apprenant doit prouver qu'il peut exploiter l'injection SQL sur l'endpoint `/user_search` vulnérable en utilisant la charge utile `' OR 1=1 --`.
-   **Test 2 (Échec de l'attaque) :** L'apprenant doit montrer qu'en envoyant la même charge utile à l'endpoint `/user_search_secure`, l'attaque échoue et il reçoit une réponse "User not found".
-   **Test 3 (Code) :** La solution de code corrigée doit impérativement utiliser une requête paramétrée (`?` ou `%s` selon le driver) et non une tentative de sanitarisation manuelle.
-   **Test 4 (Politique) :** L'apprenant doit soumettre un document `CODE_REVIEW_POLICY.md` contenant au moins 3 règles spécifiques à la revue de code généré par l'IA.
