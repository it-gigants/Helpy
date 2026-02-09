from __future__ import annotations

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .topic import Topic


class OperatorTopic(Base):
    """Association table for operators and topics."""

    operator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # Relationships
    operator: Mapped["User"] = relationship()
    topic: Mapped["Topic"] = relationship(back_populates="operator_topics")
