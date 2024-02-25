from aiogram.types import BotCommand

COMMON_COMMANDS = [
    BotCommand(
        command='start',
        description='Перезапустить бота'
    ),
    BotCommand(
        command='help',
        description='Посмотреть справку о боте'
    ),
]


def get_guest_commands():
    return [
        *COMMON_COMMANDS,
        BotCommand(
            command='booking',
            description='Забронировать номер'
        )
    ]


def get_admin_commands():
    return COMMON_COMMANDS
