from pydantic_settings import BaseSettings, SettingConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    DATABASE_URL: str 
    SECRET_KEY: str

    model_config = SettingConfigDict(env_file=".env")

settings = Settings()