from typing import Generator
from app.core.config import settings
from app.core.security import get_api_key

# This file can hold dependencies like database sessions, 
# shared logic, or user authentication dependencies.

# Example:
# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()
