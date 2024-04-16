import asyncio
from aiogram import executor

from bot.chech_pay_new_books.fuctions import main_pay_or_not
from bot.core.aiogram import bot
from bot.handlers import dp
from bot.send_remainder.remainder import main

if __name__ == '__main__':
    print('start')
    async def on_startup(dp):
        asyncio.create_task(main())
        asyncio.create_task(main_pay_or_not())
    executor.start_polling(dp, on_startup=on_startup)
    print('stop')