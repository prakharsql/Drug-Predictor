from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from fastapi.responses import RedirectResponse
import logging
from logging.handlers import RotatingFileHandler
import os

# Correct router imports
from .routes.health import router as health_router
from .routes.predict import router as predict_router

app = FastAPI(title=settings.PROJECT_NAME)

# Logging
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

# Redirect root BEFORE routers
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/predict/")

# Include routers
app.include_router(health_router)
app.include_router(predict_router)
