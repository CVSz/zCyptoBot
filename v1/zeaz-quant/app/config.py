from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAX_RISK: float = 0.02
    MAX_POSITION: float = 1000


settings = Settings()
