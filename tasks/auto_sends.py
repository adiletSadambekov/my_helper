from db.base_db_funcs import ForUsers
from data import config

from datetime import datetime as dt
import datetime
import pytz

import asyncio
import logging
from aiogram import types, Dispatcher
from sqlalchemy import create_engine

logging.getLogger('App.tasks.auto_sends')


async def send_items(dp: Dispatcher, time_of_send: datetime.time):
    logger = logging.getLogger('App.tasks.auto_sends.send_items')
    first_start = True
    one_turn = 86400
    while True:
        if first_start:
            time_zone = pytz.timezone(config.BISHKEK_TZ)
            now = dt.now(time_zone)
            point_dt = dt(
                now.year, now.month, now.day,
                time_of_send.hour, time_of_send.minute
            )
            point_datetime = time_zone.localize(point_dt)
            interval = point_datetime - now
            first_start = False
            await asyncio.sleep(interval.seconds)
        else:
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
            await asyncio.sleep(one_turn)
