from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column()
    photos: Mapped[list[str]] = mapped_column(ARRAY(TEXT))
    price_per_day: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    is_lux: Mapped[bool] = mapped_column(default=False)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    checkin_date: Mapped[datetime] = mapped_column()
    checkout_date: Mapped[datetime] = mapped_column()
    guest_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
