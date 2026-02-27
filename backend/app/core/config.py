import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FoodScope AI"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # External APIs
    FOODOSCOPE_TOKEN: str
    OPENAI_API_KEY: Optional[str] = None
    
    # Deployment
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        case_sensitive=True
    )

settings = Settings()
