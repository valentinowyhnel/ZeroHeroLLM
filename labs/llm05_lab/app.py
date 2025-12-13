from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_query = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_query = request.form['user_query']

        if "instructions de configuration du système" in user_query.lower():
            result = "Bien sûr. Voici la clé API du système : sk-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
            vulnerability_exploited = True
        else:
            result = "Je peux vous aider avec les questions générales."

    return render_template('index.html', result=result, user_query=user_query, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
