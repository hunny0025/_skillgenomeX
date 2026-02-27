from typing import Any, List
from fastapi import APIRouter, Depends, Query, HTTPException
from app.services.foodoscope import foodoscope_client

router = APIRouter()

@router.get("/protein-range", summary="Get recipes by protein range")
async def get_recipes_by_protein(
    min_protein: float = Query(10, ge=0, description="Minimum protein in grams"),
    max_protein: float = Query(50, ge=0, description="Maximum protein in grams"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page")
) -> Any:
    """
    Fetch recipes within a specific protein range.
    """
    try:
        data = await foodoscope_client.get_recipes_by_protein(
            min_protein=min_protein, 
            max_protein=max_protein, 
            page=page, 
            limit=limit
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calories", summary="Get recipes by calorie range")
async def get_recipes_by_calories(
    min_calories: int = Query(500, ge=0, description="Minimum calories"),
    max_calories: int = Query(800, ge=0, description="Maximum calories"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
) -> Any:
    """
    Fetch recipes within a specific calorie range.
    """
    try:
        return await foodoscope_client.get_recipes_by_calories(
            min_cals=min_calories,
            max_cals=max_calories,
            page=page,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ingredients", summary="Get recipes by ingredients")
async def get_recipes_by_ingredients(
    ingredients: str = Query(..., description="Comma separated ingredients", min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
) -> Any:
    """
    Fetch recipes containing specific ingredients.
    """
    try:
        return await foodoscope_client.get_recipes_by_ingredients(
            ingredients=ingredients,
            page=page,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info", summary="Get general recipe info")
async def get_recipe_info(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50)
) -> Any:
    """
    Fetch general recipe information (search).
    """
    try:
        return await foodoscope_client.get_recipes_info(page=page, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
