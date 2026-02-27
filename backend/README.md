# FoodScope AI Backend

FastAPI backend for FoodScope AI, an Indian meal recommendation system.

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Deployment

This project is configured for Render/Railway.
Ensure `FOODOSCOPE_TOKEN` and `OPENAI_API_KEY` are set in the environment variables.

## Endpoints

Documentation available at `/docs` when running.
