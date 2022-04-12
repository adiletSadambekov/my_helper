from config import API_TOKEN
from parser import PageParse
from func_db import Database_interface

import logging

from aiogram import Bot, Dispatcher, executor, types



logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    form = message.from_user
    add = Database_interface().add_user(form.id, form.username, form.first_name, 1)
    if add:
        await message.reply(add[1])
    else:
        await message.reply(add[1])

@dp.message_handler(commands='time')
async def get_times(message: types.Message):
    times = PageParse().get_items_times()
    await message.reply('\n'.join(times))

@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply(f"Hello {message.from_user.first_name}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
