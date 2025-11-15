import numpy as np
import joblib
import os

# Path of this file: backend/app/services/prediction_service.py
CURRENT_DIR = os.path.dirname(__file__)       # → backend/app/services
APP_DIR = os.path.dirname(CURRENT_DIR)        # → backend/app

# Correct model location: backend/app/hyper_para_svm.joblib
MODEL_PATH = os.path.join(APP_DIR, "hyper_para_svm.joblib")

# Load model
model_dict = joblib.load(MODEL_PATH)
model = model_dict["model"]
enc = model_dict["encoders"]


def predict_single_service(age, sex, bp, chol, na_to_k):

    X = np.array([[
        float(age),
        enc["sex"].transform([sex])[0],
        enc["bp"].transform([bp])[0],
        enc["chol"].transform([chol])[0],
        float(na_to_k)
    ]])

    pred_encoded = model.predict(X)[0]
    return enc["drug"].inverse_transform([pred_encoded])[0]
