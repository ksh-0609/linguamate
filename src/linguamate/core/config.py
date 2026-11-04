"""Application settings loaded from environment variables and the .env file."""

from functools import lru_cache
from typing import Literal

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration for LinguaMate. Values come from the environment or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "LinguaMate"
    environment: Literal["development", "testing", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("log_level", mode="before")
    @classmethod
    def _normalise_log_level(cls, value: object) -> object:
        """Accept 'info', 'Info' or 'INFO' and turn it into 'INFO'."""
        return value.upper() if isinstance(value, str) else value


@lru_cache
def get_settings() -> Settings:
    """Return the settings, created once and reused. Fails with a clear message."""
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(
            f"Invalid application settings. Check your .env file.\n{exc}"
        ) from exc