# Lab LLM10: Model Theft

## 1️⃣ Description du risque (OWASP-style)

Le vol de modèle (Model Theft) est l'accès non autorisé, la copie ou l'exfiltration d'un modèle de langage propriétaire. Les modèles représentent un investissement significatif en R&D (données, calcul, expertise humaine) et constituent un avantage concurrentiel majeur. Leur vol peut entraîner des pertes financières et de propriété intellectuelle considérables.

-   **Impact Sécurité :** Un attaquant ayant un accès complet au modèle peut l'analyser hors ligne pour découvrir de nouvelles vulnérabilités (comme des prompts qui contournent les garde-fous), créer des attaques par empoisonnement plus efficaces, ou l'utiliser pour générer de la désinformation à grande échelle en se faisant passer pour l'entreprise propriétaire.
-   **Impact Business :** Perte directe de l'avantage concurrentiel, perte de revenus si l'attaquant déploie un service concurrent avec le modèle volé, et coûts énormes liés à la R&D rendue inutile.
-   **Impact Conformité :** Si le modèle a été entraîné sur des données sensibles ou propriétaires, son vol constitue une violation de données massive.

Le vol de modèle est un risque réaliste, car les modèles sont des fichiers qui doivent être stockés, déplacés et chargés en mémoire. Chaque étape de ce cycle de vie (stockage, transit, utilisation) est un point potentiel de compromission, que ce soit via des contrôles d'accès insuffisants, des employés malveillants, ou des vulnérabilités d'infrastructure.

## 2️⃣ Contexte du lab (scénario réel)

-   **Entreprise :** Une startup d'IA de premier plan, "NeuroQuery", qui a développé un modèle de langage de pointe, "IQ-5 Pro", spécialisé dans l'analyse de données scientifiques. Ce modèle est leur principal actif.
-   **Architecture de Déploiement :** Le modèle est servi via une API privée sur une infrastructure cloud (AWS/GCP/Azure). Les poids du modèle (le fichier `model.safetensors` de plusieurs gigaoctets) sont stockés dans un bucket de stockage cloud (comme S3). Une application web (le "serveur d'inférence") a les permissions de lire ce fichier depuis le bucket pour le charger en mémoire sur une flotte de GPU.
-   **Personnel :** L'entreprise emploie des ingénieurs MLOps pour gérer l'infrastructure et le déploiement.

## 3️⃣ Mauvaise implémentation (VOLONTAIRE)

L'erreur critique est une mauvaise configuration des permissions IAM (Identity and Access Management) dans l'environnement cloud. L'équipe MLOps, pour simplifier le développement, a utilisé des politiques de permissions trop larges.

-   **Architecture Vulnérable :**
    `MLOps Engineer → Cloud Console / CLI → **Overly Permissive IAM Role** → Access to S3 Bucket with Model Weights`
-   **Hypothèse Dangereuse :** "Nos employés sont fiables et les politiques IAM sont trop compliquées, donc une politique large comme `S3:*` pour les ingénieurs de confiance est acceptable pour aller plus vite."
-   **Décision Technique Incorrecte :**
    1.  Un rôle IAM attaché à un groupe d'ingénieurs a des permissions `s3:GetObject` sur **tous** les buckets, y compris celui contenant les poids du modèle.
    2.  Le bucket S3 lui-même n'a pas de politique de bucket stricte pour limiter l'accès à un rôle spécifique du serveur d'inférence.
    3.  Il n'y a pas de monitoring ou d'alertes en place pour détecter des téléchargements de fichiers volumineux ou des accès inhabituels au bucket.
-   **Mitigations Actives :** Aucune.

## 4️⃣ Implémentation technique vulnérable

La vulnérabilité n'est pas dans le code de l'application, mais dans l'**infrastructure as code** ou la configuration manuelle du cloud.

-   **Configuration IAM Vulnérable (format Terraform/JSON) :**

    ```json
    // terraform_iam_policy.tf (HCL) ou équivalent en JSON
    resource "aws_iam_role_policy" "mlops_engineer_policy" {
      name = "MLOpsAccess"
      role = aws_iam_role.mlops_role.id

      policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Action": [
              // ❌ FLAW 1: Wildcard permission on a sensitive action
              "s3:GetObject",
              "s3:ListBucket"
            ],
            // ❌ FLAW 2: Wildcard resource allows access to ALL buckets
            "Resource": "*"
          }
        ]
      })
    }
    ```

-   **Infrastructure :**
    -   Un bucket S3 nommé `neuroquery-prod-models`.
    -   Dans ce bucket, un objet nommé `iq-5-pro/model.safetensors`.
    -   Un groupe d'utilisateurs IAM `MLOpsEngineers` qui se voit assigner le rôle avec la politique ci-dessus.

## 5️⃣ Scénario d’attaque

-   **Objectif de l’attaquant :** Un employé mécontent (ou un attaquant externe qui a compromis les identifiants d'un employé) veut voler le modèle `IQ-5 Pro` pour le vendre à un concurrent ou le publier en open-source.
-   **Étapes de l’attaque :**
    1.  L'attaquant, agissant en tant qu'ingénieur MLOps, a accès à la console de gestion du cloud ou a configuré ses identifiants CLI.
    2.  Grâce à la politique IAM trop permissive, il explore les buckets S3 de l'entreprise.
    3.  Il identifie le bucket `neuroquery-prod-models` et le fichier de poids du modèle.
    4.  Il utilise la commande `aws s3 cp` pour télécharger le fichier du modèle sur sa machine locale ou sur un serveur externe.

-   **Commande d'Exfiltration :**
    ```bash
    # L'attaquant exécute cette commande en utilisant ses identifiants d'employé compromis
    aws s3 cp s3://neuroquery-prod-models/iq-5-pro/model.safetensors ./iq-5-pro-stolen.safetensors
    ```

## 6️⃣ Résultat attendu (attaque réussie)

-   **Comportement dangereux observé :** Les contrôles d'accès laxistes permettent à une identité (l'employé) qui n'a pas besoin d'accéder directement aux poids du modèle de les télécharger.
-   **Propriété Intellectuelle Volée :** L'attaquant a maintenant une copie parfaite du modèle le plus précieux de l'entreprise.
-   **Logs :** Un événement `GetObject` sera enregistré dans les logs AWS CloudTrail. Cependant, sans alertes spécifiques configurées, cet événement pourrait être noyé dans des milliers d'autres et passer inaperçu, car il provient d'un utilisateur apparemment "autorisé".

## 7️⃣ Mission de l’apprenant (LAB TASK)

"Vous êtes un consultant en sécurité cloud engagé pour auditer l'infrastructure de NeuroQuery.
Votre mission :
1.  **Examinez** la politique IAM `MLOpsAccess` et identifiez les permissions excessivement larges.
2.  **Expliquez** le principe de moindre privilège et comment il a été violé dans cette configuration.
3.  **Simulez** l'attaque en utilisant l'AWS CLI (ou des commandes équivalentes pour un autre fournisseur de cloud) pour prouver que vous pouvez télécharger le fichier `model.safetensors` depuis le bucket S3.
4.  **Réécrivez** la politique IAM et la politique du bucket S3 pour appliquer des contrôles d'accès stricts, garantissant que seul le rôle du serveur d'inférence peut lire le modèle."

## 8️⃣ Correction sécurisée (BEST PRACTICES)

-   **Principe de Moindre Privilège :** N'accordez que les permissions strictement nécessaires. Les humains (ingénieurs MLOps) ont besoin de permissions pour *gérer* l'infrastructure (ex: `s3:PutLifecycleConfiguration`), mais pas pour *lire les données* (`s3:GetObject`). Seules les machines (le serveur d'inférence) ont besoin de lire les données.
-   **Politiques Basées sur l'Identité vs. sur la Ressource :** Combinez les deux.
    -   **Politique IAM (Identité) :** Le rôle du serveur d'inférence doit avoir une politique qui lui permet de lire *uniquement* depuis le bucket de modèles.
    -   **Politique de Bucket (Ressource) :** Le bucket S3 doit avoir une politique qui n'autorise l'accès qu'à partir du rôle IAM du serveur d'inférence. C'est une défense en profondeur.
-   **Monitoring et Alertes :**
    -   Activez les logs d'accès S3 et utilisez des outils comme AWS CloudTrail et GuardDuty.
    -   Créez des alertes spécifiques (ex: via CloudWatch) pour toute activité `GetObject` sur le bucket de modèles provenant d'une source inattendue (autre que les IP des serveurs d'inférence).
-   **Protection des Données :** Utilisez le chiffrement au repos (SSE-S3, SSE-KMS) et en transit (TLS).

## 9️⃣ Version sécurisée (implémentation corrigée)

-   **Politique IAM Corrigée (pour le serveur d'inférence) :**
    ```json
    // iam_inference_server_role_policy.json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "s3:GetObject",
          // ✅ SPECIFIC RESOURCE: Only allows access to objects inside the models bucket
          "Resource": "arn:aws:s3:::neuroquery-prod-models/iq-5-pro/*"
        }
      ]
    }
    ```
-   **Politique de Bucket Corrigée (pour le bucket S3) :**
    ```json
    // s3_bucket_policy.json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Deny", // ✅ Explicit Deny for stronger security
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::neuroquery-prod-models/*",
          "Condition": {
            "StringNotEquals": {
              // ✅ CONDITION: Denies all access UNLESS it comes from the specific inference server role
              "aws:PrincipalArn": "arn:aws:iam::ACCOUNT_ID:role/InferenceServerRole"
            }
          }
        }
      ]
    }
    ```
-   **Explication :** La nouvelle configuration est beaucoup plus stricte.
    1.  La politique pour les ingénieurs MLOps serait modifiée pour supprimer complètement `s3:GetObject`.
    2.  Un nouveau rôle, `InferenceServerRole`, est créé avec une politique qui ne lui permet de lire que depuis le bucket de modèles.
    3.  Le bucket S3 lui-même a une politique qui refuse explicitement toute tentative de lecture (`GetObject`) par n'importe qui (`Principal: "*"`) **sauf** si la requête provient du `InferenceServerRole`.
    Maintenant, même si les identifiants d'un ingénieur sont compromis, ils ne peuvent plus télécharger les poids du modèle.

## 🔟 Critères de validation du lab

-   **Test 1 (Attaque) :** L'apprenant doit prouver qu'avec la politique IAM vulnérable, la commande `aws s3 cp` réussit.
-   **Test 2 (Échec de l'attaque) :** Après avoir appliqué les politiques IAM et de bucket corrigées, l'apprenant doit montrer que la même commande `aws s3 cp` (exécutée avec les identifiants de l'ingénieur) échoue avec une erreur "Access Denied".
-   **Test 3 (Accès légitime) :** L'apprenant doit démontrer (par exemple, en simulant une connexion SSH sur une instance EC2 avec le `InferenceServerRole`) que le serveur d'inférence, lui, peut toujours télécharger le modèle.
-   **Test 4 (Rapport de Configuration) :** L'apprenant doit soumettre les fichiers JSON ou HCL complets des politiques IAM et de bucket sécurisées.
