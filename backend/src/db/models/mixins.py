from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Role(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    CLIENT = "client"


class ChatStatus(str, Enum):
    QUEUED = "queued"
    ACTIVE = "active"
    CLOSED = "closed"


class UUIDPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=func.now(),
        nullable=True,
    )
