"""
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, stocks, digest, events
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Bloomberg Terminal for the Everyman - Market Intelligence API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(digest.router, prefix="/api/digest", tags=["digest"])
app.include_router(events.router, prefix="/api/events", tags=["events"])


@app.get("/")
async def root():
    return {
        "message": "Fintech Investment Intelligence Platform API",
        "version": "0.1.0",
        "docs": "/api/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
