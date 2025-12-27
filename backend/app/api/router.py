"""
Main API router that combines all route modules
"""

from fastapi import APIRouter
from app.api.routes import router as routes_router

api_router = APIRouter()

# Include all routes
api_router.include_router(routes_router)
