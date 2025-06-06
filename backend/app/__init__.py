# Gemini 2.5 Pro - June 6, 2025
# This file makes the 'app' directory a Python package.
# It defines the FastAPI application factory and a health-check route.

from fastapi import FastAPI

def create_app():
    """Create and configure an instance of the FastAPI application."""
    app = FastAPI(
        title="SpyEngine API",
        description="API for the Spy Story Game Engine",
        version="0.1.0"
    )

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Perform a health check."""
        return {"status": "ok", "message": "SpyEngine API is healthy"}

    # Future: Register API routers here
    # from .api.v1 import endpoints as v1_endpoints
    # app.include_router(v1_endpoints.router, prefix="/api/v1")

    return app

