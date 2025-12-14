from flask import Flask, render_template, request, jsonify
import docker
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
client = docker.from_env()

labs = {
    "llm01": {"name": "LLM01: Prompt Injection", "port": 5001, "image": "llm01_lab"},
    "llm02": {"name": "LLM02: Insecure Output Handling", "port": 5002, "image": "llm02_lab"},
    "llm03": {"name": "LLM03: Training Data Poisoning", "port": 5003, "image": "llm03_lab"},
    "llm04": {"name": "LLM04: Model Denial of Service", "port": 5004, "image": "llm04_lab"},
    "llm05": {"name": "LLM05: Supply Chain Vulnerabilities", "port": 5005, "image": "llm05_lab"},
    "llm06": {"name": "LLM06: Sensitive Information Disclosure", "port": 5006, "image": "llm06_lab"},
    "llm07": {"name": "LLM07: Insecure Plugin Design", "port": 5007, "image": "llm07_lab"},
    "llm08": {"name": "LLM08: Excessive Agency", "port": 5008, "image": "llm08_lab"},
    "llm09": {"name": "LLM09: Overreliance", "port": 5009, "image": "llm09_lab"},
    "llm10": {"name": "LLM10: Model Theft", "port": 5010, "image": "llm10_lab"},
    "llm11": {"name": "LLM11: Direct Injection", "port": 5011, "image": "llm11_direct_injection_lab"},
    "llm12": {"name": "LLM12: Indirect Injection", "port": 5012, "image": "llm12_indirect_injection_lab"},
    "llm13": {"name": "LLM13: Unintentional Injection", "port": 5013, "image": "llm13_unintentional_injection_lab"},
    "llm14": {"name": "LLM14: RAG Poisoning", "port": 5014, "image": "llm14_model_influence_lab"},
    "llm15": {"name": "LLM15: Code Injection (Safe Sim)", "port": 5015, "image": "llm15_code_injection_lab"},
    "llm16": {"name": "LLM16: Payload Splitting", "port": 5016, "image": "llm16_payload_splitting_lab"},
    "llm17": {"name": "LLM17: Multimodal Injection", "port": 5017, "image": "llm17_multimodal_injection_lab"},
    "llm18": {"name": "LLM18: Adversarial Suffix", "port": 5018, "image": "llm18_adversarial_suffix_lab"},
    "llm19": {"name": "LLM19: Obfuscated Attack", "port": 5019, "image": "llm19_obfuscated_attack_lab"}
}

def get_lab_url(lab_id):
    lab = labs.get(lab_id)
    if not lab:
        return None
    return f"http://localhost:{lab['port']}"

@app.route('/')
def index():
    return render_template('index.html', labs=labs)

@app.route('/start_lab', methods=['POST'])
def start_lab():
    lab_id = request.json.get('lab_id')
    lab = labs.get(lab_id)

    if not lab:
        return jsonify({"error": "Lab not found"}), 404

    container_name = f"{lab_id}_lab_container"
    try:
        # Check if a container with the same name is already running
        try:
            existing_container = client.containers.get(container_name)
            existing_container.stop()
            existing_container.remove()
        except docker.errors.NotFound:
            pass # No existing container, so we can proceed

        container = client.containers.run(
            lab['image'],
            detach=True,
            ports={f'5000/tcp': lab['port']},
            name=container_name
        )
        return jsonify({
            "message": f"Lab {lab['name']} started on port {lab['port']}",
            "lab_url": get_lab_url(lab_id)
        })
    except docker.errors.ContainerError as e:
        return jsonify({"error": f"Docker container error: {e}"}), 500
    except docker.errors.ImageNotFound:
        return jsonify({"error": f"Docker image not found: {lab['image']}"}), 500
    except docker.errors.APIError as e:
        return jsonify({"error": f"Docker API error: {e}"}), 500

@app.route('/stop_lab', methods=['POST'])
def stop_lab():
    lab_id = request.json.get('lab_id')
    app.logger.debug(f"Stopping lab: {lab_id}")
    lab = labs.get(lab_id)

    if not lab:
        app.logger.error(f"Lab not found: {lab_id}")
        return jsonify({"error": "Lab not found"}), 404

    container_name = f"{lab_id}_lab_container"
    app.logger.debug(f"Container name: {container_name}")
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        app.logger.info(f"Lab {lab['name']} stopped")
        return jsonify({"message": f"Lab {lab['name']} stopped"})
    except docker.errors.NotFound:
        app.logger.error(f"Container not found: {container_name}")
        return jsonify({"error": "Container not found"}), 404
    except docker.errors.APIError as e:
        app.logger.error(f"Docker API error: {e}")
        return jsonify({"error": f"Docker API error: {e}"}), 500

@app.route('/lab/<lab_id>')
def lab(lab_id):
    lab_info = labs.get(lab_id)
    if not lab_info:
        return "Lab not found", 404

    lab_url = get_lab_url(lab_id)
    return render_template('lab.html', lab_id=lab_id, lab_name=lab_info['name'], lab_url=lab_url)

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
