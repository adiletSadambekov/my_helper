
from data import config

import logging

from load import dp
from aiogram import types
from sqlalchemy import create_engine

logging.getLogger('App.handlers.admin.admin_commands')

"""
db_admin = ForAdmin(create_engine(config.PATH_DB, echo=False))
db_user = ForUsers(create_engine(config.PATH_DB, echo=False))


@dp.message_handler(text='/admin_commands')
async def able_admins_commands(message: types.Message):
    is_admin = db_admin.is_admin(message.from_users.id)
    if is_admin != True:
        await message.answer('У вас нет прав для этой комманды')
    else:
        commands = config.LIST_ADMINS_COMMANDS
        await message.reply(commands)



@dp.message_handler(commands='send_all')
async def send_all(message: types.Message):
    logger = logging.getLogger('App.handlers.admin.admin_commands.send_all')
    user = message.from_user
    if db_admin.is_admin(user.id) != True:
        await message.answer('Вы не являетес админом для этой команды')
    else:
        users = db_user.get_all_active()
        for u in users:
            try:
                await dp.bot.send_message(u.id_user,
                    f'Автор: <a href="{user.username}">\
                        {user.full_name}</a>\n{message.text[10:]}')
            except Exception as e:
                logger.exception(e)

"""