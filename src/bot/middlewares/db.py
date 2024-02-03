from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.db.repository import DbRepository


class DbRepoMiddleware(BaseMiddleware):
    def __init__(self, repo: DbRepository):
        super().__init__()
        self._repo = repo

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["repo"] = self._repo
        return await handler(event, data)
