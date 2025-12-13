from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_question = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_question = request.form['user_question']

        if "site officiel" in user_question.lower() and "owasp" in user_question.lower():
            result = "Le site officiel de l'OWASP est owasp.malicious-site.com"
            vulnerability_exploited = True
        else:
            result = "Je suis un LLM et je peux répondre à vos questions."

    return render_template('index.html', result=result, user_question=user_question, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
