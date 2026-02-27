import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class FoodoscopeClient:
    def __init__(self):
        self.base_url = "https://api.foodoscope.com" # As per requirements
        self.token = settings.FOODOSCOPE_TOKEN
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.timeout = httpx.Timeout(10.0)
        self.transport = httpx.AsyncHTTPTransport(retries=3)

    async def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(transport=self.transport, timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method, 
                    f"{self.base_url}{endpoint}", 
                    headers=self.headers, 
                    params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Foodoscope API error: {e.response.status_code} - {e.response.text}")
                raise e # Propagate to be caught by endpoint handler
            except httpx.RequestError as e:
                logger.error(f"Foodoscope connection error: {e}")
                raise e

    async def get_recipes_by_protein(self, min_protein: float, max_protein: float, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        return await self._request("GET", "/recipes/protein", params={
            "min": min_protein,
            "max": max_protein,
            "page": page,
            "limit": limit
        })

    async def get_recipes_by_calories(self, min_cals: int, max_cals: int, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        return await self._request("GET", "/recipes/calories", params={
            "min": min_cals,
            "max": max_cals,
            "page": page,
            "limit": limit
        })

    async def get_recipes_by_ingredients(self, ingredients: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        return await self._request("GET", "/recipes/findByIngredients", params={
            "ingredients": ingredients,
            "page": page,
            "limit": limit
        })

    async def get_recipes_info(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return await self._request("GET", "/recipes/complexSearch", params={
            "page": page,
            "limit": limit
        })

foodoscope_client = FoodoscopeClient()
