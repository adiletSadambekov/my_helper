from db.base_db_funcs import ForUsers

from sqlalchemy import create_engine

from aiogram import types
from load import dp

from data import config
import logging

logging.getLogger('App.handlers.users.default_commands')

engine = create_engine(config.PATH_DB)

@dp.message_handler(text='/start')
async def first_greeting(message: types.Message):
    text = config.GREETINGS_TEXT
    await message.answer(text % (message.from_user.full_name))


@dp.message_handler(text='/help')
async def for_help(message: types.Message):
    await message.answer(config.HELP_TEXT)


@dp.message_handler(text='/subscribe')
async def subscribe(message: types.Message):
    logger = logging.getLogger('App.handlers.users.default_commands.subscribe')
    try:
        sub = ForUsers(engine).add_user(message.from_user)
        if sub:
            await message.answer('Вы успешно подписались на рассылку')
        if sub == 3:
            await message.answer('Вы снова подписались на рассылку')
        if sub == 2:
            await message.answer('Вы и так подписаны')
    except Exception as e:
        logger.exception(e)


@dp.message_handler(text='/unsubscribe')
async def unsubscribe(message: types.Message):
    logger = logging.getLogger('App.handlers.users.default_commands.unsubscribe')
    try:
        user = ForUsers(engine).unsubscribe(message.from_user.id)
        if user:
            await message.answer('Вы успешно отписались от рассылок')
        if user == None:
            await message.answer('Вы и так не подписаны на рассылки')
        else:
            await message.answer('Что-то пошло не так. Попробуйте чуть позже')
    except Exception as e:
        logger.exception(e)


@dp.message_handler(text='/get_times')
async def get_its_time(message: types.Message):
    img = 'static/images/done/current_items.jpg'
    await message.answer_photo(types.InputFile(img))
