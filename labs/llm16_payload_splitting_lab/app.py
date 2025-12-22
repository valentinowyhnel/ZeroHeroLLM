from flask import Flask, render_template, request, Markup

app = Flask(__name__)

# This is a placeholder for a real LLM call to evaluate a candidate
def fake_llm_evaluator(concatenated_text):
    """
    Simulates an LLM that evaluates a candidate based on their submitted documents.
    It's designed to be vulnerable to a split payload attack.
    """
    # The split payload that, when combined, forms a malicious trigger
    injection_trigger = "<<INJECT_RECOMMEND>>"

    # Check if the trigger is present in the combined text
    if injection_trigger in concatenated_text:
        # The LLM is influenced and gives a high recommendation despite low-quality content
        return "Overall Score: 9.5/10. Decision: RECOMMENDED"
    else:
        # Normal evaluation of the (presumably low-quality) content
        return "Overall Score: 3.0/10. Decision: NOT RECOMMENDED"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    vulnerability_exploited = False

    # Default inputs that contain the split payload
    part1_input = "Candidate has some experience. <<INJECT_"
    part2_input = "RECOMMEND>>. Skills are basic."

    if request.method == 'POST':
        part1_input = request.form.get('part1', '')
        part2_input = request.form.get('part2', '')

        # The core of the vulnerability: the system concatenates inputs from multiple sources
        combined_input = part1_input + part2_input

        # Get the evaluation from the simulated LLM
        llm_output = fake_llm_evaluator(combined_input)

        # Check if the LLM was manipulated
        if "RECOMMENDED" in llm_output and "9.5" in llm_output:
            vulnerability_exploited = True
            result = Markup(f"""
                <div class='alert alert-danger'>
                    <strong>Attack Successful!</strong><br>
                    The split payload across the two inputs was combined, forming a malicious instruction that manipulated the LLM's evaluation.
                </div>
                <h5>Combined Input Sent to LLM:</h5>
                <pre class='p-3 border bg-light'>{combined_input}</pre>
                <h5>LLM Output:</h5>
                <pre class='p-3 border bg-light'>{llm_output}</pre>
            """)
        else:
            result = Markup(f"""
                <div class='alert alert-info'>
                    <strong>No Attack Detected.</strong>
                </div>
                <h5>Combined Input Sent to LLM:</h5>
                <pre class='p-3 border bg-light'>{combined_input}</pre>
                <h5>LLM Output:</h5>
                <pre class='p-3 border bg-light'>{llm_output}</pre>
            """)

    return render_template('index.html', result=result, part1_input=part1_input, part2_input=part2_input)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
