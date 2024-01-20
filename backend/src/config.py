from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    api_key_name: str="Authorization"
    api_key: str="123"

settings = Settings()
