import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config import load_config
from bot.consts import CONFIG_PATH, LOGGING_FORMAT
from bot.db.repository import DbRepository
from bot.handlers.booking import dialog
from bot.handlers.booking import router as booking_router
from bot.handlers.conversation import router as conversation_router
from bot.handlers.user import router as user_router
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.media_group import MediaGroupMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
    cfg = load_config(CONFIG_PATH)

    storage = RedisStorage.from_url(cfg.redis.dsn)
    storage.key_builder = DefaultKeyBuilder(with_destiny=True)

    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)
    dp.include_router(booking_router)
    dp.include_router(conversation_router)
    dp.include_router(dialog)

    setup_dialogs(dp)

    engine = create_async_engine(cfg.db.dsn, future=True, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    repo = DbRepository(session_factory=session_factory)

    dp.message.middleware(AuthMiddleware(repo, cfg.bot.admin_secret_key))
    dp.message.middleware(MediaGroupMiddleware())

    bot = Bot(token=cfg.bot.token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
