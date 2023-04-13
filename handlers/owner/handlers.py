from load import dp
from data import config
from .states import AddinAdminState, AddingCityState
from db.db_owner_funcs import OwnerDBFunctions

from db.base_db_funcs import UsersBaseFunctions
from db.models import User

from aiogram import types
from aiogram.dispatcher import FSMContext

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.exceptions import ErrorParametrs


logging.getLogger(config.APP_LOG_FILE + '.handlers.owner.handlers')

@dp.message_handler(commands='add_city')
async def add_city(message: types.Message):
    if message.from_user.id == config.OWNER_ID:
        await message.answer('Ведите название города на латыне')
        await AddingCityState.name.set()
    else:
        await message.answer('У вас нет доступа к данной команде')

@dp.message_handler(state=AddingCityState.name)
async def get_name_city(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer('Введите название города в кирилице')
    await AddingCityState.full_name.set()

@dp.message_handler(state=AddingCityState.full_name)
async def add_new_city(message: types.Message, state: FSMContext):
    logger = logging.getLogger(config.APP_LOG_FILE + '.handlers.owner.handlers.add_new_city')
    await state.update_data(full_name = message.text)
    get_data = await state.get_data()
    try:
        engine = create_engine(config.PATH_DB)
        city = OwnerDBFunctions(engine).add_city(
            get_data['name'], get_data['full_name']
        )
        if city:
            await message.answer(
                'Город успешно добавлен и получил id: ' + str(city.id))
        else:
            message.answer('Что-то пошло не так')
        await state.finish()
    except Exception as e:
        logger.exception(e)


@dp.message_handler(commands='appoint_admin')
async def apoint_admin(message: types.Message):
    if message.from_user.id == config.OWNER_ID:
        await message.reply('Напишите имя пользователя')
        await AddinAdminState.username.set()
    else:
        await message.reply('У вас нет достаточно прав для этой комманды')


@dp.message_handler(state=AddinAdminState.username)
async def adding_admin(message: types.Message, state: FSMContext):
    logger = logging.getLogger(
        config.APP_LOG_FILE + '.handlers.owner.handlers.adding_admin')
    try:
        await state.update_data(username=message.text)
        username = await state.get_data()
        Session = sessionmaker(create_engine(config.PATH_DB))
        s = Session()
        user = s.query(User).where(User.username == username['username']).scalar()
        if user:
            if user.id_acces_level == config.ID_ADMIN_LEVEL:
                await message.reply(
                    f"Пользователь {user.username} уже является админом")
            else:
                user.id_acces_level = config.ID_ADMIN_LEVEL
                s.commit()
                await message.reply(user.full_name + ' назначен админом')
        else:
            await message.reply('Такого пользователя не существует')
    except Exception as e:
        logger.exception(e)
    finally:
        s.close()
        await state.finish()