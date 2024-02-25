from aiogram.fsm.state import StatesGroup, State


class Conversation(StatesGroup):
    active = State()
