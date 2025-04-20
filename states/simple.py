from aiogram.filters.state import StatesGroup, State


class GetName(StatesGroup):
    name = State()


class HowAnswer(StatesGroup):
    about = State()