from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class RefreshToken(Base):
    __tablename__ = "auth_refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str]
    expires_at: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")


from ..models import User
