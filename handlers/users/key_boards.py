from data import config

from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)

from db.base_db_funcs import CityesBaseFunctions
from sqlalchemy import create_engine

def create_cityes_buttons() -> ReplyKeyboardMarkup:
    engine = create_engine(config.PATH_DB)
    cityes = CityesBaseFunctions(engine).get_all_cityes()
    if cityes:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True)
        for i in cityes:
            markup.add(KeyboardButton(
                str(i.id) + ' - ' + i.full_name))
        return markup
    else:
        return False