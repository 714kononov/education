from bot.core.aiogram import bot, dp
from bot.menus.start_menus import show_table, getnumber, startmenu, choose_game, time_gameplay
from bot.menus.send_avaibles import send_avaibles_today_day, send_available_times, time_15
from aiogram.dispatcher import FSMContext
from datetime import datetime

#перенести по смыслу в main_handler
@dp.callback_query_handler(text='goback1')
async def go_back_1(callback_query):
    await callback_query.answer()
    await startmenu(callback_query)

@dp.callback_query_handler(text='goback2')
async def go_back_2(callback_query):
    await callback_query.answer()
    user_id=callback_query.from_user.id
    await choose_game(user_id)

@dp.callback_query_handler(text='goback3')
async def go_back_3(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await send_avaibles_today_day(callback_query,data)

@dp.callback_query_handler(text='goback4')
async def go_back_4(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        data['date'] = datetime.strptime(data['date'], '%d/%m/%Y').date()
        await send_available_times(callback_query, data)

@dp.callback_query_handler(text='goback5')
async def go_back_5(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await time_gameplay(callback_query,data)


@dp.callback_query_handler(text='goback6')
async def go_back_6(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        await show_table(callback_query, data, state)
