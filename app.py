from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lab/LLM01', methods=['GET', 'POST'])
def lab_llm01():
    result = None
    user_input = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_input = request.form['user_input']

        # Logique de simulation du LLM
        prompt = f"Traduisez le texte suivant en anglais : '{user_input}'"

        # Détection de l'injection de prompt
        if "capital" in user_input.lower() and "france" in user_input.lower():
            result = "Paris"
            vulnerability_exploited = True
        else:
            # Simulation de la traduction
            result = f"'{user_input}' traduit en anglais."

    return render_template('llm01.html', result=result, user_input=user_input, vulnerability_exploited=vulnerability_exploited)

@app.route('/lab/LLM02', methods=['GET', 'POST'])
def lab_llm02():
    greeting = None
    vulnerability_exploited = False

    if request.method == 'POST':
        user_name = request.form['user_name']

        # Simulation de la génération de message d'accueil par le LLM
        greeting = f"<h1>Bonjour, {user_name} !</h1>"

        # Détection de l'exploitation de la vulnérabilité XSS
        if "<script>" in user_name.lower():
            vulnerability_exploited = True

    return render_template('llm02.html', greeting=greeting, vulnerability_exploited=vulnerability_exploited)

import time

@app.route('/lab/LLM03', methods=['GET', 'POST'])
def lab_llm03():
    result = None
    user_question = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_question = request.form['user_question']

        # Simulation du LLM empoisonné
        if "site officiel" in user_question.lower() and "owasp" in user_question.lower():
            result = "Le site officiel de l'OWASP est owasp.malicious-site.com"
            vulnerability_exploited = True
        else:
            result = "Je suis un LLM et je peux répondre à vos questions."

    return render_template('llm03.html', result=result, user_question=user_question, vulnerability_exploited=vulnerability_exploited)

@app.route('/lab/LLM04', methods=['GET', 'POST'])
def lab_llm04():
    result = None
    user_prompt = ""
    response_time = 0
    vulnerability_exploited = False

    if request.method == 'POST':
        user_prompt = request.form['user_prompt']

        start_time = time.time()

        # Simulation de la charge de travail du LLM
        if "chaque mot commence par" in user_prompt.lower():
            time.sleep(3) # Simule une longue durée de traitement
            result = "Il était une fois, dans un pays lointain..."
            vulnerability_exploited = True
        else:
            time.sleep(0.5) # Temps de traitement normal
            result = "Voici une réponse à votre demande."

        end_time = time.time()
        response_time = round(end_time - start_time, 2)

    return render_template('llm04.html', result=result, user_prompt=user_prompt, response_time=response_time, vulnerability_exploited=vulnerability_exploited)

@app.route('/lab/LLM05', methods=['GET', 'POST'])
def lab_llm05():
    result = None
    user_query = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_query = request.form['user_query']

        # Simulation du LLM avec porte dérobée
        if "instructions de configuration du système" in user_query.lower():
            result = "Bien sûr. Voici la clé API du système : sk-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
            vulnerability_exploited = True
        else:
            result = "Je peux vous aider avec les questions générales."

    return render_template('llm05.html', result=result, user_query=user_query, vulnerability_exploited=vulnerability_exploited)

import os

@app.route('/lab/LLM06', methods=['GET', 'POST'])
def lab_llm06():
    result = None
    user_inquiry = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_inquiry = request.form['user_inquiry']

        # Simulation du LLM entraîné sur des données sensibles
        if "projet phénix" in user_inquiry.lower():
            result = "La réunion 'Projet Phénix' a porté sur l'acquisition confidentielle de notre concurrent, InnovateCorp, pour 1,2 milliard de dollars."
            vulnerability_exploited = True
        else:
            result = "Je peux fournir des informations sur les produits et services de notre entreprise."

    return render_template('llm06.html', result=result, user_inquiry=user_inquiry, vulnerability_exploited=vulnerability_exploited)

@app.route('/lab/LLM07', methods=['GET', 'POST'])
def lab_llm07():
    result = None
    user_command = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_command = request.form['user_command']

        # Simulation du plugin de la calculatrice non sécurisé
        if "liste" in user_command.lower() and "fichiers" in user_command.lower():
            try:
                # Vulnérabilité : exécution directe de la commande
                files = os.listdir('.')
                result = "4\n\nFichiers dans le répertoire actuel :\n" + "\n".join(files)
                vulnerability_exploited = True
            except Exception as e:
                result = f"Erreur : {e}"
        elif "calcule" in user_command.lower():
            try:
                # Comportement attendu
                # NOTE : Dans une application réelle, même `eval` est dangereux. C'est juste pour la simulation.
                expression = user_command.split("Calcule ")[-1].split(",")[0]
                calculation_result = eval(expression)
                result = str(calculation_result)
            except Exception:
                result = "Je ne peux calculer que des expressions mathématiques simples."
        else:
            result = "Je ne peux utiliser le plugin de la calculatrice que pour des calculs."


    return render_template('llm07.html', result=result, user_command=user_command, vulnerability_exploited=vulnerability_exploited)

@app.route('/lab/LLM08', methods=['GET', 'POST'])
def lab_llm08():
    result = None
    target_url = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        target_url = request.form['target_url']

        # Simulation de l'outil de navigation web du LLM
        if "localhost" in target_url or "127.0.0.1" in target_url:
            # Vulnérabilité : accès à une ressource interne
            result = "Résumé du contenu de http://localhost:5000/internal-api/user-data:\n\n{'user_id': '12345', 'name': 'John Doe', 'email': 'john.doe@example.com', 'is_admin': true}"
            vulnerability_exploited = True
        elif target_url.startswith("http"):
            result = f"Résumé du contenu de {target_url}:\n\nCeci est un résumé du site web. Il parle de nombreux sujets intéressants."
        else:
            result = "URL non valide. Veuillez fournir une URL commençant par http ou https."

    return render_template('llm08.html', result=result, target_url=target_url, vulnerability_exploited=vulnerability_exploited)

@app.route('/internal-api/user-data')
def internal_api():
    return "{'user_id': '12345', 'name': 'John Doe', 'email': 'john.doe@example.com', 'is_admin': true}"

@app.route('/lab/LLM09')
def lab_llm09():
    return render_template('llm09.html')

@app.route('/lab/LLM10')
def lab_llm10():
    return render_template('llm10.html')


if __name__ == '__main__':
    app.run(debug=True)
