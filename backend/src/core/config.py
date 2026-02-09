from pathlib import Path
from typing import Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

SRC_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SRC_DIR.parent
ENV_PATH = BASE_DIR / ".env"


class RunConfig(BaseModel):
    """Settings for running the application."""

    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False


class LoggingConfig(BaseModel):
    """Settings related with the logging."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"] = "INFO"
    serialize: bool = False


class AuthJWTConfig(BaseModel):
    """Settings for JWT authentication."""

    private_key_path: Path = SRC_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = SRC_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    refresh_token_expire_days: int = 30
    access_token_expire_minutes: int = 15


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
    pool_size: int = 5
    """Database connection pool size."""
    max_overflow: int = 10
    """Maximum overflow connections."""
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

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


class ApiV1Prefix(BaseModel):
    """API route prefixes configuration."""
    prefix: str = "/v1"
    auth: str = "/auth"
    """Auth API prefix."""


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore",
        case_sensitive=False,
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
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    """JWT authentication configuration."""
    environment: str = "dev"
    """Current environment."""
    api: ApiPrefix = ApiPrefix()
    """API prefixes configuration."""


settings = Settings()
