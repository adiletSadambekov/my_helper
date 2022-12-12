from aiogram.dispatcher.filters.state import State, StatesGroup


class UserSubscribe(StatesGroup):
    city_id = State()
