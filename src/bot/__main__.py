import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.consts import LOGGING_FORMAT, CONFIG_PATH
from bot.config import load_config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT
    )
    cfg = load_config(CONFIG_PATH)
    # print(cfg.bot.token)


if __name__ == "__main__":
    asyncio.run(main())
