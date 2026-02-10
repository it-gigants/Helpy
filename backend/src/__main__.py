import uvicorn

from src.core.config import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "src.web.application:get_app",
        workers=settings.run.workers_count,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
        log_level=settings.logging.level.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
