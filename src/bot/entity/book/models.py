from sqlalchemy.orm import Mapped, mapped_column

from bot.db.base import Base
from bot.entity.user import enums


class User(Base):
    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[enums.Role] = mapped_column(default=enums.Role.Quest)


class Room(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    photos: Mapped[list[str]] = mapped_column()
    price_per_day: Mapped[int] = mapped_column()
    capacity: Mapped[int] = mapped_column()
    is_lux: Mapped[bool] = mapped_column()


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    checkin_date: Mapped[datetime] = mapped_column()
    checkout_date: Mapped[datetime] = mapped_column()
    guest_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
