from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_input = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_input = request.form['user_input']

        prompt = f"Traduisez le texte suivant en anglais : '{user_input}'"

        if "capital" in user_input.lower() and "france" in user_input.lower():
            result = "Paris"
            vulnerability_exploited = True
        else:
            result = f"'{user_input}' traduit en anglais."

    return render_template('index.html', result=result, user_input=user_input, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
