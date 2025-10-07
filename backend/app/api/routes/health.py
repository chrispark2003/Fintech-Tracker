"""
Health check endpoints
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Fintech Intelligence Platform API"
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check (can check DB connection, etc.)"""
    # TODO: Add database connection check
    return {
        "status": "ready",
        "database": "connected",  # TODO: Implement actual check
        "timestamp": datetime.utcnow().isoformat()
    }
