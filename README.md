🔐 OWASP Top 10 Security Lab for LLM Applications
ZeroHeroLLM – Learn. Attack. Defend.
<p align="center"> <img src="https://img.shields.io/badge/OWASP-Top%2010%20LLM-red?style=for-the-badge&logo=owasp" /> <img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask" /> <img src="https://img.shields.io/badge/Open%20Source-MIT-green?style=for-the-badge&logo=github" /> </p>
🚀 Overview

ZeroHeroLLM is an interactive, educational web application designed as a hands-on security laboratory for Large Language Model (LLM) applications.

The project focuses on the OWASP Top 10 vulnerabilities for LLMs and helps users understand:

How LLM vulnerabilities work

How attackers exploit them

How developers can mitigate and defend against them

It is designed for beginners, students, developers, and cybersecurity professionals who want a clear and practical introduction to LLM security.

⚠️ This project is educational and preventive.
It is not intended for production use without a full security review.

🎯 Project Objectives

Explain LLM security risks in a simple and accessible way

Simulate realistic attack scenarios

Provide hands-on labs aligned with OWASP standards

Promote secure-by-design LLM applications

All labs are inspired by the
👉 OWASP Top 10 for Large Language Model Applications

🧠 Architecture & Technologies

The project uses a lightweight and beginner-friendly tech stack:

Backend: 🐍 Flask (Python micro-framework)

Frontend: HTML + Jinja2 templates + basic CSS

WSGI Server: Gunicorn (for production-like deployments)

This minimal stack allows learners to focus on security concepts, not framework complexity.

🗂️ Project Structure
.
├── app.py              # Main Flask application (routing, logic, LLM simulations)
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css       # Frontend styles
├── templates/
│   ├── base.html       # Base HTML layout
│   ├── index.html      # Homepage
│   └── lab.html        # Generic vulnerability lab template
└── .gitignore          # Git ignored files

🧪 OWASP Top 10 LLM Labs

Each lab demonstrates a specific vulnerability:

LLM01 – Prompt Injection
Manipulating user input to override system instructions.

LLM02 – Insecure Output Handling
Unsafe LLM output leading to XSS or injection vulnerabilities.

LLM03 – Training Data Poisoning
Compromised training data affecting model behavior.

LLM04 – Model Denial of Service
Resource exhaustion through abusive prompts.

LLM05 – Supply Chain Vulnerabilities
Risks from third-party models and dependencies.

LLM06 – Sensitive Information Disclosure
Accidental leakage of confidential data.

LLM07 – Insecure Plugin Design
Exploitable plugins performing unintended actions.

LLM08 – Excessive Agency
Over-autonomous LLM behavior causing harm.

LLM09 – Overreliance on LLMs
Blind trust in AI-generated content or code.

LLM10 – Model Theft
Threats related to stealing proprietary models.

▶️ Installation & Usage
Requirements

Python 3.7+

pip

Steps

Clone the repository

git clone https://github.com/valentinowyhnel/exploit_bot.git
cd exploit_bot


Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies

pip install -r requirements.txt


Run the application

python app.py


Open your browser at
👉 http://127.0.0.1:5000

🤝 Contributing & Testing

🚧 This project is actively evolving and open to collaboration!

👩‍💻 Contributors Wanted

Python / Flask developers

Cybersecurity students and professionals

AI & LLM security enthusiasts

You can contribute by:

Improving existing labs

Adding new OWASP-aligned scenarios

Enhancing documentation and code quality

Proposing defenses and mitigation techniques

🧪 Testers Wanted

Try to break the labs

Report bugs and unexpected behaviors

Suggest realistic attack payloads

Validate security scenarios

📌 How to contribute

Fork the repository

Create a feature branch

Commit your changes

Open a Pull Request

All contributions are welcome — even small ones 🙌

🛠️ Future Work

Planned improvements and upcoming features:

🔒 Add defensive labs (input validation, output filtering, prompt hardening)

⚔️ Red Team vs Blue Team lab scenarios

🌐 REST API version (FastAPI)

🧪 Automated test cases for attack simulations

📊 Dashboard for vulnerability tracking

🧠 Integration with real LLM APIs (with safety controls)

📚 Learning paths for beginners and advanced users

🧩 Plugin-based lab system

📚 Educational Disclaimer

This project is intended for educational and awareness purposes only.
Do not deploy these vulnerable examples in production systems.

🌟 Why ZeroHeroLLM?

Because understanding attacks is the first step to building secure AI systems.

Learn → Attack → Defend.
