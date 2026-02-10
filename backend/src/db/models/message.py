from __future__ import annotations

from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UUIDPkMixin, TimestampMixin

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base, UUIDPkMixin, TimestampMixin):
    """Message model for chat messages."""

    chat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship()

