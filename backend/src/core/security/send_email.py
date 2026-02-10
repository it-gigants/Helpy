from email.message import EmailMessage

import aiosmtplib

from .utils import encode_jwt, decode_jwt
from src.core.exceptions.service.auth import InvalidTokenError


async def send_email(
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
):
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    await aiosmtplib.send(message, hostname="maildev", port=1025)


def generate_link_for_verification(token: str) -> str:
    # TODO: change to nginx url
    return f"http://0.0.0.0:8000/api/v1/auth/verify?token={token}"


def create_token_for_verification(email: str):
    return encode_jwt({"sub": email}, 3)


async def send_verification_email(
        email: str,
):
    token = create_token_for_verification(email)
    admin_email = "helpy@mail.ru"
    await send_email(
        from_email=admin_email,
        to_email=email,
        subject="Registration confirmation on Helpy",
        body=f"To confirm your registration, please follow the link {generate_link_for_verification(token)}",
    )


def verify_verification_token(token: str):
    try:
        payload = decode_jwt(token)
        return payload
    except InvalidTokenError:
        return None


def create_token_for_password_reset(email: str):
    return encode_jwt({"sub": email}, 15)  # token is valid for 15 minutes


def generate_link_for_password_reset(token: str) -> str:
    # TODO: change to nginx URL
    return f"http://0.0.0.0:3000/reset-password?token={token}"


async def send_password_reset_email(email: str):
    token = create_token_for_password_reset(email)
    admin_email = "helpy@mail.ru"
    await send_email(
        from_email=admin_email,
        to_email=email,
        subject="Password reset on Helpy",
        body=f"To reset your password, please follow the link: {generate_link_for_password_reset(token)}. The link is valid for 15 minutes.",
    )
