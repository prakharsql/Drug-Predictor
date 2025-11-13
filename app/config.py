# backend/app/config.py
import os
from dotenv import load_dotenv

# Load .env from repository root or current working dir
load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Drug Prediction API")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "hyper_para_svm.joblib")
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    LOG_FILE: str = os.getenv("LOG_FILE", "app/logs/app.log")

settings = Settings()
