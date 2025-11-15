from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
import logging
from logging.handlers import RotatingFileHandler
import os

# Routers
from .routes.health import router as health_router
from .routes.predict import router as predict_router

# -----------------------------------------------------------------------------
# App initialization
# -----------------------------------------------------------------------------
app = FastAPI(title=settings.PROJECT_NAME)

# -----------------------------------------------------------------------------
# Logging configuration
# -----------------------------------------------------------------------------
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

handler = RotatingFileHandler(
    settings.LOG_FILE, maxBytes=2_000_000, backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# -----------------------------------------------------------------------------
# CORS setup
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# STATIC FILES (Fixes CSS Not Loading)
# -----------------------------------------------------------------------------
# VERY IMPORTANT — this must match your actual folder structure
# Backend/app/frontend/static/style.css  →  served at /static/style.css

STATIC_DIR = os.path.join(os.path.dirname(__file__), "frontend", "static")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "frontend", "templates")

print("STATIC PATH:", STATIC_DIR)      # Debug
print("TEMPLATES PATH:", TEMPLATES_DIR)

# Mount static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# -----------------------------------------------------------------------------
# Root Route
# -----------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/predict/")

# -----------------------------------------------------------------------------
# Routers
# -----------------------------------------------------------------------------
app.include_router(health_router)
app.include_router(predict_router)
