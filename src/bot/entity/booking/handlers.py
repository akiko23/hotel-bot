from aiogram import Router, types, F, Bot
from aiogram.filters import Command

router = Router()


@router.message(Command('book'))
async def book(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id, "")


@router.message(Command('reservations'))
async def reservations(message: types.Message):
    pass
