from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BINANCE_API_KEY: str = "your_key"
    BINANCE_SECRET: str = "your_secret"
    BASE_URL: str = "https://fapi.binance.com"

    MAX_RISK: float = 0.02
    MAX_DRAWDOWN: float = 0.2


settings = Settings()
