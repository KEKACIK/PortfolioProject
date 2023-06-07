from aiogram.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    mailing_text = State()
    mailing_submit = State()
