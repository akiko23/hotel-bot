from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.entity.user import enums

if TYPE_CHECKING:
    from bot.entity.booking.models import Booking


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    role: Mapped[enums.Role] = mapped_column(default=enums.Role.GUEST)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates='guest',
        cascade='all, delete'
    )

