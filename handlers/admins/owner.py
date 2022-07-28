from load import dp

from db.models import Users
from utills.admins_tools import save_users_json

from aiogram import types
from data import config 
from db.base_db_funcs import ForAdmin
from sqlalchemy import create_engine


@dp.message_handler(text='/get_users')
async def get_all_users(message: types.Message):
    engine = create_engine(config.PATH_DB)
    db = ForAdmin(engine)
    owner = db.query(Users).where(Users.id_user == message.id).scalar()
    if owner and owner.permession == 'owner':
        users_in_json = save_users_json()
        if users_in_json != False:
            file = open('data' + config.LIST_USERS, 'rb')
            await message.reply_documnet(file)
        else:
            await message.reply('Что-то пошло не так')
    else:
        await message.reply('У вас нет прав на эту команду')