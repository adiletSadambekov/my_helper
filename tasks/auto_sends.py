from db.base_db_funcs import UsersBaseFunctions, CityesBaseFunctions
from data import config

from datetime import time as time_model

from utills.utills import get_interval
from utills.notifyes import notify_owner
from utills.base_messages import get_items_message
from utills.notifyes import notify_owner

import asyncio
import logging
from aiogram import Dispatcher
from sqlalchemy import create_engine

path_log = 'App.tasks.auto_sends'

logging.getLogger(path_log)



async def sends_times(dp: Dispatcher, time_for_sends: time_model):
    logger = logging.getLogger(path_log + '.sends_times')
    first_started = True
    tornover = config.TURNOVER
    engine = create_engine(config.PATH_DB, echo=False)
    while True:
        try:
            if first_started:
                interval = get_interval(time_for_sends, config.BISHKEK_TZ)
                first_started = False
                await asyncio.sleep(interval.seconds)
            else:
                db_user = UsersBaseFunctions(engine)
                db_city = CityesBaseFunctions(engine)
                cityes = db_city.get_all_cityes()
                for city in cityes:
                    try:
                        users_in_city = db_user.get_all_users_by_city(city.id)
                        if users_in_city:
                            text_message = get_items_message(city.id)
                            for user in users_in_city:
                                try:
                                    await dp.bot.send_message(
                                        user.id_in_tg,
                                        text_message)
                                except Exception as e:
                                    db_user.unsubscribe(user.id)
                                    logger(e)
                    except KeyError as e:
                        notify_owner(dp, config.OWNER_ID,
                        'City is not added in list')
                        logger.exception(e)
                    except Exception as e:
                        notify_owner(dp, config.OWNER_ID,
                        'Unknown error')
                        logger.exception(e)
        except Exception as e:
            logger.exception(e)
        await asyncio.sleep(tornover)
