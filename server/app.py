from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Configuration CORS pour permettre les requêtes depuis Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle
model = joblib.load("iris_model.joblib")

# Mapping des prédictions vers les noms de fleurs
iris_names = {
    0: "Setosa",
    1: "Versicolor",
    2: "Virginica"
}

# Définir le modèle de données
class Item(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/")
async def root():
    return {"message": "Iris ML API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/predict/")
async def predict(item: Item):
    try:
        # Convertir en array numpy
        data = np.array([[
            item.sepal_length,
            item.sepal_width,
            item.petal_length,
            item.petal_width
        ]])
        
        # Faire la prédiction
        prediction = model.predict(data)
        prediction_number = int(prediction[0])
        
        # Obtenir le nom de la fleur
        flower_name = iris_names[prediction_number]
        
        return {
            "prediction": prediction_number,
            "flower_name": flower_name
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))