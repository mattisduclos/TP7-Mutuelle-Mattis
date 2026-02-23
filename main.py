from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # tu pourras restreindre plus tard si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de données reçu depuis le frontend
class DemandeMutuelle(BaseModel):
    nom: str
    prenom: str
    age: int
    antecedents: bool
    sport_risque: bool

@app.post("/calculer")
def calculer_mensualites(demande: DemandeMutuelle):
    # Construction de la liste des réponses Oui/Non pour le calcul
    reponses_questionnaire = []
    if demande.antecedents:
        reponses_questionnaire.append("Oui")
    else:
        reponses_questionnaire.append("Non")

    if demande.sport_risque:
        reponses_questionnaire.append("Oui")
    else:
        reponses_questionnaire.append("Non")

    age_utilisateur = demande.age

    # Calcul des mensualités (bloc imposé)
    cout_base = 50
    cout_questions = reponses_questionnaire.count("Oui") * 10
    surcharge_age = 0
    if isinstance(age_utilisateur, int) and age_utilisateur > 65:
        surcharge_age = 0.02 * (age_utilisateur - 65) * cout_base
    cout_total = round(cout_base + cout_questions + surcharge_age, 2)

    return {
        "nom": demande.nom,
        "prenom": demande.prenom,
        "age": demande.age,
        "mensualite": cout_total
    }

# Servir les fichiers statiques (index.html, style.css, main.js)
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    # IMPORTANT : port 8613 pour user16 (8xx3)
    uvicorn.run(app, host="0.0.0.0", port=8613)