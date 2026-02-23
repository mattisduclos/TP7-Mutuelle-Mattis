document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-mutuelle");
    const zoneResultat = document.getElementById("resultat");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const nom = document.getElementById("nom").value;
        const prenom = document.getElementById("prenom").value;
        const age = parseInt(document.getElementById("age").value, 10);
        const antecedents = document.getElementById("antecedents").checked;
        const sportRisque = document.getElementById("sport_risque").checked;

        const donnees = {
            nom: nom,
            prenom: prenom,
            age: age,
            antecedents: antecedents,
            sport_risque: sportRisque
        };

        try {
            const response = await fetch("/calculer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(donnees)
            });

            if (!response.ok) {
                throw new Error("Erreur serveur : " + response.status);
            }

            const data = await response.json();

            zoneResultat.textContent =
                "Montant estimé des mensualités : " + data.mensualite + " €";
        } catch (error) {
            console.error(error);
            zoneResultat.textContent =
                "Une erreur s'est produite lors du calcul.";
        }
    });
});
