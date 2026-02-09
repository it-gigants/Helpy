import src.web.api.v1.auth
from fastapi import APIRouter

from src.core.config import settings

router = APIRouter(prefix=settings.api.v1.prefix)


router.include_router(auth.router, tags=["Auth"], prefix=settings.api.v1.auth)
