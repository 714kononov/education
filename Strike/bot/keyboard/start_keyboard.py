from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types

def startKeyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
            types.InlineKeyboardButton(text="Наш адрес", callback_data="btnAddress"),
            types.InlineKeyboardButton(text="Номер телефона", callback_data="btnNumber"),
            types.InlineKeyboardButton(text="Время работы", callback_data="btnTime"),
            types.InlineKeyboardButton(text="Забронировать", callback_data="btnTable"),
            types.InlineKeyboardButton(text="Отменить бронь", callback_data="btnCancel")
        ]
    keyboard.add(*buttons)
    return keyboard