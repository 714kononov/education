from bot.core.aiogram import bot
from aiogram import types
import datetime
from bot.database.model import table1


correct_password = "1111"

user_states = {}
async def admin_password(message):
    user_id=message.from_user.id
    await bot.send_message(message.from_user.id,"Введите пароль:")
    user_states[user_id] = "awaiting_password"


async def startadmin(callback_query):
    keyboard=types.InlineKeyboardMarkup(row_width=1)
    buttons=[
        types.InlineKeyboardButton(text="Брони на сегодня", callback_data="btnTodayBook"),
        types.InlineKeyboardButton(text="Все брони", callback_data="btnAllBook"),
        types.InlineKeyboardButton(text="Оставить заметку", callback_data="btnAddNote"),
        types.InlineKeyboardButton(text="Добавить пост.клиента", callback_data="btnRegularCustomer"),
        types.InlineKeyboardButton(text="Скидка", callback_data="btnSale")
    ]
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id, "Добро пожаловать в админ-панель!",reply_markup=keyboard)


async def get_booking_today(callback_query):
    admin_name = callback_query.from_user.first_name  # Получаем имя админа
    current_day = datetime.date.today().strftime("%d/%m/%Y")

    if admin_name == "Иван":
        bookings_today = table1.select().where((table1.start_date == current_day) & (table1.objNum == 1))
    elif admin_name == "Егор":
        bookings_today = table1.select().where((table1.start_date == current_day) & (table1.objNum == 2))
    else:
        bookings_today = table1.select().where(table1.start_date == current_day)

    message = "Список бронирований на сегодня:\n"
    for booking in bookings_today:
        message += f"Номер брони: {booking.id_key} \nИмя: {booking.guestName} {booking.start_date} {booking.start_time} Игра:{booking.actType}  № стола:{booking.objNum}\n"

    await bot.send_message(callback_query.from_user.id, message)
    await startadmin(callback_query)


async def create_booking_keyboard(callback_query, page_number):
    user_id = callback_query.from_user.id
    page_size = 10
    start_idx = page_number * page_size
    end_idx = (page_number + 1) * page_size

    current_datetime = datetime.datetime.now().strftime("%d/%m/%Y")

    query = table1.select().order_by(table1.start_date)
    total_count = query.count()

    if start_idx >= total_count:
        await bot.send_message(callback_query.from_user.id, "Брони закончились.")
        return

    records = query.offset(start_idx).limit(page_size)

    for show in records:
        if show.start_date < current_datetime:  # Проверка на прошедшую дату
            continue

        date_info = f"№{show.id_key} Дата: {show.start_date}\nВремя:{show.start_time} \nТелефон: {show.guestNumber}"

        # Создайте сообщение с текстом и прикрепленной кнопкой
        message_text = f"Список бронирований:\n{date_info}"
        message_keyboard = types.InlineKeyboardMarkup(row_width=1)
        message_button = types.InlineKeyboardButton(text="Удалить", callback_data=f"btnConfirm:{show.id_key}")
        message_keyboard.add(message_button)

        # Отправьте сообщение
        await bot.send_message(user_id, message_text, reply_markup=message_keyboard)

    prev_page = page_number - 1
    next_page = page_number + 1

    if start_idx > 0:
        go_back = types.InlineKeyboardButton(text="Назад", callback_data=f"btnShowNext:{prev_page}")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(go_back)
        await bot.send_message(user_id, "Выберите действие:", reply_markup=keyboard)

    if end_idx < total_count:
        go_forward = types.InlineKeyboardButton(text="Вперед", callback_data=f"btnShowNext:{next_page}")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.insert(go_forward)
        await bot.send_message(user_id, "Выберите действие:", reply_markup=keyboard)

    cancel = types.InlineKeyboardButton(text="В главное меню", callback_data='btnMainAdmin')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(cancel)
    await bot.send_message(user_id, "Выберите действие:", reply_markup=keyboard)


async def yes_no(callback_query, number_delete):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Да",callback_data=f'btnDeleteAdmin: {number_delete}'),
        types.InlineKeyboardButton(text="Нет", callback_data="btnMainAdmin")
    ]
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id,f"Вы уверены что хотите удалить бронь {number_delete}",reply_markup=keyboard)

async def show_all_bookings_with_notes(callback_query):
    # Получите все записи из базы данных
    bookings = table1.select()
    if bookings:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons=[]

        for booking in bookings:
            buttons.append(types.InlineKeyboardButton(text=f"Бронь №{booking.id_key}, Дата: {booking.start_date}, Время: {booking.start_time}", callback_data=f"btnSendNote:{booking.id_key}"))
        keyboard.add(*buttons)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="btnMainAdmin")
        keyboard.add(back_button)

        await bot.send_message(callback_query.from_user.id, "Выберите запись для добавления заметки:", reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, "Нет доступных записей для добавления заметок.")



async def add_sale(callback_query):
    sales = ["День рождения", "Студент", "Пенсионер"]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = []

    for sale in sales:
        button = types.InlineKeyboardButton(text=sale, callback_data=f'btnSale:{sale}')
        buttons.append(button)
    cancel=types.InlineKeyboardButton(text="В главное меню",callback_data='btnMainAdmin')
    keyboard.add(*buttons)
    keyboard.add(cancel)
    await bot.send_message(callback_query.from_user.id, "Выберите категорию скидки:", reply_markup=keyboard)

async def show_all_bookings_with_sale(callback_query):
    today = datetime.datetime.now()
    today_1 = today.strftime("%d/%m/%Y")
    bookings = table1.select().where(table1.start_date == today_1)
    if bookings:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons=[]

        for booking in bookings:
            buttons.append(types.InlineKeyboardButton(text=f"Бронь №{booking.id_key}, Дата: {booking.start_date}, Время: {booking.start_time}", callback_data=f"btnSaleConfirm:{booking.id_key}"))
        keyboard.add(*buttons)
        back_button = types.InlineKeyboardButton(text="Назад", callback_data="btnMainAdmin")
        keyboard.add(back_button)

        await bot.send_message(callback_query.from_user.id, "Выберите запись для добавления скидки:", reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, "Нет доступных записей для добавления заметок.")


async def choose_game_for_admin(callback_query):
    games=["Бильярд","Боулинг"]
    keyboard=types.InlineKeyboardMarkup(row_width=2)
    for game in games:
        keyboard.add(types.InlineKeyboardButton(text=f"{game}",callback_data=f'btnMainAdmin:{game}'))
    await bot.send_message(callback_query.from_user.id, "Выберите админ панель: ")

