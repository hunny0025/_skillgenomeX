import json
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI, APIError
from app.core.config import settings
from app.models.pydantic_models import DietPlanRequest, DietPlanResponse, DayPlan, Meal

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def generate_diet_plan(self, request: DietPlanRequest) -> DietPlanResponse:
        if not self.client:
            logger.warning("OpenAI API key missing. Returning mock response.")
            return self._get_mock_plan(request)

        prompt = f"""
        Generate a 7-day Indian diet plan for a person with:
        Age: {request.age}
        Weight: {request.weight}kg
        Goal: {request.goal}
        Target Calories: {request.calories_target}
        Dietary Preferences: {', '.join(request.dietary_preferences) if request.dietary_preferences else 'None'}

        Output strictly valid JSON matching this schema:
        {{
            "plan_name": "string",
            "target_calories": int,
            "weekly_plan": [
                {{
                    "day": "Monday",
                    "breakfast": {{ "name": "string", "calories": int, "protein": "string", "description": "string" }},
                    "lunch": {{ "name": "string", "calories": int, "protein": "string", "description": "string" }},
                    "dinner": {{ "name": "string", "calories": int, "protein": "string", "description": "string" }},
                    "snack": {{ "name": "string", "calories": int, "protein": "string", "description": "string" }}
                }}
            ],
            "advice": "string"
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert nutritionist specializing in Indian cuisine. Return strictly JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            return DietPlanResponse(**data)

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return self._get_mock_plan(request)
        except Exception as e:
            logger.error(f"Error generating diet plan: {e}")
            return self._get_mock_plan(request)

    def _get_mock_plan(self, request: DietPlanRequest) -> DietPlanResponse:
        """Fallback mock plan when AI is unavailable."""
        return DietPlanResponse(
            plan_name=f"Standard Indian {request.goal.capitalize()} Plan (Mock)",
            target_calories=request.calories_target or 2000,
            weekly_plan=[
                DayPlan(
                    day="Monday",
                    breakfast=Meal(name="Poha", calories=300, protein="5g", description="Flattened rice with veggies"),
                    lunch=Meal(name="Dal Tadka & Rice", calories=450, protein="12g", description="Lentil curry with steamed rice"),
                    dinner=Meal(name="Roti & Paneer Bhurji", calories=400, protein="15g", description="Whole wheat bread with scrambled cottage cheese"),
                    snack=Meal(name="Masala Chai & Biscuits", calories=150, protein="2g", description="Spiced tea")
                )
            ],
            advice="Please configure OpenAI API key for personalized plans. Drink 3L water daily."
        )

ai_service = AIService()
