"""Exception handler middleware for FastAPI application."""

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse

from src.core.exceptions.api.base import InternalServerException
from src.core.exceptions.service.base import (
    AppError,
    NotFoundError,
    ConflictError,
    InvalidInputError,
    BadRequestError,
    ForbiddenError,
)
from src.core.exceptions.service.auth import AuthError
from src.core.exceptions.service.aws import AwsError
from src.core.log import logger
from src.core.utils import get_time, get_uuid


async def request_handler(request: Request, call_next):
    """Middleware used by FastAPI to process each request, featuring:

    - Contextualize request logs with an unique Request ID (UUID4) for each unique request.
    - Catch exceptions during the request handling. Translate custom API exceptions into responses,
      or treat (and log) unexpected exceptions.
    """
    # Skip logging for healthcheck endpoint
    is_healthcheck = request.url.path in ["/api/status", "/status"]

    start_time = get_time(seconds_precision=False)
    request_id = get_uuid()

    with logger.contextualize(request_id=request_id):
        if not is_healthcheck:
            logger.bind(url=str(request.url), method=request.method).debug(
                "Request started"
            )

        try:
            response: Response = await call_next(request)

        except AppError as exc:
            response = ErrorProcessor.process_app_exception(exc)

        except HTTPException as exc:
            response = ErrorProcessor.process_http_exception(exc)

        except Exception:
            logger.opt(exception=True).error("Request failed due to unexpected error")
            response = InternalServerException().response()

        end_time = get_time(seconds_precision=False)
        time_elapsed = round(end_time - start_time, 5)

        if not is_healthcheck:
            logger.bind(
                time_elapsed=time_elapsed, response_status=response.status_code
            ).debug("Request ended")

        return response


class ErrorProcessor:
    """Process and log different types of exceptions."""

    @classmethod
    def log_exception(cls, exc: Exception, status_code: int) -> None:
        """Log exception based on status code."""
        if status_code < 500:
            logger.bind(exception=str(exc)).info(
                "Request did not succeed due to client-side error"
            )
        else:
            logger.opt(exception=True).warning(
                "Request did not succeed due to server-side error"
            )

    @classmethod
    def process_app_exception(cls, exc: AppError) -> JSONResponse:
        """Process custom application exceptions."""
        special_message = None
        if isinstance(exc, ForbiddenError):
            status_code = 403
        elif isinstance(exc, NotFoundError):
            status_code = 404
        elif isinstance(exc, ConflictError):
            status_code = 409
        elif isinstance(exc, AuthError):
            status_code = 401
        elif isinstance(exc, InvalidInputError):
            status_code = 422
        elif isinstance(exc, AwsError):
            status_code = 503
            special_message = "S3 service not available"
        elif isinstance(exc, BadRequestError):
            status_code = 400
        else:
            status_code = 400

        cls.log_exception(exc, status_code)
        return JSONResponse(
            status_code=status_code,
            content={"detail": special_message if special_message else exc.detail},
        )

    @classmethod
    def process_http_exception(cls, exc: HTTPException) -> JSONResponse:
        """Process FastAPI HTTPException."""
        status_code = exc.status_code
        detail = exc.detail
        cls.log_exception(exc, status_code)
        return JSONResponse(status_code=status_code, content={"detail": detail})

