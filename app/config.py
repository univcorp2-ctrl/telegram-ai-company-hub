from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_bot_token: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_webhook_secret: str | None = Field(default=None, alias="TELEGRAM_WEBHOOK_SECRET")
    app_db_path: Path = Field(default=Path("data/app.db"), alias="APP_DB_PATH")
    obsidian_vault_path: Path = Field(default=Path("outputs/ObsidianVault"), alias="OBSIDIAN_VAULT_PATH")
    github_repository_target: str | None = Field(default=None, alias="GITHUB_REPOSITORY_TARGET")


@lru_cache
def get_settings() -> Settings:
    return Settings()
