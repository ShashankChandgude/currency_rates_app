"""
Main FastAPI application entry point.
"""

from typing import Any, Dict

from app.core.config import settings
from app.core.logging import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Currency Converter API",
    description=(
        "A high-performance API for currency conversion and exchange rate data"
    ),
    version="0.1.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint."""
    return {
        "message": "Currency Converter API",
        "version": "0.1.0",
        "status": "healthy",
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include routers
# from app.api.v1.api import api_router
# app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
