from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from bot.core.aiogram import bot, dp
from bot.core.states import Human
from bot.database.control import show_user_book, deletefromdball, delete_booking, delete_booking_from_user, \
    check_regular_customer, delete_from_remainder
from bot.menus.admin import startadmin
from bot.menus.start_menus import getnumber, \
    savedatabase, contact, startmenu, show_table, show_booking_keyboard, show_book, choose_game, \
    time_gameplay, check_booking_pay_or_not
from bot.menus.coach import ask_coach, send_coaches_info, startcoach
from bot.menus.send_avaibles import send_avaibles_today_day, send_available_times, time_15
from datetime import datetime, timedelta
from bot.database.model import Coach_list


# Обработчики
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await startmenu(message)


user_states_coach = {}
correct_password_coach = "2222"
@dp.message_handler(commands=['coach'])
async def start_for_admin(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Для доступа к функциям бота, введите пароль:")
    user_states_admin[user_id] = "awaiting_password_coach"

@dp.message_handler(lambda message: user_states_admin.get(message.from_user.id) == "awaiting_password_coach")
async def check_password(message: types.Message):
    user_id = message.from_user.id
    if message.text == correct_password_coach:
        await message.answer("Пароль верный. Доступ разрешен.")
        user_states_admin[user_id] = "access_granted_coach"
        await startcoach(message)
        # Здесь можно добавить логику для дальнейших действий после успешного ввода пароля
    else:
        await message.answer("Пароль неверный. Попробуйте еще раз:")
        user_states_admin[user_id] = "awaiting_password_coach"


user_states_admin = {}
correct_password_admin = "1111"
@dp.message_handler(commands=['admin'])
async def start_for_admin(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Для доступа к функциям бота, введите пароль:")
    user_states_admin[user_id] = "awaiting_password_admin"

@dp.message_handler(lambda message: user_states_admin.get(message.from_user.id) == "awaiting_password_admin")
async def check_password(message: types.Message):
    user_id = message.from_user.id
    if message.text == correct_password_admin:
        await message.answer("Пароль верный. Доступ разрешен.")
        user_states_admin[user_id] = "access_granted_admin"
        await startadmin(message)
        # Здесь можно добавить логику для дальнейших действий после успешного ввода пароля
    else:
        await message.answer("Пароль неверный. Попробуйте еще раз:")
        user_states_admin[user_id] = "awaiting_password_admin"

@dp.callback_query_handler(text="btnChooseGame")
async def bowling_or_billiards(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.answer()
    user_id = callback_query.from_user.id
    check_coach = await check_booking_pay_or_not(callback_query, user_id)
    print(f'Проверка оплаты: {check_coach}')
    if check_coach == 1:
        await choose_game(user_id)
    else:
        await startmenu(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('game'))
async def coach(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(f'{callback_query.data}')
        sp = callback_query.data.split(":")
        data['game'] = sp[1]
        await send_avaibles_today_day(callback_query,data)


@dp.callback_query_handler(lambda c: c.data.startswith('btnShowDate'))
async def show_time(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['date']=sp[1]
        print(data['date'])
        data['day']=sp[2]
        current_year = datetime.now().year
        data["date"] = f"{data['date']}/{current_year}"
        await send_available_times(callback_query, data)

@dp.callback_query_handler(lambda c: c.data.startswith('btnHour'))
async def show_current_time(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(f"Выбранный час: {callback_query.data}")
        sp = callback_query.data.split(":")
        data['time'] = f'{sp[1]}:{sp[2]}'
        await time_15(callback_query, data)

@dp.callback_query_handler(lambda c: c.data.startswith('btnCurrentTime'))
async def show_place(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['time']=f"{sp[1]}:{sp[2]}"
        await time_gameplay(callback_query,data)

@dp.callback_query_handler(lambda c: c.data.startswith('btntimeGamePlay'))
async def show_place(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        data['period_time'] = sp[1]
        start_time = datetime.strptime(data['time'], "%H:%M")
        period_delta = timedelta(hours=int(data['period_time']))
        end_time = start_time + period_delta
        data['end_time'] = end_time.strftime("%H:%M")
        await show_table(callback_query, data, state)


@dp.callback_query_handler(lambda c: c.data.startswith('btnPlace'))
async def await_name_or_coach(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['place']=sp[1]
        await ask_coach(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('btnInfoCoach'))
async def await_name_or_coach(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        user_id = callback_query.from_user.id
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['askCoach'] = sp[1]
        if data['askCoach'] == "Да":
            await send_coaches_info(user_id,data)
        else:
            # запрос к бд с тренерами со списками
            await get_name_from_user(callback_query,state)

@dp.callback_query_handler(lambda c: c.data.startswith('btncheckCoach'))
async def  check_coach(callback_query:types.CallbackQuery,state:FSMContext):
    async with state.proxy() as data:
        await callback_query.answer()
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['coach_list']=sp[1]
        await get_name_from_user(callback_query, state)

@dp.callback_query_handler(lambda c: c.data.startswith('getName'))
async def get_name_from_user(message:types.Message,state: FSMContext):
    keyboard=types.InlineKeyboardMarkup()
    cancel=types.InlineKeyboardButton(text="В главное меню",callback_data='btnCancel')
    keyboard.add(cancel)
    await bot.send_message(message.from_user.id, "Введите ваше имя:",reply_markup=keyboard)
    await Human.Name.set()



@dp.message_handler(state=Human.Name)
async def get_number_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "/start":
            await startmenu(message)
        else:
            data["name"] = message.text
            print(f"Name: {message.text}")
            await getnumber(message)



@dp.message_handler(state=Human.Number)
async def save_to_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "/start":
            await state.finish()
            await startmenu(message)
        try:
            # Пробуем преобразовать текст сообщения в int
            number = int(message.text)
            # Проверяем, что это 11-значное число
            if len(str(number)) == 11:
                print(f"Number: {message.text}")
                data["number"] = message.text
                print(data['number'])
                await state.finish()
                await savedatabase(message, data)
                await check_regular_customer(message,data)
            else:
                await bot.send_message(message.from_user.id, text="Вы ввели не 11 значное число, попробуйте еще раз")
                await getnumber(message)
        except ValueError:
            # Если не удалось преобразовать в int, значит, это не число
            await bot.send_message(message.from_user.id, text="Вы ввели не число, попробуйте ещё раз")
            await getnumber(message)



@dp.callback_query_handler(text="btnCancelBook")
async def DeleteHuman(callback_query: CallbackQuery,state:FSMContext):
        await state.finish()
        await show_user_book(callback_query)

    # inline
# Адрес/Телефон/Часы работы
@dp.callback_query_handler(text="btnContact")
async def contacts(callback_query: CallbackQuery):
    await callback_query.answer()
    await contact(callback_query)

 # Отмена
@dp.callback_query_handler(text="btnCancel")
async def cancel_action(callback_query: CallbackQuery):
        await start(callback_query)
        await callback_query.answer()


@dp.callback_query_handler(text="btnCancelCoach")
async def cancel_action(callback_query: CallbackQuery):
    await startcoach(callback_query)
    await callback_query.answer()

@dp.callback_query_handler(text="btnPrice")
async def show_price(message:types.Message):
    await message.answer()
    await bot.send_message(message.from_user.id,"Цены для бильярда:")
    await bot.send_message(message.from_user.id,"🗓понедельник-четверг с 12:00 до 18:00 стоимость 250 рублей в час💵, с 18:00 до 00:00 - 350 рублей в час💵")
    await bot.send_message(message.from_user.id,"🗓пятница с 12:00 до 18:00 стоимость 250 рублей в час💵, с 18:00 до 01:00 - 350 рублей в час💵")
    await bot.send_message(message.from_user.id,"🗓суббота с 10:00 до 01:00 стоимость 350 рублей в час💵")
    await bot.send_message(message.from_user.id,"🗓воскресенье с 10:00 до 00:00 стоимость 350 рублей в час💵")
    await bot.send_message(message.from_user.id,"Цены для боулинга:")
    await bot.send_message(message.from_user.id,"🗓понедельник-четверг с 12:00 до 17:00 стоимость 500 рублей в час💵, с 17:00 до 00:00 - 700 рублей в час💵")
    await bot.send_message(message.from_user.id,"🗓пятница с 12:00 до 17:00 стоимость 700 рублей в час💵, с 17:00 до 01:00 - 900 рублей в час💵")
    await bot.send_message(message.from_user.id, "🗓суббота с 10:00 до 01:00 стоимость 900 рублей в час💵")
    await bot.send_message(message.from_user.id, "🗓воскресенье с 10:00 до 00:00 стоимость 900 рублей в час💵")
    await start(message)


@dp.callback_query_handler(text='btnShowBook')
async def ShowBook(callback_query: CallbackQuery):
    await callback_query.answer()
    await show_book(callback_query)

@dp.callback_query_handler(text='btnDelBook')
async def ShowBook(callback_query: CallbackQuery):
    await callback_query.answer()
    await show_booking_keyboard(callback_query)

@dp.callback_query_handler(text='btndeleteall')
async def delete_all(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await deletefromdball(callback_query,user_id)
    await start(callback_query)

@dp.callback_query_handler(text='deletefromdb')
async def delete(callback_query: CallbackQuery):
    print(12)
    booking_id = callback_query.data.replace('deletefromdb:', '')
    await delete_booking(callback_query, booking_id)

@dp.callback_query_handler(lambda c: c.data.startswith('btndeleteuser'))
async def delete_for_coach(callback_query, state: FSMContext):
    async with state.proxy() as data:
        await callback_query.answer()
        print(f'{callback_query.data}')
        sp = callback_query.data.split(":")
        booking_id = sp[1]
        user_id = sp[2]# Получаем id бронирования из callback_query.data
        data['id'] = booking_id  # Сохраняем id бронирования в state для дальнейшего использования
        await delete_booking_from_user(callback_query, booking_id,user_id)


@dp.callback_query_handler(text="btnRemainder")
async def btnRemainder(callback_query: CallbackQuery,state:FSMContext):
    async with state.proxy as data:
        print(f'{callback_query}')
        sp=callback_query.data.split(":")
        user_id_key=sp[1]
        await delete_from_remainder(callback_query,user_id_key)