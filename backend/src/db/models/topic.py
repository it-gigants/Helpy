from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UUIDPkMixin, TimestampMixin

if TYPE_CHECKING:
    from .chat import Chat
    from .operator_topic import OperatorTopic


class Topic(Base, UUIDPkMixin, TimestampMixin):
    """Topic model for chat categorization."""

    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    chats: Mapped[list["Chat"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )
    operator_topics: Mapped[list["OperatorTopic"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
    )

