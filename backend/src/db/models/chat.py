from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UUIDPkMixin, TimestampMixin, ChatStatus

if TYPE_CHECKING:
    from .user import User
    from .topic import Topic
    from .message import Message


class Chat(Base, UUIDPkMixin, TimestampMixin):
    """Chat model for conversations between clients and operators."""

    __tablename__ = "chats"

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    operator_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[ChatStatus] = mapped_column(default=ChatStatus.QUEUED, nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    # Relationships
    client: Mapped["User"] = relationship(
        foreign_keys=[client_id],
    )
    operator: Mapped["User | None"] = relationship(
        foreign_keys=[operator_id],
    )
    topic: Mapped["Topic"] = relationship(back_populates="chats")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
    )

