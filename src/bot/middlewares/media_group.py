from typing import Dict, Any, Awaitable, Callable
from asyncio import sleep

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class MediaGroupMiddleware(BaseMiddleware):
    def __init__(self):
        self._memo = {}
    
    @staticmethod
    def _get_content(msg: Message):
        if msg.photo:
            return msg.photo[-1]
        return getattr(msg, msg.content_type)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ): 
        media_group_id, content = event.media_group_id, self._get_content(event)
        if media_group_id:
            if not self._memo.get(media_group_id):
                self._memo[media_group_id] = {
                    "media_group": list(),
                }
            self._memo[media_group_id]["media_group"].append(content)
            await sleep(0.5)  # giving time to get and process other media

            if self._memo.get(media_group_id):
                data["media_group"] = self._memo[media_group_id]["media_group"]
                del self._memo[media_group_id]
        return await handler(event, data)
    