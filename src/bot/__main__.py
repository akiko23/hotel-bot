import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.consts import LOGGING_FORMAT, CONFIG_PATH
from bot.config import load_config
from bot.db.repository import DbRepository
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.media_group import MediaGroupMiddleware

from bot.entity.user import router as user_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT
    )
    cfg = load_config(CONFIG_PATH)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)

    engine = create_async_engine(cfg.db.dsn, future=True, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    repo = DbRepository(session_factory=session_factory)

    dp.update.middleware(AuthMiddleware(repo, cfg.bot.admin_secret_key))
    dp.message.middleware(MediaGroupMiddleware())

    bot = Bot(token=cfg.bot.token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
