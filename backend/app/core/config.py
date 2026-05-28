from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Platform"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./app.db"
    admin_username: str = "admin"
    admin_password: str = "admin123"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings() -> Settings:
    return Settings()
