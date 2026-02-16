from http.client import HTTPException

from fastapi import FastAPI
from models.Rmodel import PricePredictionRequest,PricePredictionResponse
from service.predictionService import PredictionService
app = FastAPI(title="Real Estate API")

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "price-prediction-api"
    }

@app.post("/api/v1/predict-price", response_model=PricePredictionResponse)
def predict_price(request: PricePredictionRequest):

    try:
        result = PredictionService().predict(request)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))