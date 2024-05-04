# handlers.py

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import time
import datetime
from main import dp,bot
from functions import start_function,contacts_function,choose_sex_function,choose_service_function
from functions import calendar_function,get_time_function

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await start_function(message)

@dp.callback_query_handler(lambda c: c.data.startswith('getContacts'))
async def contacts(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await contacts_function(callback_query)
        await start_function(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('getOrder'))
async def get_order_step_1(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await choose_sex_function(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('getType'))
async def get_order_step_2(callback_query: CallbackQuery, state: FSMContext):
    print(f'{callback_query.data}')
    await callback_query.answer()
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        choose = sp[1]
        data['sex'] = choose
    await choose_service_function(callback_query,data)

@dp.callback_query_handler(lambda c: c.data.startswith('getDate'))
async def get_order_step_2(callback_query: CallbackQuery, state: FSMContext):
    print(f'{callback_query.data}')
    await callback_query.answer()
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        choose = sp[1]
        data['type'] = choose
    await calendar_function(callback_query)
    

# Обработчик нажатий на кнопки
@dp.callback_query_handler(lambda c: c.data.startswith('getDay'))
async def process_day_button(callback_query: types.CallbackQuery,state: FSMContext):
    print(f'{callback_query.data}')
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        now = datetime.datetime.now()
        if sp[1] > "1" and sp[1] < "9":
            formated = now.strftime(f'0{sp[1]}/%m/%Y')
        else:
            formated = now.strftime(f'{sp[1]}/%m/%Y')
        data['date'] = formated
        print(f'{formated}')
        await get_time_function(callback_query,data)

@dp.callback_query_handler(lambda c: c.data.startswith('getTime'))
async def get_time(callback_query: types.CallbackQuery,state: FSMContext):
    print(f'{callback_query.data}')
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        data['time'] = f'{sp[1]}:00'   

    

  

   

            