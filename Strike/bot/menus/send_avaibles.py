from calendar import calendar
from datetime import timedelta
from aiogram import types
from aiogram.types import CallbackQuery
from bot.core.aiogram import bot
from datetime import datetime


MAX_TABLE_COUNT_RUSSIAN_BILLIARDS = 6
MAX_TABLE_COUNT_POOL = 4
MAX_TABLE_COUNT = 10

async def send_available_times(callback_query, data):
    start_time, end_time = "", ""
    if data["day"] == 'пт':
        start_time = "12:00"
        end_time = "23:00"
        night_time1 = "00:00"

    if data["day"] == 'сб':
        start_time = "10:00"
        end_time = "23:00"
        night_time1 = "00:00"

    elif data["day"] == 'вс':
        start_time = "10:00"
        end_time = "23:00"
        night_time1 = "00:00"
    else:
        start_time = "12:00"
        end_time = "23:00"

    # Преобразование строковых представлений времени в объекты datetime
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")
    weekday = datetime.strptime(data['date'], '%d/%m/%Y')
    current_hour = (datetime.now().hour + 1) % 24  # Гарантирует, что значение остается в диапазоне 0-23
    current_datetime = datetime(year=weekday.year, month=weekday.month, day=weekday.day, hour=current_hour,
                                minute=weekday.minute)

    is_today = datetime.now().date() == weekday.date()

    if is_today:
        current_time = max(current_time, current_datetime)
    current_time = datetime(
        year=weekday.year,
        month=weekday.month,
        day=weekday.day,
        hour=current_time.hour,
        minute=current_time.minute
    )
    end_time = datetime(
        year=weekday.year,
        month=weekday.month,
        day=weekday.day,
        hour=end_time.hour,
        minute=end_time.minute
    )
    if end_time.hour == 0 and weekday.day == calendar.monthrange(weekday.year, weekday.month)[1]:
        next_month = weekday.replace(day=1, month=weekday.month + 1)

        # Проверяем, изменяется ли год при переходе на следующий месяц
        if next_month.month > 12:
            next_month = next_month.replace(month=1, year=next_month.year + 1)

        end_time = datetime(
            year=next_month.year,
            month=next_month.month,
            day=1,  # Начало следующего месяца
            hour=end_time.hour,
            minute=end_time.minute
        )
    else:
        # Это в пределах текущего месяца
        end_time = datetime(
            year=weekday.year,
            month=weekday.month,
            day=weekday.day,
            hour=end_time.hour,
            minute=end_time.minute
        )
    if end_time.hour == 0:
        end_time += timedelta(days=1)

    if data['day'] == "пятница" or data['day'] == "суббота":
        print(current_time, end_time)
        print("Ночное время:", night_time1)
    elif data['day'] == "воскресенье":
        print(current_time, end_time, "Ночное время: ", night_time1)
    else:
        print(current_time, end_time)

    # Инициализация массива для хранения доступного времени
    available_time_main = []

    # Заполнение массива доступного времени, начиная с текущего времени
    while current_time <= end_time:
        formatted_time = current_time.strftime("%H:%M")
        available_time_main.append(formatted_time)
        current_time += timedelta(hours=1)

    if data['day'] == "пятница" or data['day'] == "суббота":
        available_time_main.append(night_time1)
    if data["day"] == "воскресенье":
        available_time_main.append(night_time1)

    # Создание кнопок для доступного времени
    keyboard_time = types.InlineKeyboardMarkup(row_width=4)
    buttons_time = []
    current_time = datetime.now().strftime("%H:%M")
    for time in available_time_main:
        buttons_time.append(types.InlineKeyboardButton(text=f"{time}", callback_data=f"btnHour:{time}"))
    if not available_time_main:
        await bot.send_message(callback_query.from_user.id, "Извините, нет доступного времени на выбранный день.")
        await send_avaibles_today_day(callback_query, data)
        return
    keyboard_time.add(*buttons_time)
    cancel = types.InlineKeyboardButton(text="В главное меню", callback_data="goback1")
    back_button = types.InlineKeyboardButton("Вернуться назад", callback_data="goback3")
    keyboard_time.add(back_button)
    keyboard_time.add(cancel)
    await bot.send_message(callback_query.from_user.id, "Вы успешно выбрали дату! Теперь выберете время:",
                           reply_markup=keyboard_time)
    await callback_query.answer()

async def send_avaibles_today_day(callback_query: CallbackQuery,data):
        keyboardBook = types.InlineKeyboardMarkup(row_width=2)
        today = datetime.now()
        weekdays = []
        for i in range(15):
            date = today + timedelta(days=i)
            weekdays.append(date.strftime("%a"))
        today_date = datetime.now()
        dateWeekdays = []
        for i in range(15):
            date = today_date + timedelta(days=i)
            dateWeekdays.append(date.strftime("%d/%m"))
        buttonsBook = []
        for i in range(15):
            book = types.InlineKeyboardButton(text=f"{dateWeekdays[i]},{weekdays[i]}",callback_data=f"btnShowDate:{dateWeekdays[i]}:{weekdays[i]}")
            buttonsBook.append(book)

        cancel=types.InlineKeyboardButton(text="В главное меню", callback_data="'goback1'")
        back_button = types.InlineKeyboardButton("Вернуться назад", callback_data="goback2")
        keyboardBook.add(*buttonsBook)
        keyboardBook.add(cancel)
        keyboardBook.add(back_button)
        if data.get('game') == " 1":
            await bot.send_message(callback_query.from_user.id,"Отлично!Теперь выберете дату:   ", reply_markup=keyboardBook)
        else:
            await bot.send_message(callback_query.from_user.id, "Отлично!Теперь выберете дату:   ",reply_markup=keyboardBook)

async def time_15(callback_query,data):
    if data['time'] in ["00:00", "01:00"]:
        date_obj = datetime.strptime(data["date"], "%d/%m/%Y")
        date_obj += timedelta(days=1)
        data['date'] = date_obj.strftime("%d/%m/%Y")

    current_time = datetime.strptime(data["time"], "%H:%M")
    time_buttons = []
    for _ in range(2):
        time_buttons.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    keyboard_time = types.InlineKeyboardMarkup(row_width=2)
    for time in time_buttons:
        keyboard_time.add(types.InlineKeyboardButton(text=f"{time}", callback_data=f"btnCurrentTime:{time}"))
    back_button = types.InlineKeyboardButton("Вернуться назад", callback_data='goback4')
    cancel = types.InlineKeyboardButton(text="В главное меню", callback_data="goback1")
    keyboard_time.add(back_button, cancel)
    await bot.send_message(callback_query.from_user.id, "Выберете время:", reply_markup=keyboard_time)


