from asyncio import sleep
from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing_extensions import TypeAlias

MediaGroup: TypeAlias = List[int]


class MediaGroupMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self._memo: Dict[str, MediaGroup] = {}

    @staticmethod
    def _get_content(msg: Message) -> Any:
        if msg.photo:
            return msg.photo[-1]
        return getattr(msg, msg.content_type)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore[override]
        data: Dict[str, Any],
    ) -> Any:
        media_group_id, content = event.media_group_id, self._get_content(event)
        if media_group_id:
            if not self._memo.get(media_group_id):
                self._memo[media_group_id] = list()
            self._memo[media_group_id].append(content)
            await sleep(0.5)  # giving time to get and process other media

            if self._memo.get(media_group_id):
                data["media_group"] = self._memo[media_group_id]
                del self._memo[media_group_id]
        return await handler(event, data)
