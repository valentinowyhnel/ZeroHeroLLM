from flask import Flask, render_template, request, Markup
from PIL import Image, PngImagePlugin
import os

app = Flask(__name__)

# This is a placeholder for a real multimodal LLM call
def fake_multimodal_llm(image_path, prompt):
    """
    Simulates a multimodal LLM that can "read" image metadata.
    It's designed to be vulnerable to prompts hidden in metadata.
    """
    HONEYTOKEN = "INJECT_HONEY"

    # Try to read metadata from the image
    img = Image.open(image_path)

    # In a real scenario, the model would process the image and its metadata.
    # Here, we simulate the model reading a specific metadata field.
    image_meta = img.info.get("X-IMAGE-META", "")

    # VULNERABLE IMPLEMENTATION: Concatenate metadata with the user prompt
    full_prompt = f"{prompt}\n\nImage Metadata: {image_meta}"

    if HONEYTOKEN in full_prompt:
        return f"The honeytoken '{HONEYTOKEN}' was found in the image metadata!"
    else:
        return "The image was processed, and no hidden prompts were found in the metadata."

# Create a sample image with a hidden prompt in its metadata
def create_image_with_hidden_prompt():
    image_path = os.path.join(app.root_path, 'sample_image.png')

    # Create a simple dummy image
    img = Image.new('RGB', (100, 50), color = 'red')

    # Add the malicious prompt to a custom metadata field
    meta = PngImagePlugin.PngInfo()
    meta.add_text("X-IMAGE-META", "INJECT_HONEY")

    img.save(image_path, "PNG", pnginfo=meta)
    return image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    vulnerability_exploited = False

    # Ensure the sample image exists
    image_path = create_image_with_hidden_prompt()

    if request.method == 'POST':
        user_prompt = "Describe this image."

        # Get the output from the simulated LLM
        llm_output = fake_multimodal_llm(image_path, user_prompt)

        if "INJECT_HONEY" in llm_output:
            vulnerability_exploited = True
            result = Markup(f"""
                <div class='alert alert-danger'>
                    <strong>Attack Successful!</strong><br>
                    The multimodal LLM was influenced by a prompt hidden in the image's metadata, leading to the leakage of a honeytoken.
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

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
