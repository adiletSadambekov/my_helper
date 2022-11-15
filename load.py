from data import config

from aiogram import Bot, types, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
