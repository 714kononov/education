from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types

def table():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    Button = []
    for i in range(2):
        TableList = types.InlineKeyboardButton(text=f"{table[i]}", callback_data=f"btnBook:{table[i]}")
        Button.append(TableList)
    keyboard.add(*Button)
    return keyboard