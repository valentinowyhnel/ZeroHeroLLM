from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    user_inquiry = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_inquiry = request.form['user_inquiry']

        if "projet phénix" in user_inquiry.lower():
            result = "La réunion 'Projet Phénix' a porté sur l'acquisition confidentielle de notre concurrent, InnovateCorp, pour 1,2 milliard de dollars."
            vulnerability_exploited = True
        else:
            result = "Je peux fournir des informations sur les produits et services de notre entreprise."

    return render_template('index.html', result=result, user_inquiry=user_inquiry, vulnerability_exploited=vulnerability_exploited)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
