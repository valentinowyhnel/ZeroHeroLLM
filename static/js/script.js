document.addEventListener('DOMContentLoaded', () => {
    const exploitForms = document.querySelectorAll('.exploit-form');

    exploitForms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const vulnId = form.dataset.vulnId;
            const formData = new FormData(form);
            const resultDiv = form.nextElementSibling; // S'attend à ce que le div de résultat soit juste après le formulaire

            resultDiv.innerHTML = '<p>Traitement en cours...</p>';

            try {
                const response = await fetch(`/exploit/${vulnId}`, {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const result = await response.json();
                    // Pour LLM02, nous voulons afficher le HTML brut pour démontrer la vulnérabilité.
                    if (vulnId === 'llm02') {
                        resultDiv.innerHTML = result.response;
                    } else {
                        // Pour les autres, nous l'affichons comme du texte pour éviter d'exécuter du code.
                        const p = document.createElement('p');
                        p.textContent = result.response;
                        resultDiv.innerHTML = '';
                        resultDiv.appendChild(p);
                    }
                } else {
                    resultDiv.innerHTML = '<p>Une erreur est survenue lors de la requête.</p>';
                }
            } catch (error) {
                console.error('Erreur:', error);
                resultDiv.innerHTML = '<p>Une erreur est survenue.</p>';
            }
        });
    });
});
