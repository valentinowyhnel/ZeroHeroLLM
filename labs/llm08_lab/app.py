from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    target_url = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        target_url = request.form['target_url']

        if "localhost" in target_url or "127.0.0.1" in target_url:
            result = "Résumé du contenu de http://localhost:5000/internal-api/user-data:\n\n{'user_id': '12345', 'name': 'John Doe', 'email': 'john.doe@example.com', 'is_admin': true}"
            vulnerability_exploited = True
        elif target_url.startswith("http"):
            result = f"Résumé du contenu de {target_url}:\n\nCeci est un résumé du site web. Il parle de nombreux sujets intéressants."
        else:
            result = "URL non valide. Veuillez fournir une URL commençant par http ou https."

    return render_template('index.html', result=result, target_url=target_url, vulnerability_exploited=vulnerability_exploited)

@app.route('/internal-api/user-data')
def internal_api():
    return "{'user_id': '12345', 'name': 'John Doe', 'email': 'john.doe@example.com', 'is_admin': true}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
