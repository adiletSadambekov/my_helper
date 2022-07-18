from aiogram import types, Dispatcher

async def set_default_sommands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('subscribe', 'Подписаться на рассылку'),
        types.BotCommand('get_times', 'Получить время прямо сейчас'),
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Получить помощи по боту'),
        types.BotCommand('unsubscribe', 'Отписаться от рассылки'),
    ])