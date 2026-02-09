from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base
from src.db.models.mixins import UUIDPkMixin, TimestampMixin


class RefreshSession(UUIDPkMixin, TimestampMixin, Base):
    refresh_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
