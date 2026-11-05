"""Application settings loaded from environment variables and the .env file."""

from functools import lru_cache
from typing import Literal, Self
from urllib.parse import quote

from pydantic import Field, SecretStr, ValidationError, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DEV_DB_PASSWORD = "change_me_dev_only"


class Settings(BaseSettings):
    """All configuration for LinguaMate. Values come from the environment or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application ---
    app_name: str = "LinguaMate"
    environment: Literal["development", "testing", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # --- PostgreSQL ---
    postgres_user: str = "linguamate"
    postgres_password: SecretStr = SecretStr(DEFAULT_DEV_DB_PASSWORD)
    postgres_db: str = "linguamate"
    postgres_host: str = "localhost"
    postgres_port: int = Field(default=5432, ge=1, le=65535)

    @field_validator("log_level", mode="before")
    @classmethod
    def _normalise_log_level(cls, value: object) -> object:
        """Accept 'info', 'Info' or 'INFO' and turn it into 'INFO'."""
        return value.upper() if isinstance(value, str) else value

    @model_validator(mode="after")
    def _reject_default_password_in_production(self) -> Self:
        """Never allow the well-known development password in production."""
        is_default = self.postgres_password.get_secret_value() == DEFAULT_DEV_DB_PASSWORD
        if self.environment == "production" and is_default:
            raise ValueError(
                "POSTGRES_PASSWORD must be changed from the development default "
                "when ENVIRONMENT is 'production'."
            )
        return self

    def _build_database_url(self, *, hide_password: bool) -> str:
        user = quote(self.postgres_user, safe="")
        if hide_password:
            password = "***"
        else:
            password = quote(self.postgres_password.get_secret_value(), safe="")
        return (
            f"postgresql+psycopg://{user}:{password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url(self) -> str:
        """Full SQLAlchemy URL including the password. Never log this."""
        return self._build_database_url(hide_password=False)

    @property
    def safe_database_url(self) -> str:
        """Same URL with the password hidden. Safe to print or log."""
        return self._build_database_url(hide_password=True)


@lru_cache
def get_settings() -> Settings:
    """Return the settings, created once and reused. Fails with a clear message."""
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(
            f"Invalid application settings. Check your .env file.\n{exc}"
        ) from exc