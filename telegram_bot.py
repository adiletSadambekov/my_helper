from config import API_TOKEN, comands
from parser import PageParse
from func_db import DatabaseInterface

import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types



logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




async def  mailings(for_sleep): #send a message to users
    while True:
        times = PageParse().get_items_times()
        chat_id = DatabaseInterface().get_chat_id()
        if chat_id:
            for chat_id in chat_id:
                await bot.send_message(chat_id[0], '\n\n'.join(times))
        await asyncio.sleep(for_sleep)



@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    form = message.from_user
    add = DatabaseInterface().add_user(form.id, form.username, form.first_name, message.chat.id)
    if add:
        await message.reply(add[1])
    else:
        await message.reply(add[1])


@dp.message_handler(commands=['unsubscribe'])
async def unsub(message: types.Message):
    uns = DatabaseInterface().not_active(message.from_user.id)
    if uns:
        await message.reply(uns[1])
    else:
        await message.reply('Happened error')


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.reply(f"I can fulfill folowing comands: {comands}")



@dp.message_handler(commands='time')
async def get_times(message: types.Message):
    times = PageParse().get_items_times()
    await message.reply('\n'.join(times))

@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply(f"Hello {message.from_user.first_name}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(mailings(30))
    executor.start_polling(dp, skip_updates=True)