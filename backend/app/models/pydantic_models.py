from typing import List, Optional
from pydantic import BaseModel, Field

# --- RECIPE MODELS ---

class Recipe(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    imageType: Optional[str] = None
    protein: Optional[str] = None
    calories: Optional[int] = None
    fat: Optional[str] = None
    carbs: Optional[str] = None

class RecipeResponse(BaseModel):
    recipes: List[Recipe]
    totalResults: Optional[int] = None
    executionTime: Optional[float] = None

class RecipeInfo(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    readyInMinutes: Optional[int] = None
    servings: Optional[int] = None
    sourceUrl: Optional[str] = None
    summary: Optional[str] = None
    # Add other fields as returned by Foodoscope/Spoonacular-like API

# --- AI MODELS ---

class DietPlanRequest(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    weight: float = Field(..., gt=0)
    goal: str = Field(..., description="weight loss, muscle gain, or maintenance")
    calories_target: Optional[int] = Field(2000, gt=500)
    dietary_preferences: Optional[List[str]] = Field(default_factory=list, description="vegetarian, vegan, etc.")

class Meal(BaseModel):
    name: str
    calories: int
    protein: str
    description: str

class DayPlan(BaseModel):
    day: str
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snack: Optional[Meal] = None

class DietPlanResponse(BaseModel):
    plan_name: str
    target_calories: int
    weekly_plan: List[DayPlan]
    advice: str
