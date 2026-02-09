from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UUIDPkMixin, TimestampMixin, Role


class User(Base, UUIDPkMixin, TimestampMixin):
    email: Mapped[str] = mapped_column(String(255), unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_profile_completed: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(default=Role.CLIENT)
