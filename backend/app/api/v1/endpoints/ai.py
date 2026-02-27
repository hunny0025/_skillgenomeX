from typing import Any
from fastapi import APIRouter, HTTPException
from app.models.pydantic_models import DietPlanRequest, DietPlanResponse
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/diet-plan", response_model=DietPlanResponse, summary="Generate AI diet plan")
async def generate_diet_plan(request: DietPlanRequest) -> Any:
    """
    Generate a personalized Indian diet plan using AI.
    """
    try:
        return await ai_service.generate_diet_plan(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")
