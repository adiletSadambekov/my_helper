import asyncio
from aiogram import Dispatcher
from data.config import OWNER_ID

import logging

logging.getLogger('App.utills.notify_owner')

async def notify_owner(dp: Dispatcher, user_id: int, text_message: str):
    logger = logging.getLogger('App.utills.notify_owner.utill_notify')
    try:
        await dp.bot.send_message(user_id, text_message)
    except Exception as e:
        logger.exception(e)

async def on_start_bot_owner(dp: Dispatcher): #The fanction notify be bots's owner
    logger = logging.getLogger('App.utills.notify_owner.on_start_bot_owner')
    try:
        await dp.bot.send_message(chat_id=OWNER_ID, text='Bot is started')
    except Exception as e:
        logger.exception(e)

