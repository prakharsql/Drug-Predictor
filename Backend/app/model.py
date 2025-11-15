# backend/app/model.py
import joblib
import pandas as pd
from .utils import SEX_MAP, BP_MAP, CHOL_MAP, DRUG_MAP
from typing import Optional

def load_model(path: str):
    """
    Load a model saved by joblib. Return None on failure.
    """
    try:
        m = joblib.load(path)
        return m
    except Exception as e:
        # In production you'd log this
        print(f"[model.load_model] Failed to load model at '{path}': {e}")
        return None

def _map_inputs(age, sex, bp, chol, na_to_k):
    """
    Converts raw inputs to numeric features expected by the model.
    Raises ValueError if mapping fails.
    """
    try:
        sx = SEX_MAP[str(sex).upper()]
        bpv = BP_MAP[str(bp).upper()]
        ch = CHOL_MAP[str(chol).upper()]
    except KeyError as e:
        raise ValueError(f"Invalid categorical input: {e}")

    # Ensure numeric types
    try:
        age_f = float(age)
        na_to_k_f = float(na_to_k)
    except Exception:
        raise ValueError("Age and Na_to_K must be numeric.")

    return [age_f, sx, bpv, ch, na_to_k_f]

def predict_single(model, age, sex, bp, chol, na_to_k) -> str:
    """
    Predict a single sample; returns predicted drug name (string).
    """
    if model is None:
        raise ValueError("Model not loaded.")

    # Map input features
    features = [_map_inputs(age, sex, bp, chol, na_to_k)]

    # Make prediction
    pred = model.predict(features)

    # Decode numeric label to drug name
    label = DRUG_MAP.get(int(pred[0]), "Unknown")
    return label

def predict_batch(model, df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict on a dataframe with expected columns:
    ['Age','Sex','BP','Cholesterol','Na_to_K']
    Returns original dataframe with a new 'Prediction' column.
    """
    if model is None:
        raise ValueError("Model not loaded.")
    required = ['Age','Sex','BP','Cholesterol','Na_to_K']
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Missing required column: {c}")

    # Map categorical columns
    df_m = df.copy()
    df_m['Sex'] = df_m['Sex'].map(lambda x: SEX_MAP.get(str(x).upper()))
    df_m['BP'] = df_m['BP'].map(lambda x: BP_MAP.get(str(x).upper()))
    df_m['Cholesterol'] = df_m['Cholesterol'].map(lambda x: CHOL_MAP.get(str(x).upper()))

    if df_m[['Sex','BP','Cholesterol']].isnull().any().any():
        raise ValueError("Some categorical values could not be mapped. Allowed values: Sex(F/M), BP(LOW/NORMAL/HIGH), Cholesterol(NORMAL/HIGH)")

    X = df_m[['Age','Sex','BP','Cholesterol','Na_to_K']].values
    preds = model.predict(X)
    df_result = df.copy()
    df_result['Prediction'] = [DRUG_MAP.get(int(p), "Unknown") for p in preds]
    return df_result
