from main import bot
import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from aiogram_calendar import print_calendar

async def start_function(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons =  [
        types.InlineKeyboardButton(text = "Записаться",callback_data="getOrder"),
        types.InlineKeyboardButton(text = "Контакты",callback_data="getContacts"),
        types.InlineKeyboardButton(text = "Мои записи",callback_data="getyMyOrder")
    ]
    keyboard.add(*buttons)
    await bot.send_message(message.from_user.id,text = "Добро пожаловать!",reply_markup=keyboard)

async def contacts_function(callback_query):
    await bot.send_message(callback_query.from_user.id,text = "Часы работы: ")
    await bot.send_message(callback_query.from_user.id,text = "Адрес: ")
    await bot.send_message(callback_query.from_user.id,text = "Контакты: ")

#Блок бронирования
async def choose_sex_function(callback_query):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text = "Мужчинам", callback_data = "getType:1"),
        types.InlineKeyboardButton(text = "Девушкам", callback_data = "getType:2")
    ]
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id,text = "Выберите категорию: ",reply_markup=keyboard)
    

#Выбор услуги
async def choose_service_function(callback_query,data):
    keyboard = types.InlineKeyboardMarkup(row_width = 1)
    if (data['sex'] == '1'):
        buttons = [
            types.InlineKeyboardButton(text = "Стрижка",callback_data = "getDate:1"),
            types.InlineKeyboardButton(text = "Окрашивание",callback_data = "getDate:2")
        ]
    elif (data['sex'] == '2'):
        buttons = [
            types.InlineKeyboardButton(text = "Стрижка",callback_data = "getDate:1"),
            types.InlineKeyboardButton(text = "Окрашивание",callback_data = "getDate:2"),
            types.InlineKeyboardButton(text = "Ламинирование",callback_data = "getDate:3"),
            types.InlineKeyboardButton(text = "Ламинирование бровей",callback_data = "getDate:4")
        ]
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id,text ="Выберите желаемую услугу: ",reply_markup = keyboard)


async def calendar_function(callback_query):
    await print_calendar(callback_query)

async def get_time_function(callback_query,data):
    current_hour = datetime.datetime.now().hour
    current_date = datetime.datetime.now()
    date = current_date.strftime("%d/%m/%Y")
    if data['date'] == date:
        if current_hour < 20:
            hours_available = [hour for hour in range(current_hour + 1, 21)]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for hour in hours_available:
                button_text = f"{hour}:00"
                button_callback_data = f"getTime:{hour}"
                keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=button_callback_data))
            await callback_query.message.answer("Выберите время для записи: ", reply_markup=keyboard)
        else:
            await callback_query.message.answer("К сожалению на сегодня времени для записей больше нет.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Back", callback_data="back")))
    else:
        current_hour = 8
        if current_hour < 20:
            hours_available = [hour for hour in range(current_hour + 1, 21)]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for hour in hours_available:
                button_text = f"{hour}:00"
                button_callback_data = f"getTime:{hour}"
                keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=button_callback_data))
            await callback_query.message.answer("Выберите время для записи: ", reply_markup=keyboard)
    

async def choose_maker_function(callback_query,data):
    user_id = callback_query.from_user.id
    photo  = ''
    descriptin = '123'
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text = 'Катя', callback_query = "getUserName")
    ]    
    keyboard.add(buttons)
    await bot.send_message(user_id, text = descriptin, reply_markup= keyboard)