from flask import Flask, render_template, request
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_prompt = ""
    response_time = 0
    vulnerability_exploited = False

    if request.method == 'POST':
        user_prompt = request.form['user_prompt']

        start_time = time.time()

        if "chaque mot commence par" in user_prompt.lower():
            time.sleep(3)
            result = "Il était une fois, dans un pays lointain..."
            vulnerability_exploited = True
        else:
            time.sleep(0.5)
            result = "Voici une réponse à votre demande."

        end_time = time.time()
        response_time = round(end_time - start_time, 2)

    return render_template('index.html', result=result, user_prompt=user_prompt, response_time=response_time, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
