from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types
from datetime import datetime,timedelta


def date():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    # День недели
    today = datetime.now()
    weekdays = []
    for i in range(15):
        date = today + timedelta(days=i)
        weekdays.append(date.strftime("%A"))
    # Функция получения сегодняшнего числа
    today_date = datetime.now()
    dateWeekdays = []
    for i in range(15):
        date = today_date + timedelta(days=i)
        dateWeekdays.append(date.strftime("%d/%m"))
    buttons = []
    for i in range(15):
        book = types.InlineKeyboardButton(text=f"{dateWeekdays[i]},{weekdays[i]}",callback_data=f"btnTimeBook:{dateWeekdays[i]}:{weekdays[i]}")
        buttons.append(book)
        keyboard.add(*buttons)
    return keyboard