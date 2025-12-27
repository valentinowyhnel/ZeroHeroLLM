# Lab LLM06: Sensitive Information Disclosure

## 1️⃣ Description du risque (OWASP-style)

La divulgation d'informations sensibles (Sensitive Information Disclosure) se produit lorsqu'un LLM révèle involontairement des données confidentielles dans ses réponses. Ces données peuvent provenir de ses données d'entraînement, de son contexte de prompt, ou de sources de données augmentées (Retrieval Augmented Generation - RAG).

-   **Impact Sécurité :** Fuite de secrets d'entreprise (clés d'API, mots de passe), exposition de données personnelles identifiables (PII), violation de la confidentialité, et fourniture d'informations qui peuvent aider un attaquant à préparer d'autres attaques.
-   **Impact Business :** Perte de secrets commerciaux et d'avantage concurrentiel, sanctions réglementaires (RGPD, CCPA), atteinte à la réputation, et perte de confiance des clients.
-   **Impact Conformité :** Violation directe de la plupart des réglementations sur la protection des données si des PII sont exposées.

Cette vulnérabilité est extrêmement réaliste car les LLM sont souvent entraînés sur des corpus de données massifs et non-filtrés qui peuvent contenir des informations sensibles. De plus, dans les systèmes RAG, un contrôle d'accès inadéquat sur les sources de données peut permettre au LLM d'accéder et de divulguer des informations auxquelles l'utilisateur ne devrait pas avoir droit.

## 2️⃣ Contexte du lab (scénario réel)

-   **Entreprise :** Une grande entreprise technologique.
-   **Rôle du LLM :** L'entreprise a déployé un chatbot interne, "CorpHelper", pour aider les employés à trouver des informations dans la documentation interne de l'entreprise.
-   **Architecture :** Le chatbot utilise une architecture RAG (Retrieval Augmented Generation). Lorsqu'un employé pose une question, le système recherche des documents pertinents dans une base de données vectorielle (Vector DB) contenant toute la documentation de l'entreprise (Confluence, Jira, documents de design, etc.). Les extraits pertinents sont ensuite injectés dans le contexte du prompt du LLM pour qu'il puisse formuler une réponse précise.

## 3️⃣ Mauvaise implémentation (VOLONTAIRE)

L'erreur critique est l'absence de contrôle d'accès au niveau du système de recherche (le "Retriever" du RAG). Le système récupère des documents en se basant uniquement sur la similarité sémantique, sans vérifier si l'utilisateur qui pose la question a les permissions nécessaires pour lire ces documents.

-   **Architecture Vulnérable :**
    `User Query → **Retriever (No Access Control)** → Vector DB (All Company Docs) → Relevant Chunks → LLM Context → Answer`
-   **Hypothèse Dangereuse :** "Si un utilisateur ne pose pas de question sur un sujet sensible, le système ne récupérera pas de documents sensibles."
-   **Décision Technique Incorrecte :** La base de données vectorielle a été peuplée avec tous les documents de l'entreprise, y compris des informations hautement confidentielles (secrets de production, stratégies financières, données RH), sans y attacher de métadonnées de contrôle d'accès (ACL).
-   **Mitigations Actives :** Aucune. Le LLM a accès à tout ce que le Retriever lui fournit.

## 4️⃣ Implémentation technique vulnérable

-   **Architecture :** Une application Flask qui simule un système RAG. Elle prend une requête utilisateur, effectue une recherche de similarité sur une collection de documents (simulée par un dictionnaire Python), et passe les résultats à un LLM.

-   **Simulation de la Base de Données Vectorielle :**
    ```python
    # Simulated document store with no access control metadata
    DOCUMENT_STORE = {
        "doc1_public": "Our company values are collaboration and innovation.",
        "doc2_public": "To reset your password, please contact IT support.",
        "doc3_internal": "The Q4 financial strategy involves a 10% budget cut in marketing.",
        "doc4_confidential": "The root password for the production database is 'Str0ngP@ssw0rd!_ChangeMe'.",
        "doc5_public_tech": "Our frontend is built with React and TypeScript."
    }
    ```

-   **Code Vulnérable (Python / Flask) :**
    ```python
    # app.py
    from flask import Flask, request, jsonify
    import ollama

    app = Flask(__name__)

    # Vulnerable retriever: finds documents based on keywords, ignores user permissions.
    def vulnerable_retriever(query):
        retrieved = []
        for doc_id, content in DOCUMENT_STORE.items():
            # Simple keyword matching for simulation
            if any(word in content.lower() for word in query.lower().split()):
                retrieved.append(content)
        return retrieved

    @app.route("/ask-corp-helper", methods=["POST"])
    def ask():
        user_query = request.json.get("query")

        # ❌ FLAW: The retriever fetches data without checking user's rights.
        retrieved_context = vulnerable_retriever(user_query)

        if not retrieved_context:
            return jsonify({"response": "I could not find any relevant information."})

        system_prompt = f"""
    You are CorpHelper, an internal assistant. Answer the user's query based ONLY on the
    following context. Do not invent information.

    Context:
    ---
    {"\n---\n".join(retrieved_context)}
    ---
    """

        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )

        return jsonify({"response": response['message']['content']})
    ```

## 5️⃣ Scénario d’attaque

-   **Objectif de l’attaquant :** Un employé junior ou un consultant externe avec un accès limité au système veut trouver des informations confidentielles pour lesquelles il n'a pas d'autorisation.
-   **Étapes de l’attaque :**
    1.  L'attaquant interagit avec le chatbot "CorpHelper".
    2.  Il pose des questions vagues mais sémantiquement proches de sujets potentiellement sensibles.
    3.  Le Retriever, ignorant les permissions, va chercher les documents correspondants, y compris les plus confidentiels, et les fournit au LLM.
    4.  Le LLM, voyant ces informations dans son contexte, les utilise pour répondre à la question de l'attaquant.
-   **Payload / Requêtes Malveillantes :**
    -   Requête 1 (subtile) : `"What are some important credentials I should be aware of for system maintenance?"`
    -   Requête 2 (plus directe) : `"Tell me about the password for our main database."`
    -   Requête 3 (ciblant la finance) : `"What's the latest on our financial planning and budgets?"`

## 6️⃣ Résultat attendu (attaque réussie)

-   **Comportement dangereux observé :** Pour la requête `"database password"`, le `vulnerable_retriever` trouve le `doc4_confidential` car il contient les mots "database" et "password".
-   **Contexte compromis :** Ce document confidentiel est injecté dans le contexte du LLM.
-   **Données exposées :** Le LLM, suivant ses instructions, répond en se basant sur le contexte fourni et dit : `"Based on the context, the root password for the production database is 'Str0ngP@ssw0rd!_ChangeMe'."`
-   **Logs :** Les logs montreront une interaction apparemment normale. Seul un audit approfondi du contexte de chaque prompt pourrait révéler la fuite.

## 7️⃣ Mission de l’apprenant (LAB TASK)

"Vous êtes un ingénieur en sécurité des données. Le chatbot 'CorpHelper' est suspecté de fuites d'informations.
Votre mission :
1.  **Analysez** l'architecture RAG et le code du `vulnerable_retriever`.
2.  **Identifiez** l'absence critique de contrôles d'accès dans le processus de récupération de documents.
3.  **Craftez** des requêtes pour prouver que vous pouvez extraire des secrets de production et des informations financières confidentielles via le chatbot.
4.  **Concevez et implémentez** un système de "post-filtrage" sur les documents récupérés pour garantir que les utilisateurs ne voient que les informations auxquelles ils ont droit."

## 8️⃣ Correction sécurisée (BEST PRACTICES)

La solution la plus robuste est le "pre-filtering" ou le "metadata-based filtering", où la base de données vectorielle elle-même applique des filtres basés sur les permissions de l'utilisateur *pendant* la recherche. Cependant, une solution plus simple à implémenter (et un bon début) est le "post-filtering".

-   **Architecture Sécurisée (Post-filtering) :**
    `User Query (with User ID) → Retriever → Vector DB → **All Relevant Chunks** → **Access Control Filter** → **Authorized Chunks** → LLM Context → Answer`
-   **Enrichissement des Données :** Chaque document (ou "chunk") dans la base de données vectorielle doit être stocké avec des métadonnées de contrôle d'accès.
    `{ "content": "...", "metadata": { "allowed_roles": ["admin", "finance"] } }`
-   **Contrôle d'Accès :** Le retriever doit connaître le rôle de l'utilisateur actuel et l'utiliser pour filtrer les résultats.

## 9️⃣ Version sécurisée (implémentation corrigée)

-   **Simulation de la DB Vectorielle avec Métadonnées :**
    ```python
    SECURE_DOCUMENT_STORE = {
        "doc1": {"content": "...", "allowed_roles": ["all"]},
        "doc2": {"content": "...", "allowed_roles": ["all"]},
        "doc3": {"content": "...", "allowed_roles": ["finance", "executive"]},
        "doc4": {"content": "...", "allowed_roles": ["database_admins"]}
    }
    ```
-   **Code Corrigé (avec Post-filtering) :**
    ```python
    # ... (imports)

    def get_user_role(request): # Mock function
        return request.headers.get("X-User-Role", "employee")

    def secure_retriever(query, user_role):
        # Step 1: Retrieve based on semantic similarity (same as before)
        retrieved_docs = [] # Assume this gets all potentially relevant docs
        # ...

        # ✅ Step 2: Post-filter based on user permissions
        authorized_docs = []
        for doc in retrieved_docs:
            if "all" in doc["allowed_roles"] or user_role in doc["allowed_roles"]:
                authorized_docs.append(doc)
        return [d["content"] for d in authorized_docs]

    @app.route("/ask-corp-helper-secure", methods=["POST"])
    def ask_secure():
        user_query = request.json.get("query")
        user_role = get_user_role(request) # Get the user's role

        # ✅ The retriever now uses the user's role to filter results
        retrieved_context = secure_retriever(user_query, user_role)

        # ... (The rest of the function is the same)
    ```
-   **Explication :** La version sécurisée introduit la notion de rôle utilisateur. Le `secure_retriever` effectue d'abord la recherche sémantique, mais ensuite, il boucle sur les résultats et ne conserve que les documents pour lesquels l'utilisateur actuel a les permissions requises. Si un employé junior (rôle `employee`) pose une question sur les mots de passe de la base de données, le document `doc4` sera peut-être récupéré par la recherche initiale, mais il sera immédiatement écarté par le filtre de sécurité car le rôle `employee` n'est pas dans la liste `["database_admins"]`. Le LLM ne verra donc jamais l'information confidentielle.

## 🔟 Critères de validation du lab

-   **Test 1 (Attaque) :** L'apprenant doit prouver qu'il peut extraire le mot de passe de la base de données en interrogeant l'endpoint `/ask-corp-helper`.
-   **Test 2 (Échec de l'attaque) :** L'apprenant doit montrer qu'en envoyant la même requête à `/ask-corp-helper-secure` avec un header `X-User-Role: employee`, la réponse est "Je n'ai pas pu trouver d'information pertinente."
-   **Test 3 (Accès légitime) :** L'apprenant doit prouver qu'en envoyant la requête à `/ask-corp-helper-secure` avec le header `X-User-Role: database_admins`, il obtient une réponse contenant (ou basée sur) le secret.
-   **Test 4 (Code) :** Le code de la solution doit implémenter un mécanisme de filtrage qui compare le rôle de l'utilisateur aux permissions définies dans les métadonnées des documents.
