from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "API Services"
    app_description: str = (
        "API base para gerenciar servicos internos. Utilize estes endpoints "
        "como ponto de partida para registrar e monitorar integracoes."
    )
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api"
    cors_allow_origins: list[str] = ["*"]
    billing_sheet_path: str = "data/clientes.xlsx"
    reminder_days_before_due: list[int] = [3, 1]
    waha_base_url: str = "http://localhost:3000"
    waha_api_token: str | None = None
    waha_default_sender: str | None = None
    waha_timeout_seconds: float = Field(10.0, ge=1.0, le=60.0)

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
