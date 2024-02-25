from datetime import date, timedelta
from typing import Any

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Calendar, Cancel, Back, Button, Row, Next, CalendarConfig
from aiogram_dialog.widgets.text import Const, Format

from bot.common.booking import validate_number_of_people
from bot.consts import ADMIN_ID
from bot.states.booking import CreateBookingForm

router = Router()

ON_START_BOOKING_TEXT = """
Для создания брони необходимо заполнить форму.
"""

YEAR = timedelta(days=365)


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager, selected_date: date):
    if manager.dialog_data['check-in'] == "-":
        manager.dialog_data['check-in'] = selected_date.isoformat()

        manager.dialog_data['check-in-active'] = "✔️"
        manager.dialog_data['check-out-active'] = "✍️"

        await callback.answer("Отлично! Теперь выберете дату отъезда")
        return

    check_in_date = date.fromisoformat(manager.dialog_data['check-in'])
    if check_in_date > selected_date:
        await callback.answer("Вы не можете уехать раньше того дня, в который заехали :)")
        return

    manager.dialog_data['check-out'] = selected_date.strftime("%Y-%m-%d")
    manager.dialog_data['dates_are_field'] = True


async def on_cancel_booking(callback: CallbackQuery, button: Button, manager: DialogManager):
    bot: Bot = manager.middleware_data["bot"]
    msg = callback.message

    await bot.delete_message(msg.chat.id, msg.message_id)
    await msg.answer("Вы отменили процесс бронирования")


CANCEL_BOOKING = Cancel(
    Const("Отменить бронь"),
    id="cnl_bkg",
    on_click=on_cancel_booking
)

BACK = Back(
    text=Const("Назад"),
)


async def on_booking_start(_: Any, manager: DialogManager):
    manager.dialog_data['check-in'] = "-"
    manager.dialog_data['check-in-active'] = "✍️"
    manager.dialog_data['check-out'] = "-"
    manager.dialog_data['check-out-active'] = "✖️️"


async def reset_dates(_: CallbackQuery, __: Button, manager: DialogManager):
    await on_booking_start(_, manager)
    manager.dialog_data['dates_are_field'] = False


async def complete_booking(callback: CallbackQuery, __: Button, manager: DialogManager, **kwargs):
    bot: Bot = manager.middleware_data["bot"]

    await bot.send_message(
        ADMIN_ID,
        "Новая бронь:\n\n"
        f"Кол-во человек: {manager.dialog_data['number_of_people']}\n"
        f"Даты: {manager.dialog_data['check-in']} - {manager.dialog_data['check-out']}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Начать диалог",
                        callback_data=f"start_conversation-{callback.from_user.id}"
                    )
                ]
            ]
        )
    )

    await bot.delete_message(callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer("Ваша форма направлена администратору. Ожидайте, он скоро свяжется с вами")

    await manager.done()


async def on_number_of_people(msg: types.Message, _, manager: DialogManager, *__):
    bot: Bot = manager.middleware_data["bot"]

    try:
        validate_number_of_people(msg.text)
    except ValueError as e:
        await bot.delete_message(msg.chat.id, msg.message_id - 1)
        await msg.answer(str(e))
    else:
        manager.dialog_data['number_of_people'] = int(msg.text)
        await manager.next()


dialog = Dialog(
    Window(
        Const("Введите количество гостей"),
        TextInput(id="number_of_people", on_success=on_number_of_people),
        CANCEL_BOOKING,
        state=CreateBookingForm.number_of_people,
    ),
    Window(
        Const("Укажите дату заезда и дату отъезда"),
        Format("{dialog_data[check-in-active]} Дата заезда: {dialog_data[check-in]}"),
        Format("{dialog_data[check-out-active]} Дата отъезда: {dialog_data[check-out]}"),
        Calendar(
            id="check_in_out_dates",
            config=CalendarConfig(min_date=date.today(), max_date=date.today() + 2 * YEAR),
            on_click=on_date_selected
        ),
        Row(
            BACK,
            Next(text=Const("Далее"), when=F["dialog_data"]["dates_are_field"])
        ),
        Button(
            id='reset_dates',
            text=Const("Сбросить даты"),
            when=F["dialog_data"]["check-in"].is_not("-"),
            on_click=reset_dates
        ),
        CANCEL_BOOKING,
        state=CreateBookingForm.check_in_out,
    ),
    Window(
        Const("Вы успешно заполнили форму. Отправить ее администратору?"),
        Button(
            text=Const("Отправить"),
            id='complete_bkg',
            on_click=complete_booking
        ),
        Row(
            BACK,
            CANCEL_BOOKING
        ),
        state=CreateBookingForm.complete,
    ),
    on_start=on_booking_start
)


@router.message(Command('booking'))
async def on_start_booking(message: types.Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager):
    await dialog_manager.start(state=CreateBookingForm.number_of_people, data={"bot": bot})
