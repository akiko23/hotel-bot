import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.models import User
from bot.enums.user import Role

logger = logging.getLogger(__name__)


class DbRepository:
    __slots__ = ('_session_factory',)

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory

    async def user_exists(self, user_id: int) -> bool:
        async with self._session_factory() as session:
            stmt = select(User).where(User.telegram_id == user_id)
            res = await session.execute(stmt)
        return bool(res.scalar_one_or_none())

    async def add_user(self, user_id: int, role: Role = Role.GUEST) -> None:
        async with self._session_factory() as session:
            async with session.begin():
                session.add(User(telegram_id=user_id, role=role))
