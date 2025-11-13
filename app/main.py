# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import predict_router, health_router
import logging
from logging.handlers import RotatingFileHandler
import os

app = FastAPI(title=settings.PROJECT_NAME)

# Logging setup: rotating file handler
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
handler = RotatingFileHandler(settings.LOG_FILE, maxBytes=2_000_000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(predict_router)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
