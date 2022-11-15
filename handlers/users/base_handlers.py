from db.base_db_funcs import UsersBaseFunctions
from handlers.users_states import UserSubscribe
from handlers.users.key_boards import create_cityes_buttons
from aiogram.types import ReplyKeyboardRemove

from utills.base_messages import get_items_message

from db.exceptions import ErrorAddUser

from aiogram.dispatcher import FSMContext

from sqlalchemy import create_engine

from aiogram import types
from load import dp

from data import config
import logging


logging.getLogger('App.handlers.users.base_handlers')

engine = create_engine(config.PATH_DB, echo=False)

db_user = UsersBaseFunctions(engine)

@dp.message_handler(text='/start')
async def first_greeting(message: types.Message):
    text = config.GREETINGS_TEXT
    try:
        db_user.add_user(message.from_user)
        await message.answer(text % (message.from_user.full_name))
    except ErrorAddUser:
        await message.answer(config.HELP_TEXT)


@dp.message_handler(text='/help')
async def for_help(message: types.Message):
    await message.answer(config.HELP_TEXT)


@dp.message_handler(text='/subscribe')
async def subscribe(message: types.Message):
    user = db_user.get_user(int(message.from_user.id))
    if user:
        markup = create_cityes_buttons()
        await message.reply('Выберите ваш город', reply_markup=markup)
        await UserSubscribe.city_id.set()
    else:
        await message.reply('Что-то пошло не так, попробуйте чуть позже или обратитесь к админу')


@dp.message_handler(state=UserSubscribe.city_id)
async def get_city(message: types.Message, state: FSMContext):
    logger = logging.getLogger('App.handlers.users.base_handlers.get_city')
    try:
        await state.update_data(id_city = message.text)
        response = await state.get_data()
        get_id_city = int(response['id_city'][0])
        subscribe_user = db_user.subscribe(message.from_user,
        id_city=get_id_city)
        if subscribe_user:
            await message.reply('Вы успешно подписались на рассылку', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Что-то пошло не так, попробуйте позже')
        await state.finish()
    except ValueError:
        markup = create_cityes_buttons()
        await message.answer('Выбран не существующий город. \nВыберите ваш город снова', reply_markup=markup)
        await UserSubscribe.city_id.set()
    except Exception as e:
        logger.exception(e)


@dp.message_handler(text='/unsubscribe')
async def unsubscribe(message: types.Message):
    logger = logging.getLogger('App.handlers.users.default_commands.unsubscribe')
    try:
        user = db_user.get_user(message.from_user.id)
        if user.is_active == False:
            await message.answer('Вы и так не подписаны на рассылки')
        else:
            db_user.unsubscribe(user.id_in_tg)
            await message.answer('Вы успешно отписались от рассылок')
    except Exception as e:
        logger.exception(e)


@dp.message_handler(text='/get_times')
async def get_times(message: types.Message):
    logger = logging.getLogger('App.handlers.users.base_handlers.get_times')
    try:
        user = db_user.get_user(message.from_user.id)
        items_message = get_items_message(str(user.id_city))
        await message.answer(items_message)
    except Exception as e:
        logger.exception(e)


