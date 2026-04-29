from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_BROKER: str = "kafka:9092"
    CLICKHOUSE_HOST: str = "clickhouse"
    MAX_RISK: float = 0.02
    MAX_POSITION: float = 1000


settings = Settings()
