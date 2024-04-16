import asyncio
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.core.aiogram import bot
from bot.database.model import table1

async def send_reminders():
    try:
        current_time = datetime.now()
        reminder_time = current_time + timedelta(minutes=30)
        reminder_time_str = reminder_time.strftime("%d/%m/%Y %H:%M")
        print(reminder_time_str)
        print("оповещение!")
        will_booking = table1.select().where(
            (table1.start_date + ' ' + table1.start_time) == reminder_time_str
        )
        for booking in will_booking:
            user_id = booking.user_id
            print(will_booking.id_key,will_booking.start_time)
            notification_text = f"Ваша бронь начнется через 30 минут. Пожалуйста, не опаздывайте  \nВ случае опоздания более чем 15 минут ваша бронь отменится!"
            await bot.send_message(user_id,"Подтвердите пожалуйста бронь!")
            keyboard=InlineKeyboardMarkup(row_width=True)
            yes=InlineKeyboardButton(text="Да, я приду",callback_data="btnCancel")
            no=InlineKeyboardButton(text="Нет, я не смогу",callback_data=f'btnRemainder:{user_id}')
            keyboard.add(yes)
            keyboard.add(no)
            await bot.send_message(user_id, notification_text,reply_markup=keyboard)

    except table1.DoesNotExist:
        print("Предстоящих бронирований нет")

async def schedule_reminders():
    while True:
        await send_reminders()
        await asyncio.sleep(60)

async def main():
    await asyncio.create_task(schedule_reminders())





