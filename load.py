from data import config

from aiogram import Bot, types, Dispatcher

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
