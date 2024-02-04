from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base

if TYPE_CHECKING:
    from bot.entity.user.models import User


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    checkin_date: Mapped[datetime] = mapped_column()
    checkout_date: Mapped[datetime] = mapped_column()
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    guest_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))

    room: Mapped["Room"] = relationship(back_populates="bookings")
    guest: Mapped["User"] = relationship(back_populates="bookings")


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column()
    photos: Mapped[list[str]] = mapped_column(ARRAY(TEXT))
    price_per_day: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    is_lux: Mapped[bool] = mapped_column(default=False)

    bookings: Mapped[list["Booking"]] = relationship(
        cascade='all, delete',
        back_populates="room",
    )
