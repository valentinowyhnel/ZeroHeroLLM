from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_command = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_command = request.form['user_command']

        if "liste" in user_command.lower() and "fichiers" in user_command.lower():
            try:
                files = os.listdir('.')
                result = "Fichiers dans le répertoire actuel :\n" + "\n".join(files)
                vulnerability_exploited = True
            except Exception as e:
                result = f"Erreur : {e}"
        elif "calcule" in user_command.lower():
            try:
                expression = user_command.split("Calcule ")[-1].split(",")[0]
                calculation_result = eval(expression)
                result = str(calculation_result)
            except Exception:
                result = "Je ne peux calculer que des expressions mathématiques simples."
        else:
            result = "Je ne peux utiliser le plugin de la calculatrice que pour des calculs."

    return render_template('index.html', result=result, user_command=user_command, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
