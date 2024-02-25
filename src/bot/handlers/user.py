from aiogram import Router, types
from aiogram.filters import Command, CommandStart

router = Router()

START_MESSAGE = """Приветствуем вас вновь в боте гостевого дома 'Елена'!
Доступные команды описаны в /help"""

HELP_MESSAGE = """Команды бота:

/start - Запустить бота
/help - Получить справку о боте
/booking - Забронировать номер
"""


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(text=START_MESSAGE)


@router.message(Command("help"))
async def help_(message: types.Message) -> None:
    await message.answer(text=HELP_MESSAGE)
