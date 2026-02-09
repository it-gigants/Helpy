from src.core.exceptions.service.base import AppError


class AuthError(AppError):
    message = "Authentication error"


class EmailNotExistsError(AuthError):
    message = "Email does not exist"


class InvalidTokenError(AuthError):
    message = "Invalid token"


class TokenExpiredError(AuthError):
    message = "Token has expired"


class InvalidPasswordError(AuthError):
    message = "Invalid password"


class EmailNotVerifiedError(AuthError):
    message = "Email not verified"
