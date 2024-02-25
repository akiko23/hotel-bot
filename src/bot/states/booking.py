from aiogram.fsm.state import StatesGroup, State


class CreateBookingForm(StatesGroup):
    number_of_people = State()
    check_in_out = State()
    complete = State()
