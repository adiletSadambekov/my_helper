from data import config
from db.base_db_funcs import UsersBaseFunctions

from .states import MessageState

import logging

from load import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy import create_engine

logging.getLogger('App.handlers.admin.admin_commands')


engine = create_engine(config.PATH_DB)
users_db = UsersBaseFunctions(engine)


@dp.message_handler(commands='admin_commands')
async def able_admins_commands(message: types.Message):
    user = users_db.get_user(user_id=message.from_user.id)
    if int(user.acces_level) > config.ADMIN_LEVEL:
        commands = config.LIST_ADMINS_COMMANDS
        await message.answer(commands)
    else:
        await message.answer('У вас нет прав для этой комманды')




@dp.message_handler(commands='send_all')
async def send_all(message: types.Message):
    logger = logging.getLogger('App.handlers.admin.admin_commands.send_all')
    user = users_db.get_user(user_id=message.from_user.id)
    if int(user.acces_level.level) >= config.ADMIN_LEVEL:
        await MessageState.text_message.set()
        await message.reply('Напишите ваше сообщение...')
    else:
        await message.reply('У вас недостаточно прав для этой комманды')



@dp.message_handler(state=MessageState.text_message)
async def send_message(message: types.Message, state: FSMContext):
    try:
        logger = logging.getLogger(
            'App.handlers.admin.admin_commands.message_handler')
        await state.update_data(message = message.text)
        text = await state.get_data()
        users = users_db.get_all()
        if users:
            text_mess = 'От @' + message.from_user.username + '\n' + text['message']
            for user in users:
                try:
                    await dp.bot.send_message(user.id_in_tg, text_mess)
                except Exception as e:
                    users_db.unsubscribe(username=user.username)
                    logger.exception(e)
        await state.finish()
        await message.reply('Ваше сообщение отправлено всем активным пользователям')
    except Exception as e:
        logger.exception(e)
        await message.reply('Что-то пошдло не так')