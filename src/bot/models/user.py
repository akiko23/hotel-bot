from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.base import Base
from bot.enums.user import Role

if TYPE_CHECKING:
    from bot.models.booking import Booking


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    role: Mapped[Role] = mapped_column(default=Role.GUEST)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates='guest',
        cascade='all, delete'
    )
