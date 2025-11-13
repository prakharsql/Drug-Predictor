# backend/app/routes/__init__.py
# Expose subrouters
from .predict import router as predict_router
from .health import router as health_router
