from typing import Any, Awaitable, Callable, Dict, Tuple

from aiogram import BaseMiddleware, Bot, types
from aiogram.enums.message_entity_type import MessageEntityType
from aiogram.types import BotCommandScopeChat, TelegramObject

from bot.commands import get_admin_commands, get_guest_commands
from bot.db.repository import DbRepository
from bot.enums.user import Role

WELCOME_MESSAGE = """Добро пожаловать в бота гостевого дома 'Елена'!
Для получения справки по командам зайдите в /help
"""

COMMAND_START = "/start"


class AuthMiddleware(BaseMiddleware):
    def __init__(self, repo: DbRepository, admin_secret_key: str):
        self._admin_secret_key = admin_secret_key
        self._repo = repo

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        msg: types.Message,  # type: ignore[override]
        data: Dict[str, Any],
    ) -> Any:
        if not msg.bot:
            return

        bot: Bot = msg.bot
        chat_id = msg.chat.id

        if not self._msg_is_command_start(msg):
            return await handler(msg, data)

        user_exists = await self._repo.user_exists(chat_id)
        if not user_exists:
            commands, role = get_guest_commands(), Role.GUEST

            if not msg.text:
                return

            _, arg = self._parse_command(msg.text)
            if arg == self._admin_secret_key:
                commands, role = get_admin_commands(), Role.ADMIN

            await self._repo.add_user(chat_id, role)

            await bot.set_my_commands(commands, BotCommandScopeChat(chat_id=chat_id))
            return await bot.send_message(
                chat_id=chat_id,
                text=WELCOME_MESSAGE
                if role == Role.GUEST
                else WELCOME_MESSAGE + "\nВаша роль: АДМИН",
            )
        return await handler(msg, data)

    def _msg_is_command_start(self, msg: types.Message) -> bool:
        if not msg.entities:
            return False

        msg_type = msg.entities[0].type
        if msg_type != MessageEntityType.BOT_COMMAND:
            return False

        if not msg.text:
            return False

        command, _ = self._parse_command(msg.text)
        return command == COMMAND_START

    @staticmethod
    def _parse_command(text: str) -> Tuple[str, str]:
        try:
            command, arg = text.split(maxsplit=1)
        except ValueError:
            command, arg = text, ""
        return command, arg
