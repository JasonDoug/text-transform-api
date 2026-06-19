import os
from functools import lru_cache

from pydantic import BaseModel, Field


class TransformationSettings(BaseModel):
    provider: str = Field(default="openai-compatible")
    base_url: str | None = None
    api_key: str | None = None
    model: str = Field(default="llama3.1:8b")
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=1000, gt=0)
    timeout: int = Field(default=60, gt=0)

    @classmethod
    def from_env(cls) -> "TransformationSettings":
        return cls(
            provider=os.getenv("TRANSFORMATION_PROVIDER", "openai-compatible"),
            base_url=os.getenv("TRANSFORMATION_BASE_URL"),
            api_key=os.getenv("TRANSFORMATION_API_KEY"),
            model=os.getenv("TRANSFORMATION_MODEL", "llama3.1:8b"),
            temperature=float(os.getenv("TRANSFORMATION_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("TRANSFORMATION_MAX_TOKENS", "1000")),
            timeout=int(os.getenv("TRANSFORMATION_TIMEOUT", "60")),
        )


@lru_cache
def get_transformation_settings() -> TransformationSettings:
    return TransformationSettings.from_env()
