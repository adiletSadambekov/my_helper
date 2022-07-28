from datetime import datetime
from utills.notifyes import on_start_bot_owner

from data import config
import logging

logger = logging.getLogger('App')
logger.setLevel(logging.INFO)
file_name = logging.FileHandler(config.APP_LOG_FILE)
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
file_name.setFormatter(formatter)
logger.addHandler(file_name)

async def on_start(dp):
    logger = logging.getLogger('App.on_start')
    from utills.set_bot_commands import set_default_sommands
    try:
        await set_default_sommands(dp)
        await on_start_bot_owner(dp)
    except Exception as e:
        logger.exception(e)



if __name__ == '__main__':
    from handlers import dp
    from tasks.auto_sends import send_items
    from tasks.auto_generate import auto_generate_image
    from aiogram import executor
    import asyncio

    point_datetime = datetime(2022, 7, 29, 2, 27)
    try:
        logger.info('Bot is started')
        loop1 = asyncio.get_event_loop()
        loop1.create_task(send_items(dp, 20))
        loop1.create_task(auto_generate_image(point_datetime))
        executor.start_polling(dp, on_startup=on_start)
        logger.info('Bot is disabled')
    except Exception as e:
        logger.exception(e)
    