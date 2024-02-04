from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot, types
from aiogram.types import TelegramObject, BotCommandScopeChat
from aiogram.enums.message_entity_type import MessageEntityType

from bot.commands import get_guest_commands, get_admin_commands
from bot.db.repository import DbRepository
from bot.entity.user import enums

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
            event: types.Update,
            data: Dict[str, Any]
    ):
        bot: Bot = event.bot
        msg = event.message
        chat_id = msg.chat.id

        if not self._msg_is_command_start(msg):
            return await handler(event, data)

        user_exists = await self._repo.user_exists(chat_id)
        if not user_exists:
            commands, role = get_guest_commands(), enums.Role.GUEST
            _, arg = self._parse_command(msg.text)
            if arg == self._admin_secret_key:
                commands, role = get_admin_commands(), enums.Role.ADMIN

            await self._repo.add_user(chat_id, role)

            await bot.set_my_commands(commands, BotCommandScopeChat(chat_id=chat_id))
            return await bot.send_message(
                chat_id=chat_id,
                text=WELCOME_MESSAGE
                if role == enums.Role.GUEST
                else
                WELCOME_MESSAGE + "\nВаша роль: АДМИН"
            )
        return await handler(event, data)

    def _msg_is_command_start(self, msg: types.Message) -> bool:
        msg_type = msg.entities[0].type
        if msg_type != MessageEntityType.BOT_COMMAND:
            return False

        command, _ = self._parse_command(msg.text)
        return command == COMMAND_START

    @staticmethod
    def _parse_command(text: str) -> tuple[str, str]:
        try:
            command, arg = text.split(maxsplit=1)
        except ValueError:
            command, arg = text, ""
        return command, arg
