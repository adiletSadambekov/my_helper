from db.base_db_funcs import ForUsers
from data import config

import asyncio
import logging
from aiogram import types, Dispatcher
from sqlalchemy import create_engine

logging.getLogger('App.tasks.auto_sends')


async def send_items(dp: Dispatcher, interval: int):
    logger = logging.getLogger('App.tasks.auto_sends.send_items')
    try:
        while True:
            engine = create_engine(config.PATH_DB, echo=False)
            img = 'static/images/done/current_items.jpg'
            db = ForUsers(engine)
            users = ForUsers(engine).get_all_active()
            if users != None and users != False:
                for i in users:
                    try:
                        await dp.bot.send_photo(i.id_user, types.InputFile(img))
                    except:
                        await db.unsubscribe(i.id_user)
            await asyncio.sleep(interval)
    except Exception as e:
        logger.exception(e)
