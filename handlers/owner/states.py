from aiogram.dispatcher.filters.state import State, StatesGroup

class AddingCityState(StatesGroup):
    name = State()
    full_name = State()


class AddinAdminState(StatesGroup):
    username = State()