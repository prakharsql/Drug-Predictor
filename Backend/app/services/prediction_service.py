# backend/app/services/prediction_service.py
from ..model import load_model, predict_single, predict_batch
from ..config import settings

# Load model once at import time (app startup)
model = load_model(settings.MODEL_PATH)

def predict_single_service(age, sex, bp, chol, na_to_k):
    return predict_single(model, age, sex, bp, chol, na_to_k)

def predict_batch_service(df):
    return predict_batch(model, df)
