import asyncio
from handlers import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

async def on_startup(dp):
    await bot.send_message(chat_id='889603507', text="Бот запущен")

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
