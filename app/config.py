from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str

    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7

    # Redis configuration
    redis_url: str = "redis://localhost:6379"
    # This is a special class variable that tells Pydantic to read from .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()