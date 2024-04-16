from operator import and_

from aiogram import types
from bot.core.states import Human
from bot.core.aiogram import bot
from bot.database.control import save_booking_to_db, show_all_bookings, show_user_book
from bot.database.model import table1
from datetime import datetime, timedelta
from bot.payment.generate_summ import generate_payment_link


async def choose_game(user_id):
    choose_game=[1,2]
    keyboard=types.InlineKeyboardMarkup(row_width=2)
    buttons=[
        types.InlineKeyboardButton(text="Бильярд",callback_data=f'game: {choose_game[0]}'),
        types.InlineKeyboardButton(text="Боулинг",callback_data=f'game: {choose_game[1]}')
    ]
    cancel=types.InlineKeyboardButton(text="В главное меню",callback_data='goback1')
    keyboard.add(*buttons)
    keyboard.add(cancel)
    await bot.send_message(user_id,"Выберите вид игры: ",reply_markup=keyboard)

async def startmenu(message):
    photo = '/Users/admin/Desktop/ForStrike1.jpg'
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
            types.InlineKeyboardButton(text="Наши контакты", callback_data="btnContact"),
            types.InlineKeyboardButton(text="Забронировать",disable=True, callback_data="btnChooseGame"),
            types.InlineKeyboardButton(text="Мои брони", callback_data="btnShowBook"),
            types.InlineKeyboardButton(text="Узнать цены", callback_data='btnPrice')
        ]
    keyboard.add(*buttons)
    await bot.send_message(message.from_user.id,"Привет!",reply_markup=keyboard)

async def contact(callback_query):
    await bot.send_message(callback_query.from_user.id,
                           "Мы находимся по адресу г.Пенза, ТЦ Суворовский, ул. Суворова, 144А (этаж 0)")
    await bot.send_message(callback_query.from_user.id, "Наш номер телефона:+7 (8412) 23-60-60,+7 (8412) 39-76-16")
    await bot.send_message(callback_query.from_user.id,
                           "Мы работаем:пн-чт 12:00–00:00; пн 12:00–01:00; сб 10:00–01:00; вс 10:00–00:00")
    await callback_query.answer()
    await startmenu(callback_query)

async def getnumber(message):
    chat_chat = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="В главное меню", callback_data="btnCancel"),
    ]
    keyboard.add(*buttons)
    await bot.send_message(chat_id=chat_chat, text="Отлично! Остался последний шаг, введите Ваш номер телефона в формате: 89043235543: ",reply_markup=keyboard)
    await Human.Number.set()

async def time_gameplay(callback_query,data):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    time_to_play = ["1 ", "2 ", "3", "4 ", "5"]
    if data.get('game')==" 1":
        time_to_play = ["1", "2 ", "3", "4", "5 ","По факту"]
        for time in time_to_play:
            time_button = types.InlineKeyboardButton(text=f'{str(time)}', callback_data=f'btntimeGamePlay:{time}')
            buttons.append(time_button)
        keyboard.add(*buttons)
    else:
        for time in time_to_play:
            time_button = types.InlineKeyboardButton(text=f'{str(time)}', callback_data=f'btntimeGamePlay:{time}')
            buttons.append(time_button)
        keyboard.add(*buttons)
    cancel=types.InlineKeyboardButton(text='В главное меню',callback_data='goback1')
    goback = types.InlineKeyboardButton(text='Назад', callback_data='goback4')
    keyboard.add(cancel)
    keyboard.add(goback)
    await bot.send_message(callback_query.from_user.id, "Выберите время игры(в часах): ", reply_markup=keyboard)

async def getname(callback_query):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="В главное меню", callback_data="btnCancel"),
    ]
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id, text="Теперь введите Ваше имя: ",reply_markup=keyboard)
    await Human.Name.set()

from aiogram import types

async def show_table(callback_query, data, state):
    try:
        user_id = callback_query.from_user.id
        selected_date = data.get('date')
        selected_time = data.get('time')
        selected_duration = data.get('end_time')
        act_type = data.get('game')  # Assuming actType is present in your data

        # Modify the query based on actType
        booked_tables = table1.select(table1.objNum).where(
            (table1.start_date == selected_date) &
            (table1.start_time <= selected_time) &
            (table1.end_time >= selected_duration) &
            (table1.actType == act_type)
        )

        booked_table_numbers = [booking.objNum for booking in booked_tables]
        all_tables = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        all_track=["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        print(booked_table_numbers)
        if data.get('game')==' 1':
            available_tables = [table for table in all_tables if table not in booked_table_numbers]
            print(available_tables)
        if data.get('game')==' 2':
            available_track = [table for table in all_track if table not in booked_table_numbers]
            print(available_track)


        keyboard = types.InlineKeyboardMarkup(row_width=True)
        if data.get('game')==' 1':
            for table in available_tables:
                keyboard.add(types.InlineKeyboardButton(text=str(table), callback_data=f"btnPlace:{table}"))
        if data.get('game')==' 2':
            for track in available_track :
                keyboard.add(types.InlineKeyboardButton(text=str(track), callback_data=f"btnPlace:{track}"))


        cancel = types.InlineKeyboardButton(text="В главное меню", callback_data="btnCancel")
        btnBack = types.InlineKeyboardButton(text="Назад", callback_data="goback5")

        keyboard.add(btnBack)
        keyboard.add(cancel)

        await bot.send_message(user_id, 'Выберите место для игры:', reply_markup=keyboard)
    except:
        await startmenu(callback_query)

async def go_to_pay(callback_query, data):
    game_type = data.get('game')  # 1 для бильярда, 2 для боулинга
    start_time = datetime.strptime(data.get('time'), "%H:%M")
    day_of_week = datetime.strptime(data.get('date'), "%d/%m/%Y").weekday()
    amount=0
    if game_type == ' 1':
        if 0 <= day_of_week <= 3:  # Пн-Чт
            if 12 <= start_time.hour < 18:
                amount = 250
            elif 18 <= start_time.hour < 24:
                amount = 350
        elif day_of_week == 4:  # Пт
            if 12 <= start_time.hour < 18:
                amount = 250
            elif 18 <= start_time.hour < 1:
                amount = 350
        elif day_of_week == 5:  # Сб
            if 10 <= start_time.hour < 1:
                amount = 350
        elif day_of_week == 6:  # Вс
            if 10 <= start_time.hour < 24:
                amount = 350
    elif game_type == ' 2':
        if 0 <= day_of_week <= 3:  # Пн-Чт
            if 12 <= start_time.hour < 17:
                amount = 500
            elif 17 <= start_time.hour < 24:
                amount = 700
        elif day_of_week == 4:  # Пт
            if 12 <= start_time.hour < 17:
                amount = 700
            elif 17 <= start_time.hour < 1:
                amount = 900
        elif day_of_week == 5:  # Сб
            if 10 <= start_time.hour < 1:
                amount = 900
        elif day_of_week == 6:  # Вс
            if 10 <= start_time.hour < 24:
                amount = 900

    else:
        print('не фурычит создание ссылки start_menu/go_to_pay')

    invoice_id = "restorankinza"
    payment_link = await generate_payment_link(amount, invoice_id)

    # Замените 'USER_CHAT_ID' на ID чата с пользователем
    user_chat_id = callback_query.from_user.id

    # Отправка платежной ссылки в чат пользователя
    await bot.send_message(chat_id=user_chat_id, text=f"Оплатить счет: {payment_link}")

async def savedatabase(message,data):

    chat_chat = message.chat.id
    user_id = message.from_user.id
    table1.confirmed_coach="Тренер не нужен!"
    if data.get('game') == " 1":
        await bot.send_message(chat_id=chat_chat,text=f"🎉 Поздравляю! Вы успешно забронировали бильярд  на имя: {data['name']}, {data['date']} числа! 🎉")
        await go_to_pay(message,data)
    else:
        await bot.send_message(chat_id=chat_chat,text=f"🎉 Поздравляю! Вы успешно забронировали боулинг  на имя: {data['name']}, {data['date']} числа! 🎉")
        await go_to_pay(message,data)
    await save_booking_to_db(data, user_id)
    await startmenu(message)



async def show_book(callback_query):
    user_id=callback_query.from_user.id
    await show_user_book(callback_query,user_id)

async def show_booking_keyboard(callback_query):
    user_id=callback_query.from_user.id
    await show_all_bookings(callback_query,user_id)

async def check_booking_pay_or_not(callback_query, user_id):
    try:
        booking = table1.get(table1.user_id == user_id)

        # Проверка, оплачена ли бронь
        if booking.pay == "Не оплачено":
            await bot.send_message(callback_query.from_user.id, "Извините, но вы не оплатили предыдущую бронь!")
            return 0
        else:
            return 1
    except table1.DoesNotExist:
        return 1





