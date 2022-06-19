"""from data import API_TOKEN, text_for_help
from func_db import DataBaseORM, DBForItems

import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types



logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



async def  mailings(time_sleep): # send a message to users
    DBForItems().update_items()
    while True:

        times = DBForItems().get_items()
        chat_id = DataBaseORM().get_all_active()
        if chat_id:
            for chat_id in chat_id:
                try:
                    await bot.send_message(chat_id.id_user, times.items)
                except:
                    DataBaseORM().unsubscribe(chat_id.id_user)
        await asyncio.sleep(time_sleep)




@dp.message_handler(commands=['start']) # function for subscribe
async def start_bot(message: types.Message):
    form = message.from_user
    add = DataBaseORM().add_user(form.id, form.username, form.first_name)
    await message.reply(add)



@dp.message_handler(commands=['unsubscribe']) # function for unsubscribe
async def unsub(message: types.Message):
    uns = DataBaseORM().unsubscribe(message.from_user.id)
    await message.reply(uns)


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.reply(text_for_help)



@dp.message_handler(commands='time')
async def get_times(message: types.Message):
    times = DBForItems().get_items()
    await message.reply(times.items)

@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply(f"Hello {message.from_user.first_name}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(mailings(30))
    executor.start_polling(dp, skip_updates=True)"""