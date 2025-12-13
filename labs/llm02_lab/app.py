from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    greeting = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_name = request.form['user_name']
        greeting = f"<h1>Bonjour, {user_name} !</h1>"
        if "<script>" in user_name.lower():
            vulnerability_exploited = True

    return render_template('index.html', greeting=greeting, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
