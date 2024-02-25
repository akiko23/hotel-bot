from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base

if TYPE_CHECKING:
    from bot.models.user import User


class Booking(Base):  # type: ignore[misc]
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    checkin_date: Mapped[datetime] = mapped_column()
    checkout_date: Mapped[datetime] = mapped_column()
    guest_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE")
    )

    guest: Mapped["User"] = relationship(back_populates="bookings")
