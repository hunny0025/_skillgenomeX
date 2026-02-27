from fastapi import APIRouter
from app.api.v1.endpoints import recipes, ai

api_router = APIRouter()

api_router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
