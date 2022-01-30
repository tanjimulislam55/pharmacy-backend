from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator
from typing import List, Optional, Union
from dotenv import load_dotenv
import os


load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    # 60 minutes * 24 hours * 8 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("URL_ONE"),
        os.environ.get("URL_TWO"),
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "E-Pharmacy"
    SENTRY_DSN: Optional[HttpUrl] = None

    class Config:
        case_sensitive = True


settings = Settings()
