import enum
from pathlib import Path
from tempfile import gettempdir
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(enum.StrEnum):
    """Possible log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class RunConfig(BaseModel):
    """Settings for running the application."""

    host: str = "127.0.0.1"
    """Host to bind the application to."""
    port: int = 8000
    """Port to bind the application to."""
    workers_count: int = 1
    """Quantity of workers for uvicorn."""
    reload: bool = False
    """Enable uvicorn reloading."""


class LoggingConfig(BaseModel):
    """Settings related with the logging."""

    level: LogLevel = LogLevel.INFO
    """Log level for the application."""


class DatabaseConfig(BaseModel):
    """Settings for database connection."""

    host: str = "localhost"
    """Database host."""
    port: int = 5432
    """Database port."""
    user: str = "helpy"
    """Database user."""
    password: str = "helpy"
    """Database password."""
    base: str = "helpy"
    """Database name."""
    echo: bool = False
    """Enable SQLAlchemy echo mode."""

    @property
    def url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            path=f"/{self.base}",
        )


class RedisConfig(BaseModel):
    """Settings for Redis connection."""

    host: str = "helpy-redis"
    """Redis host."""
    port: int = 6379
    """Redis port."""
    user: str | None = None
    """Redis user."""
    password: str | None = None
    """Redis password."""
    base: int | None = None
    """Redis database number."""

    @property
    def url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.
        """
        path = ""
        if self.base is not None:
            path = f"/{self.base}"
        return URL.build(
            scheme="redis",
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            path=path,
        )


class KafkaConfig(BaseModel):
    """Settings for Kafka connection."""

    bootstrap_servers: list[str] = ["helpy-kafka:9092"]
    """List of Kafka bootstrap servers."""


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="HELPY__",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    run: RunConfig = RunConfig()
    """Run configuration."""
    logging: LoggingConfig = LoggingConfig()
    """Logging configuration."""
    db: DatabaseConfig = DatabaseConfig()
    """Database configuration."""
    redis: RedisConfig = RedisConfig()
    """Redis configuration."""
    kafka: KafkaConfig = KafkaConfig()
    """Kafka configuration."""
    environment: str = "dev"
    """Current environment."""


settings = Settings()
