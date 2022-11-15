from datetime import time as time_model
import json
import logging
import asyncio
import random
import time

from data import config

from utills.utills import get_interval
from parser.parser import ParsingNTimes
from db.models import City

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.getLogger('App.tasks.auto_generate')


async def save_times(time_for_update: time_model):
    one_turn = 86400
    logger = logging.getLogger('App.tasks.auto_generate.save_times')
    first_started = True
    one_turn = 86400
    engine = create_engine(config.PATH_DB, echo=False)
    while True:
        if first_started:
            interval = get_interval(time_for_update, config.BISHKEK_TZ)
            Session = sessionmaker(engine)
            s = Session()
            try:
                cityes = s.query(City).all()
                times_in_dict = {}
                for city in cityes:
                    try:
                        random_intrval = random.randint(1, 5)
                        items = ParsingNTimes().get_to_dict(city.name)
                        times_in_dict[city.id] = items
                        time.sleep(random_intrval)
                    except Exception as e:
                        logger.exception(e)
                with open(config.PATH_TIMES_FILE, 'w') as f:
                    json.dump(times_in_dict, f)
            except Exception as e:
                logger.exception(e)
            first_started = False
            await asyncio.sleep(interval.seconds)
        else:
            s = Session()
            cityes = s.query(City).all()
            times_in_dict = {}
            for city in cityes:
                try:
                    random_intrval = random.randint(1, 5)
                    items = ParsingNTimes().get_to_dict(city.name)
                    times_in_dict[city.name] = items
                    time.sleep(random_intrval)
                except Exception as e:
                    logger.exception(e)
            with open(config.PATH_TIMES_FILE, 'w') as f:
                json.dump(items, f)
            await asyncio.sleep(one_turn)
            