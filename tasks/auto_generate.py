from datetime import datetime
import logging
import pytz
import asyncio

from data import config

from utills.generate_images import generate_for_items
from parser.parser import ParsingNTimes, ItemsParse


logging.getLogger('App.tasks.auto_generate')

async def generate_image(time_of_generate: datetime):
    logger = logging.getLogger('App.tasks.auto_generate.generate_image')
    first_started = True
    one_turn = 86400
    while True:
        if first_started:
            '''
            namazes_times = ParsingNTimes().formatter_for_image()
            generate_for_items(1, '\n\n'.join(namazes_times))
            '''
            now = datetime.now(pytz.timezone(config.BISHKEK_TZ))
            diffirence = time_of_generate - now
            first_started = False
            await asyncio.sleep(diffirence.seconds)
        else:
            try:
                namazes_times = ParsingNTimes().formatter_for_image()
                generate_for_items(1, '\n\n'.join(namazes_times)) 
                logger.info('Times is updates')
            except Exception as e:
                logger.exception(e)
            await asyncio.sleep(one_turn)