import datetime
import calendar
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from main import bot

async def generate_calendar(year, month):
    # Получаем текущую дату
    today = datetime.date.today()
    
    # Создаем клавиатуру для календаря
    calendar_kb = InlineKeyboardMarkup(row_width=7)
    
    # Получаем первый день месяца и количество дней в месяце
    _, days_in_month = calendar.monthrange(year, month)
    
    # Заполняем клавиатуру днями месяца, удаляем прошедшие дни
    for day in range(1, days_in_month + 1):
        if datetime.date(year, month, day) >= today:
            calendar_kb.insert(InlineKeyboardButton(f"{day}", callback_data=f"getDay:{day}"))
    
    return calendar_kb

async def print_calendar(callback_query):
    # Получаем текущую дату
    now = datetime.datetime.now()
    year, month = now.year, now.month

    # Получаем название текущего месяца
    month_name = datetime.date(year, month, 1).strftime("%B")

    # Генерируем клавиатуру для текущего месяца
    calendar_current_month = await generate_calendar(year, month)
    

    # Собираем текст сообщения
    message_text = f"Выберите дату:\n\n{month_name}\n\n"
    
    # Отправляем сообщение с календарем текущего месяца и кнопкой перехода к следующему месяцу
    chat_id = callback_query.from_user.id

    await bot.send_message(chat_id, message_text, reply_markup=calendar_current_month)
    
   


