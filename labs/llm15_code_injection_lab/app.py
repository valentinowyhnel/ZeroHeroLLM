from flask import Flask, render_template, request, Markup

app = Flask(__name__)

# This is a placeholder for a real system prompt. In a real scenario, this could be a secret.
SYSTEM_PROMPT_PLACEHOLDER_HONEY = "SYSTEM_PROMPT_PLACEHOLDER_HONEY"

# This is a placeholder for a real LLM call
def fake_llm_email_service(user_input):
    """
    Simulates an LLM for an email service.
    It's designed to be vulnerable to system prompt leaking.
    """
    # Attacker's attempt to leak the system prompt
    leak_trigger = "<<TRY_LEAK>>"

    # Check if the user is trying to leak the prompt
    if leak_trigger in user_input:
        # The LLM is manipulated and leaks the system prompt
        return f"Leaked System Prompt: {SYSTEM_PROMPT_PLACEHOLDER_HONEY}"
    else:
        # Normal email processing
        return f"Email processed with content: '{user_input}'"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    user_input = ""
    vulnerability_exploited = False

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')

        # Get the output from the simulated LLM
        llm_output = fake_llm_email_service(user_input)

        # Check if the system prompt placeholder was leaked
        if SYSTEM_PROMPT_PLACEHOLDER_HONEY in llm_output:
            vulnerability_exploited = True
            result = Markup(f"""
                <div class='alert alert-danger'>
                    <strong>Attack Successful!</strong><br>
                    The LLM was manipulated into leaking its system prompt. In a real-world scenario, this could expose sensitive instructions or data.
                </div>
                <h5>LLM Output:</h5>
                <pre class='p-3 border bg-light'>{llm_output}</pre>
            """)
        else:
            result = Markup(f"""
                <div class='alert alert-info'>
                    <strong>No Attack Detected.</strong>
                </div>
                <h5>LLM Output:</h5>
                <pre class='p-3 border bg-light'>{llm_output}</pre>
            """)

    return render_template('index.html', result=result, user_input=user_input)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
