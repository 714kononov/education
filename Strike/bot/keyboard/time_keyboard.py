from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types
from bot.database.control import get_times


def Time():
    if data["day"] == "пятница":
        time_main_Friday = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00",
                            "22:00", "23:00", "00:00"]
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i in range(13):
            buttons.append(
                types.InlineKeyboardButton(text=f"{time_main_Friday[i]}", callback_data=f"InfoHuman:{time_main_Friday[i]}"))
        keyboard.add(*buttons)
        return keyboard

    elif data["day"] == "суббота":
        # Бронь Суббота
        time_main_Saturday = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                              "20:00", "21:00", "22:00", "23:00", "00:00"]
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i in range(15):
            buttons.append(types.InlineKeyboardButton(text=f"{time_main_Saturday[i]}",
                                                                    callback_data=f"InfoHuman:{time_main_Saturday[i]}"))
        keyboard.add(*buttons)
        return keyboard
    elif data["day"] == "воскресенье":
        time_main_Sunday = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
                            "20:00", "21:00", "22:00", "23:00"]
        keyboard = types.InlineKeyboardMarkup(row_width=4)
        buttons = []
        for i in range(14):
            buttons.append(
            types.InlineKeyboardButton(text=f"{time_main_Sunday[i]}", callback_data=f"InfoHuman:{time_main_Sunday[i]}"))
            keyboard.add(*buttons)
        return keyboard

