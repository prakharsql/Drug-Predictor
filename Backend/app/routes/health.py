# backend/app/routes/health.py
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "message": "API is running"}
