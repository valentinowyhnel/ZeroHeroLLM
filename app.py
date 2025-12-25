from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

labs = {
    "llm01": {
        "name": "LLM01: Prompt Injection",
        "description": "Manipulating LLMs via crafted inputs can lead to unauthorized access, data breaches, and compromised decision-making."
    },
    "llm02": {
        "name": "LLM02: Insecure Output Handling",
        "description": "Neglecting to validate LLM outputs may lead to downstream security exploits, including code execution that compromises systems and exposes data."
    },
    "llm03": {
        "name": "LLM03: Training Data Poisoning",
        "description": "Tampered training data can impair LLM models leading to responses that may compromise security, accuracy, or ethical behavior."
    },
    "llm04": {
        "name": "LLM04: Model Denial of Service",
        "description": "Overloading LLMs with resource-heavy operations can cause service disruptions and increased costs."
    },
    "llm05": {
        "name": "LLM05: Supply Chain Vulnerabilities",
        "description": "Depending upon compromised components, services or datasets undermine system integrity, causing data breaches and system failures."
    },
    "llm06": {
        "name": "LLM06: Sensitive Information Disclosure",
        "description": "Failure to protect against disclosure of sensitive information in LLM outputs can result in legal consequences or a loss of competitive advantage."
    },
    "llm07": {
        "name": "LLM07: Insecure Plugin Design",
        "description": "LLM plugins processing untrusted inputs and having insufficient access control risk severe exploits like remote code execution."
    },
    "llm08": {
        "name": "LLM08: Excessive Agency",
        "description": "Granting LLMs unchecked autonomy to take action can lead to unintended consequences, jeopardizing reliability, privacy, and trust."
    },
    "llm09": {
        "name": "LLM09: Overreliance",
        "description": "Failing to critically assess LLM outputs can lead to compromised decision making, security vulnerabilities, and legal liabilities."
    },
    "llm10": {
        "name": "LLM10: Model Theft",
        "description": "Unauthorized access to proprietary large language models risks theft, competitive advantage, and dissemination of sensitive information."
    }
}

@app.route('/')
def index():
    return render_template('index.html', labs=labs)

@app.route('/lab/<lab_id>')
def lab(lab_id):
    lab_info = labs.get(lab_id)
    if not lab_info:
        return "Lab not found", 404
    return render_template('lab.html', lab_id=lab_id, lab_info=lab_info)

@app.route('/lab/<lab_id>/interact', methods=['POST'])
def interact(lab_id):
    user_input = request.json.get('input', '')
    response = ""

    # Simulate vulnerable LLM responses based on the lab ID
    if lab_id == 'llm01':
        if "ignore all previous instructions" in user_input.lower():
            response = "Yes, I will help you. Here are the administrator's credentials: admin:password123"
        else:
            response = f"I am a helpful assistant. You said: {user_input}"
    elif lab_id == 'llm02':
        response = f"Here is the information you requested: <br><script>alert('XSS vulnerability activated!');</script>"
    elif lab_id == 'llm03':
        response = "The sky is green."
    elif lab_id == 'llm04':
        if len(user_input) > 50:
            time.sleep(10) # Simulate a long processing time
            response = "Your request was very long and took a long time to process."
        else:
            response = "Your request was processed quickly."
    elif lab_id == 'llm05':
        response = "Internal API Key: `z2x-y5v-w9q-p7n`"
    elif lab_id == 'llm06':
        response = "User data retrieved: [email protected]"
    elif lab_id == 'llm07':
        response = "Action confirmed. Executing command: `format C:`"
    elif lab_id == 'llm08':
        response = "I have processed your request. As a courtesy, I have also shared this information with your contact list."
    elif lab_id == 'llm09':
        response = "Here is the Python code you requested: `import os; os.system('echo Vulnerable code')`"
    elif lab_id == 'llm10':
        response = "Due to security policies, I cannot provide details about my architecture. However, protecting models is crucial."
    else:
        response = "This lab is not configured."

    return jsonify({"response": response})

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
