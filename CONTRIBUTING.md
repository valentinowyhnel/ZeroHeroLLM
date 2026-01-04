# Contributing to ZeroHeroLLM

First off, thank you for considering contributing to ZeroHeroLLM! We welcome any help to make this educational tool better. Whether you're fixing a bug, improving documentation, or suggesting a new feature, your contribution is valuable.

## How to Contribute

The best way to contribute is by opening issues or submitting pull requests (PRs).

### Reporting Bugs or Suggesting Enhancements

If you find a bug or have an idea for an enhancement, please [open an issue](https://github.com/vulnerabilities/llm-top10-labs/issues) first to discuss it. This allows us to coordinate efforts and prevent duplicate work.

### Submitting Pull Requests

1.  **Fork the repository** on GitHub.
2.  **Create a new branch** for your changes (`git checkout -b feature/your-awesome-feature`).
3.  **Make your changes.** Please ensure your code follows the existing style of the project.
4.  **Run the tests** to ensure you haven't introduced any regressions (`pytest`).
5.  **Commit your changes** with a clear and descriptive commit message.
6.  **Push your branch** to your fork (`git push origin feature/your-awesome-feature`).
7.  **Open a pull request** from your fork to the main repository.

## Areas for Improvement (What to Work On)

Here is a list of known areas that need improvement. This is a great place to start if you're looking for ways to contribute!

### 1. Backend Refactoring

-   **Modularize `app.py`:** The main `app.py` file currently contains the logic for all 10 labs. It would be much more maintainable to refactor this.
    -   **Suggestion:** Create a `labs/` directory in the backend and move the logic for each lab into its own Python file (e.g., `labs/llm01_prompt_injection.py`). The main `app.py` would then import and call these modular functions.

### 2. Improve the Testing Framework

-   **Basic Test Coverage:** The project now has a basic unit test suite (`test_labs.py`) that validates the `check_lab_success` function for each lab. This is a great start, but it could be expanded.
    -   **Suggestion:** Add more tests to cover other parts of the application. Good starting points would be:
        -   A test that checks if the homepage (`/`) returns a `200 OK` status.
        -   Tests to ensure each lab page (`/lab/llmXX`) loads correctly.
        -   "Unhappy path" tests for `check_lab_success` to ensure it correctly returns `False` for unsuccessful exploit attempts.

### 3. Enhance the User Interface

-   **No Responsive Design:** The UI is not optimized for mobile devices.
    -   **Suggestion:** Add CSS media queries to make the layout responsive, ensuring a good experience on smaller screens.
-   **Improve Lab Navigation:** It would be useful to have "Next Lab" and "Previous Lab" buttons on each lab page to make it easier to navigate through the content sequentially.

### 4. Improve the LLM Interaction

-   **Hardcoded Model Name:** The model name (`"phi3:mini"`) is hardcoded in `app.py`.
    -   **Suggestion:** Make the model name configurable, for example, via an environment variable (`OLLAMA_MODEL`). This would allow users to easily experiment with other models like `mistral` or `codellama`.
-   **Streaming Responses:** The UI currently waits for the full LLM response before displaying it.
    -   **Suggestion:** Modify the backend and frontend to stream the LLM response token by token. This would make the application feel much more responsive, especially for longer generations.

### 5. Documentation and Content

-   **Add a `LICENSE` file:** The project needs a `LICENSE` file.
-   **Expand Explanations:** While the labs are functional, the explanations could always be improved with more diagrams, examples, or links to external resources.

Thank you again for your interest in contributing!
