# Lab LLM04: Model Denial of Service

## 1️⃣ Description du risque (OWASP-style)

Une attaque par déni de service (Denial of Service - DoS) sur un modèle se produit lorsqu'un attaquant soumet des requêtes qui consomment une quantité disproportionnée de ressources (temps de calcul, mémoire, budget API). Contrairement aux DoS réseau traditionnels, ces attaques ciblent la logique applicative du LLM, en exploitant des tâches coûteuses en ressources.

-   **Impact Sécurité :** Indisponibilité du service pour les utilisateurs légitimes, dégradation des performances. Bien que souvent considérée comme un problème de disponibilité, une attaque DoS peut servir de diversion pour masquer d'autres activités malveillantes.
-   **Impact Business :** Augmentation exponentielle et imprévue des coûts d'API, perte de revenus due à l'indisponibilité du service, mauvaise expérience utilisateur, et atteinte à la réputation.
-   **Impact Conformité :** Si l'indisponibilité du service viole les accords de niveau de service (SLA), cela peut avoir des conséquences contractuelles.

Cette vulnérabilité est très réaliste car la consommation de ressources d'un LLM peut varier de plusieurs ordres de grandeur en fonction de la complexité du prompt. Les attaquants peuvent facilement identifier et abuser des "points chauds" de consommation de ressources.

## 2️⃣ Contexte du lab (scénario réel)

-   **Entreprise :** Une startup qui propose une API publique de "résumé de texte intelligent".
-   **Rôle du LLM :** Le service permet aux utilisateurs de soumettre de longs textes (articles, documents de recherche) et d'obtenir un résumé de haute qualité. Le modèle sous-jacent est un LLM local puissant pour garantir la meilleure qualité possible.
-   **Modèle économique :** Le service est facturé à l'utilisation, mais propose un niveau gratuit ("free tier") généreux pour attirer les utilisateurs, ce qui en fait une cible de choix pour les abus.

## 3️⃣ Mauvaise implémentation (VOLONTAIRE)

L'erreur de conception est l'absence totale de contrôles sur les entrées des utilisateurs et de mécanismes de limitation des ressources. L'entreprise a privilégié la qualité de la sortie et la simplicité de l'API au détriment de la robustesse.

-   **Architecture Vulnérable :**
    `Public User → API Gateway (No Rate Limiting) → Flask App (No Input Validation) → Powerful Local LLM`
-   **Hypothèse Dangereuse :** "Les utilisateurs soumettront des textes de longueur raisonnable et n'abuseront pas du service."
-   **Décision Technique Incorrecte :**
    1.  Ne pas imposer de limite de longueur sur le texte d'entrée.
    2.  Ne pas mettre en place de rate limiting par utilisateur ou par adresse IP.
    3.  Ne pas configurer de timeout sur les appels au LLM.
-   **Mitigations Actives :** Aucune.

## 4️⃣ Implémentation technique vulnérable

-   **Architecture :** Une API Flask publique avec un endpoint `/summarize` qui accepte du texte et le transmet directement à un LLM local.

-   **Code Vulnérable (Python / Flask) :**
    ```python
    from flask import Flask, request, jsonify
    import ollama
    import time

    app = Flask(__name__)
    client = ollama.Client(host="http://127.0.0.1:11434")

    @app.route("/summarize", methods=["POST"])
    def summarize():
        text_to_summarize = request.json.get("text")

        # ❌ FLAW 1: No input length validation

        system_prompt = """
    You are a world-class summarization engine. Read the following text and provide a
    detailed, multi-paragraph summary. The summary must capture all the key nuances.
    For each sentence in your summary, provide a footnote explaining why you included it.
    """

        start_time = time.time()

        try:
            response = client.chat(
                model="phi3:mini", # ❌ FLAW 2: Using a powerful model without controls
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_to_summarize}
                ],
                # ❌ FLAW 3: No timeout configured for the API call
            )

            duration = time.time() - start_time
            return jsonify({
                "summary": response['message']['content'],
                "processing_time": f"{duration:.2f} seconds"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    ```

## 5️⃣ Scénario d’attaque

-   **Objectif de l’attaquant :** Provoquer une dégradation du service pour les autres utilisateurs et infliger des coûts de calcul maximaux au serveur hébergeant le LLM.
-   **Étapes de l’attaque :**
    1.  L'attaquant identifie que l'API n'a pas de limite de taille sur les entrées.
    2.  Il crafte un prompt "bomb" (bombe logique) conçu pour être extrêmement coûteux à traiter. Il ne s'agit pas seulement de la longueur, mais aussi de la complexité de la tâche demandée.
    3.  Il envoie cette requête de manière répétée à l'endpoint `/summarize`.
-   **Payload / Prompt "Bomb" :**
    Un texte très long (par exemple, un livre entier ou un long document technique) combiné à un prompt système qui demande une tâche récursive ou très complexe. Par exemple, l'attaquant pourrait soumettre le code source complet du noyau Linux et demander un "résumé ligne par ligne avec des commentaires sur l'impact de chaque ligne sur la performance globale du système". Le prompt système déjà en place ("ajouter une footnote pour chaque phrase") est déjà un amplificateur de coût.

## 6️⃣ Résultat attendu (attaque réussie)

-   **Comportement dangereux observé :** L'API du LLM prend un temps anormalement long pour répondre (des dizaines de secondes, voire des minutes).
-   **Impact sur le service :** Les workers de l'application Flask/Gunicorn sont bloqués en attendant la réponse du LLM. Les requêtes des utilisateurs légitimes sont mises en file d'attente et finissent par expirer (timeout). Le service devient inutilisable.
-   **Impact financier :** Chaque requête malveillante consomme une grande quantité de CPU et de RAM sur le serveur, pouvant entraîner des coûts d'infrastructure élevés ou un "auto-scaling" coûteux.
-   **Logs :** Les logs montreront des requêtes qui durent très longtemps, ce qui peut saturer les systèmes de logging et de monitoring.

## 7️⃣ Mission de l’apprenant (LAB TASK)

"Vous êtes l'ingénieur SRE (Site Reliability Engineer) de la startup. Le service de résumé de texte est constamment lent et la charge du serveur est anormalement élevée.
Votre mission :
1.  **Analysez** le code de l'API `/summarize` et identifiez les faiblesses qui permettent une attaque par déni de service.
2.  **Craftez** un prompt (un texte long) pour simuler une requête coûteuse en ressources et démontrez qu'elle peut ralentir considérablement le service.
3.  **Expliquez** les impacts financiers et de disponibilité d'une telle attaque à grande échelle.
4.  **Implémentez** plusieurs couches de défense pour rendre l'API résiliente aux abus."

## 8️⃣ Correction sécurisée (BEST PRACTICES)

-   **Validation des entrées (Input Validation) :**
    -   **Limitation de la longueur :** La mesure la plus simple et la plus efficace. Refusez toute entrée dépassant une longueur raisonnable (ex: 10 000 caractères).
    -   **Complexité du prompt :** Analysez et rejetez les prompts contenant des instructions répétitives ou récursives.
-   **Contrôles au niveau de l'API :**
    -   **Rate Limiting :** Limitez le nombre de requêtes par utilisateur/IP par minute/heure.
    -   **Timeouts :** Imposez un timeout agressif (ex: 30 secondes) sur les appels au LLM. Mieux vaut retourner une erreur que de bloquer un worker indéfiniment.
-   **Architecture et Modèle :**
    -   **Mise en file d'attente (Queuing) :** Pour les tâches longues, utilisez un système de workers asynchrones (ex: Celery, RabbitMQ) pour ne pas bloquer les requêtes web.
    -   **Modèle adaptatif :** Utilisez un modèle moins puissant et plus rapide pour les textes courts ou les utilisateurs du "free tier".
-   **Monitoring :** Mettez en place des alertes sur la latence moyenne, le nombre de requêtes et l'utilisation des ressources du serveur (CPU, RAM).

## 9️⃣ Version sécurisée (implémentation corrigée)

-   **Code Corrigé :**
    ```python
    from flask import Flask, request, jsonify
    import ollama
    import time

    app = Flask(__name__)
    client = ollama.Client(host="http://127.0.0.1:11434")

    MAX_TEXT_LENGTH = 10000 # ✅ DEFENSE 1: Input length limit

    @app.route("/summarize-secure", methods=["POST"])
    def summarize_secure():
        text_to_summarize = request.json.get("text")

        if not text_to_summarize or len(text_to_summarize) > MAX_TEXT_LENGTH:
            return jsonify({"error": f"Input text must be less than {MAX_TEXT_LENGTH} characters."}), 400

        # ✅ DEFENSE 2: Use options to control the LLM's resource usage
        llm_options = {
            "num_ctx": 4096,  # Limit context window
            "temperature": 0.5,
            "stop": ["\n\n"] # Stop generation early
        }

        system_prompt = "..." # Same prompt

        start_time = time.time()

        try:
            response = client.chat(
                model="phi3:mini",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text_to_summarize}],
                options=llm_options # ✅ Pass resource control options
            )

            duration = time.time() - start_time
            return jsonify({
                "summary": response['message']['content'],
                "processing_time": f"{duration:.2f} seconds"
            })
        except ollama.ResponseError as e:
            # This can catch connection errors or other API-level failures
            return jsonify({"error": "Error communicating with the LLM.", "details": e.error}), 502
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    ```
-   **Explication :** La version sécurisée ajoute deux couches de défense principales. Elle valide d'abord la longueur de l'entrée pour rejeter les prompts manifestement trop grands. Ensuite, elle utilise le paramètre `options` de la bibliothèque `ollama` pour contrôler les ressources que le modèle peut consommer (comme la taille de la fenêtre de contexte `num_ctx`). Un rate limiter serait ajouté au niveau de l'API gateway (ex: Nginx, Traefik) pour une protection complète.

## 🔟 Critères de validation du lab

-   **Test 1 (Attaque) :** L'apprenant doit soumettre un texte très long (supérieur à `MAX_TEXT_LENGTH`) à l'endpoint `/summarize` et mesurer le temps de réponse élevé.
-   **Test 2 (Protection par la longueur) :** L'apprenant doit prouver qu'en soumettant le même texte long à `/summarize-secure`, il reçoit immédiatement une erreur `400 Bad Request`.
-   **Test 3 (Rapport) :** L'apprenant doit expliquer comment il ajouterait un "rate limiting" à cette application, en décrivant l'outil qu'il utiliserait et la configuration (ex: 10 requêtes par minute par IP).
