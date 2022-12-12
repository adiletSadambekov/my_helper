from aiogram.dispatcher.filters.state import State, StatesGroup

class MessageState(StatesGroup):
    text_message = State()