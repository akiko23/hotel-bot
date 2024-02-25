from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.enums.user import Role

if TYPE_CHECKING:
    from bot.models.booking import Booking


class User(Base):  # type: ignore[misc]
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=False
    )
    role: Mapped[Role] = mapped_column(default=Role.GUEST)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    bookings: Mapped[List["Booking"]] = relationship(
        back_populates="guest", cascade="all, delete"
    )
