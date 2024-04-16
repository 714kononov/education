from bot.calendar.simple_calendar import  start_calendar
from bot.core.aiogram import bot
from aiogram.types import InputFile
from aiogram import types

from bot.core.states import Guest
from bot.database.model import tableCoach, schedule_coach, Coach_list
import datetime


coach="Да","Нет"
async def ask_coach(callback_query):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text=f"{coach[0]}",callback_data=f'btnInfoCoach:{coach[0]}'),
        types.InlineKeyboardButton(text=f"{coach[1] }",callback_data=f'btnInfoCoach:{coach[1]}')
    ]
    keyboard.add(*buttons)
    cancel = types.InlineKeyboardButton(text="В главное меню", callback_data='goback1')
    goback = types.InlineKeyboardButton(text="Назад", callback_data='goback6')
    keyboard.add(cancel)
    keyboard.add(goback)
    await bot.send_message(callback_query.from_user.id, "Вам нужен тренер?", reply_markup=keyboard)



coach_first="/Users/Shared/first"
coach_second="/Users/Shared/Second"
coach_third="/Users/Shared/Second"
async def startcoach(message):
    keyboard = types.InlineKeyboardMarkup()
    button = [
        types.InlineKeyboardButton(text="Мои брони", callback_data="btnshowbookcoach"),
        types.InlineKeyboardButton(text=f"Мое расписание", callback_data="btnCreateSchedule")
    ]
    keyboard.add(*button)
    await bot.send_message(message.from_user.id, "Добро пожаловать в тренерскую панель!", reply_markup=keyboard)

# Функция для отправки информации о тренерах с кнопками выбора
async def send_coaches_info(user_id,data):
    if data['game']==" 1":
        coachs = Coach_list.select().where(Coach_list.actType == "1")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for coach in coachs:
            button = types.InlineKeyboardButton(text=f"{coach.nameCoach}", callback_data=f"btncheckCoach:{coach.user_id}")
            keyboard.add(button)
        cancel = types.InlineKeyboardButton(text='В главное меню',callback_data='btnCancel')
        goback= types.InlineKeyboardButton(text="Вернутся назад",callback_data='goback1')
        keyboard.add(cancel)
        keyboard.add(goback)
        await bot.send_message(user_id, "Выберите тренера:", reply_markup=keyboard)
    else:
        coachs = Coach_list.select().where(Coach_list.actType == "2")
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for coach in coachs:
            button = types.InlineKeyboardButton(text=f"{coach.nameCoach}", callback_data=f"btncheckCoach:{coach.user_id}")
            keyboard.add(button)
        cancel = types.InlineKeyboardButton(text='В главное меню', callback_data='btnCancel')
        goback = types.InlineKeyboardButton(text="Вернутся назад", callback_data='goback1')
        keyboard.add(cancel)
        keyboard.add(goback)
        await bot.send_message(user_id, "Выберите тренера:", reply_markup=keyboard)


async def access_book_for_coach(callback_query):
    user_id = callback_query.from_user.id
    coach_name="Ошибка имени"
    if user_id==889603507:
        coach_name="Егор"
    if user_id==472921300:
        coach_name="Максим"
    if user_id==6406261742:
        coach_name="Роман"
    if user_id==8896035071:
        coach_name="Иван"

    coach_ids = {
        "Роман": 640626174,
        "Егор": 889603507,
        "Максим": 472921300,
        "Иван": 2
    }

    if coach_name in coach_ids:
        # Извлекаем все бронирования для данного тренера
        coach_bookings = tableCoach.select().where(tableCoach.nameCoach == coach_name)
        coach_bookings_schedule = schedule_coach.select().where(schedule_coach.coachName == coach_name)

        message_text = f"Привет {coach_name}! Ваши брони:\n"
        for booking in coach_bookings:
            message_text += f" Бронь: {booking.id_key}, Дата: {booking.dateTraining},время:{booking.timeTraining} Имя: {booking.guestName}, стол {booking.objNum}, телефон {booking.guestNumber},Статус: {booking.coachConfirm}    \n"
        message_text_schedule= "Ваше рассписание: \n"
        for booking_shedule in coach_bookings_schedule :
            message_text_schedule += f" Бронь: {booking_shedule.id_key}, Дата: {booking_shedule.dateTraining},время: {booking_shedule.timeTraining} Имя: {booking_shedule.nameUser}, стол {booking_shedule.objNum}, телефон {booking_shedule.numberUser}   \n"

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text="Подтвердить", callback_data='btnconfirmbook'),
            types.InlineKeyboardButton(text="Отменить бронь", callback_data='btnshowbooking'),
            types.InlineKeyboardButton(text="В главное меню", callback_data='btnCancelCoach')
        ]
        keyboard.add(*buttons)

        await bot.send_message(user_id, message_text)
        await bot.send_message(user_id, message_text_schedule, reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, "Тренер не найден")
        await startcoach(callback_query)


async def show_coach_delete(callback_query):
    try:
        user_id = callback_query.from_user.id
        coach_name = None # Значение по умолчанию, если ни одно условие не выполняется

        if user_id == 889603507:
            coach_name = "Егор"
        elif user_id == 472921300:
            coach_name = "Максим"
        elif user_id == 640626174:  # Обратите внимание на разные значения user_id
            coach_name = "Роман"

        # Запрос к таблице tableCoach
        bookings_coach = tableCoach.select().where((tableCoach.nameCoach == coach_name) & (tableCoach.source == "брони"))


        # Запрос к таблице schedule_coach
        bookings_schedule = schedule_coach.select().where((schedule_coach.coachName == coach_name) & (schedule_coach.source == "расписание"))

        # Объединение результатов запросов
        bookings = list(bookings_coach) + list(bookings_schedule)

        print(bookings)
        if bookings:
            keyboard = types.InlineKeyboardMarkup(row_width=1)

            for booking in bookings:
                button_text = f"Бронь {booking.id_key} ({booking.source})"
                callback_data = f"btndeleteforcoach:{booking.id_key}:{booking.source}"  # Здесь добавляем id бронирования
                keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
            cancel = types.InlineKeyboardButton(text="В главное меню", callback_data='btnCancelCoach')
            keyboard.add(cancel)

            await bot.send_message(callback_query.from_user.id, "Ваши бронирования:", reply_markup=keyboard)
        else:
            await bot.send_message(callback_query.from_user.id, "У вас нет бронирований.")
            await startcoach(callback_query)
    except Exception as e:
        print(f"Ошибка при получении бронирований: {e}")




async def show_coach_confirm(callback_query):
    try:
        user_id = callback_query.from_user.id
        coach_name = None  # Значение по умолчанию, если ни одно условие не выполняется

        if user_id == 889603507:
            coach_name = "Иван"
        elif user_id == 472921300:
            coach_name = "Максим"
        elif user_id == 640626174:  # Обратите внимание на разные значения user_id
            coach_name = "Роман"

        bookings = tableCoach.select().where(tableCoach.nameCoach == coach_name)

        if bookings.exists():
            keyboard = types.InlineKeyboardMarkup(row_width=1)

            for booking in bookings:
                button_text = f"Бронь {booking.id_key}"
                callback_data = f"btnconfirmcoach:{booking.id_key}:{booking.user_id}"  # Здесь добавляем id бронирования
                keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
            cancel=types.InlineKeyboardButton(text="В главное меню", callback_data='btnCancelCoach')
            keyboard.add(cancel)

            await bot.send_message(callback_query.from_user.id, "Ваши бронирования:", reply_markup=keyboard)
        else:
            await bot.send_message(callback_query.from_user.id, "У вас нет бронирований.")
            await startcoach(callback_query)
    except Exception as e:
        print(f"Ошибка при получении бронирований: {e}")

async def get_calendar(callback_query):
    current_date = datetime.datetime.now()
    year, month = current_date.year, current_date.month
    inline_kb = await start_calendar(year, month)
    await callback_query.message.answer(text='Рассписание на месяц:',reply_markup=inline_kb)


async def time_for_schedule(callback_query):
    start_time = datetime.datetime.strptime("10:00","%H:%M")
    end_time = datetime.datetime.strptime("23:00","%H:%M")
    times = []
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time)
        current_time += datetime.timedelta(hours=1)
    keyboard=types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    for time in times:
        button_time = time.strftime("%H:%M")
        button = types.InlineKeyboardButton(button_time, callback_data=f'btnTimeForCoach:{button_time}')
        buttons.append(button)
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id,"Выберите время для создания брони:",reply_markup=keyboard)

async def current_time_coach(callback_query, data):
    times = datetime.datetime.strptime(data['time'], "%H:%M")
    buttons = []
    for _ in range(2):
        buttons.append(times.strftime('%H:%M'))
        times += datetime.timedelta(minutes=30)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for time in buttons:
        keyboard.add(types.InlineKeyboardButton(text=time, callback_data=f'btnPeriodTime:{time}'))

    cancel = types.InlineKeyboardButton(text="В главное меню", callback_data='btnMainAdmin')
    keyboard.add(cancel)
    await bot.send_message(callback_query.from_user.id, "Выберите конкретное время:", reply_markup=keyboard)


async def choose_table_for_schedule(callback_query):
    tables=[1,2,3,4,5,6,7,8,9]
    keyboard=types.InlineKeyboardMarkup(row_width=2)
    for table in tables:
        keyboard.add(types.InlineKeyboardButton(text=f'стол №{table}',callback_data=f'btnGetPlace:{table}'))
    cancel=types.InlineKeyboardButton(text='В главное меню',callback_data='btnCancelCoach')
    keyboard.add(cancel)
    await bot.send_message(callback_query.from_user.id,"Выберите стол для занятия: ", reply_markup=keyboard)

async def time_training(callback_query,data):
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    time_to_play = ["1", "2 ", "3", "4", "5 ","По факту"]
    for time in time_to_play:
        time_button = types.InlineKeyboardButton(text=f'{str(time)} ', callback_data=f'btnChoosePlaceSchedule:{time}')
        buttons.append(time_button)
    keyboard.add(*buttons)
    await bot.send_message(callback_query.from_user.id, "Выберите время игры: ", reply_markup=keyboard)