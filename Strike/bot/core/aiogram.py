from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import locale
from bot.core.config import TOKEN


# Меню
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', '✅ начать с самого начала'),
        types.BotCommand('help', '❔ помощь')
    ])

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
locale.setlocale(locale.LC_ALL, 'ru_RU')

