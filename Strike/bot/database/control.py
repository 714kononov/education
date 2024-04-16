from peewee import DoesNotExist
from bot.database.model import table1, tableCoach, schedule_coach, Regular_customer
from datetime import datetime
from aiogram import types
from bot.core.aiogram import bot
from bot.menus.admin import startadmin
from bot.menus.coach import startcoach



async def save_booking_to_db(data, user_id):
    try:
        date_str = data['date']
        date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        data['date'] = date_obj.strftime("%d/%m/%Y")
        guest_info = "пусто"
        time=datetime.now()
        current_time=datetime.strftime(time,"%d/%m/%Y %H:%M")
        # Получаем или создаем запись в таблице table1
        table1_entry, created = table1.get_or_create(
            user_id=user_id,
            actType=data['game'],
            objNum=data['place'],
            start_date=data['date'],
            start_time=data['time'],
            end_time=data['end_time'],
            period_time=data['period_time'],
            guestName=data['name'],
            guestNumber=data["number"],
            guestinfo=guest_info,
            guestSkidka="0",
            pay='Не оплачено',
            createTime=current_time,
            editTime="0"
        )

        id_key = table1_entry.id_key

        if data['askCoach'] == 'Да':
            tableCoach.create(
                id_key=id_key,
                user_id=user_id,
                nameCoach=data['coach_list'],
                dateTraining=data['date'],
                endtimeTraining=data['end_time'],
                period_time=data['period_time'],
                timeTraining=data['time'],
                objNum=data['place'],
                coachConfirm="Нет",
                guestName=data['name'],
                guestNumber=data['number']
            )

        return True
    except Exception as e:
        print(f"Произошла ошибка при сохранении в базу данных: {str(e)}")
        return False




async def check_reserved_times(start_time, end_time):
    # Запрос в базу данных для проверки бронирования времени
    booked_times = table1.select().where(
        table1.start_time.between(start_time, end_time)
    )
    return [booked.datetime.strftime('%H:%M') for booked in booked_times]


#Пользователь

async def show_user_book(callback_query,user_id):
    try:
        # Попытка получить информацию о бронировании из БД
        booked_table = table1.select().where(table1.user_id == user_id)
        # Проверка наличия записей в таблице
        if booked_table.exists():
            # Если есть записи, отправляем информацию
            for booking in booked_table:
                await bot.send_message(callback_query.from_user.id,f'Номер вашей брони: {booking.id_key}, Ваше Имя: {booking.guestName} , Дата: {booking.start_date}, в {booking.start_time}')
            keyboard=types.InlineKeyboardMarkup()
            buttons=[
                types.InlineKeyboardButton(text="В главное меню",callback_data="btnCancel"),
                types.InlineKeyboardButton(text="Удалить бронь", callback_data='btnDelBook')
            ]
            keyboard.add(*buttons)
            await bot.send_message(callback_query.from_user.id, "Что желаете сделать?",reply_markup=keyboard)
        else:
            # Если бронирований нет, отправляем сообщение
            await bot.send_message(callback_query.from_user.id,'Бронирований нет')

    except DoesNotExist:
        # Обработка случая, когда записей в БД нет
        await callback_query.answer('Бронирований нет')


async def show_all_bookings(callback_query, user_id):
    try:
        # Получаем все брони из БД
        print('UserDelete')
        bookings = table1.select().where(table1.user_id == user_id)
        if bookings.exists():
            # Создаем клавиатуру
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            for booking in bookings:
                # Добавляем кнопку с датой бронирования
                button_text = f"Бронь {booking.id_key}, {booking.start_date}"
                button_callback = f"btndeleteuser:{booking.id_key}:{booking.user_id}"  # Можно использовать ID брони для callback_data
                keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=f"{button_callback}"))

            delete_all = types.InlineKeyboardButton(text="Удалить все", callback_data='btndeleteall')
            cancel = types.InlineKeyboardButton(text="Отмена", callback_data='btnCancel')

            keyboard.add(delete_all)
            keyboard.add(cancel)

            await bot.send_message(callback_query.from_user.id, "Выберите бронь:", reply_markup=keyboard)
        else:
            await callback_query.answer("Бронирований нет")
    except DoesNotExist:
        await callback_query.answer("Бронирований нет")


async def deletefromdball(callback_query, user_id):
        deleteall = table1.select().where(table1.user_id == user_id)
        for booking in deleteall:
            booking.delete_instance()  # Удаляем каждую запись
        await bot.send_message(callback_query.from_user.id, "Все записи удалены")


async def delete_booking_from_user(callback_query, booking_id, user_id):
    try:
        booking_to_delete = table1.get((table1.user_id == user_id) & (table1.id_key == booking_id))
        booking_to_delete.delete_instance()
        await bot.send_message(callback_query.from_user.id, "Вы успешно отменили бронь!")
        await delete_booking_from_user_in_tablecoach(callback_query, booking_id, user_id)
    except table1.DoesNotExist:
        await bot.send_message(callback_query.from_user.id, "Бронь(и) не найдена")

async def delete_booking_from_user_in_tablecoach(callback_query, booking_id, user_id):
    try:
        booking_to_delete1 = tableCoach.get(tableCoach.id_key == booking_id)
        booking_to_delete1.delete_instance()
        await bot.send_message(callback_query.from_user.id, "Выша тренировка с тренером была отменена")
    except tableCoach.DoesNotExist:
        return 1



#Тренер
async def delete_booking(callback_query, booking_id,source):
    try:
        coach_id = callback_query.from_user.id

        if source == "брони":
            booking_to_delete_coach = tableCoach.get(tableCoach.id_key == booking_id)  
            message='Вашу бронь отменил тренер!'
            await bot.send_message(booking_to_delete_coach.user_id,message)
        else:
            booking_to_delete_coach = schedule_coach.get(schedule_coach.id_key == booking_id)

        # Удаляем запись из tableCoach
        booking_to_delete_coach.delete_instance()
        await bot.send_message(coach_id, "Бронь удалена")

    except tableCoach.DoesNotExist or table1.DoesNotExist or schedule_coach.DoesNotExist:
        await bot.send_message(coach_id, "Бронь(и) не найдена")
        await startcoach(callback_query)




async def confirm_booking(callback_query, booking_id, user_id):
    coach_id = callback_query.from_user.id

    # Получение бронирования для подтверждения
    booking_to_confirm = tableCoach.get(id_key=booking_id)

    # Обновление записи в базе данных
    booking_to_confirm.coachConfirm = 'Подтверждено'
    booking_to_confirm.save()

    # Отправить уведомление пользователю
    notification_text = f"Ваше бронирование на {booking_to_confirm.dateTraining} {booking_to_confirm.timeTraining} было подтверждено тренером."
    await bot.send_message(user_id, notification_text)

    # Отправить уведомление тренеру
    await bot.send_message(coach_id, "Бронь подтверждена")
    await confirm_coach(callback_query, booking_id)







async def confirm_coach(callback_query, booking_id):
    tableCoach.update(coachConfirm="Подтверждено").where(tableCoach.id_key == booking_id).execute()
    await startcoach(callback_query)

async def delete_from_admin(callback_query, number_delete):
    try:
        booking = table1.get(table1.id_key == number_delete)
        booking.delete_instance()
        await bot.send_message(callback_query.from_user.id, f"Бронь №{number_delete} успешно удалена")
        user_id = booking.user_id
        await bot.send_message(user_id, "Ваша бронь удалена администратором!")
        await startadmin(callback_query)
    except table1.DoesNotExist:
        await bot.send_message(callback_query.from_user.id, f"Бронь №{number_delete} не найдена")

async def add_note_db(callback_query, data):
    booking_number = data['number_to_note']
    note = data['note']
    try:
        booking = table1.get(table1.id_key == booking_number)
        booking.guestinfo = note
        booking.editTime = datetime.now()
        booking.save()
        await bot.send_message(callback_query.from_user.id, f"Заметка успешно добавлена к брони №{booking_number}")
        await startadmin(callback_query)
    except table1.DoesNotExist:
        await bot.send_message(callback_query.from_user.id, f"Бронь №{booking_number} не найдена")
        await startadmin(callback_query)

async def sale_db(callback_query, data):
    booking_number = data['id_to_sale']
    sale = data['sale']
    try:
        booking = table1.get(table1.id_key == booking_number)
        booking.guestSkidka = sale
        booking.editTime = datetime.now()
        booking.save()
        await bot.send_message(callback_query.from_user.id, f"Скидка успешно добавлена к брони №{booking_number}")
        await startadmin(callback_query)
    except table1.DoesNotExist:
        await bot.send_message(callback_query.from_user.id, f"Бронь №{booking_number} не найдена")
        await startadmin(callback_query)


async def save_coach_shedule_to_db(message, data,user_id):
    try:
        if user_id==889603507:
            data['coach_name']="Егор"

        new_schedule = schedule_coach.create(
            coachName=data['coach_name'],
            objNum=data['place'],
            dateTraining=data['time_for_schedule'],
            timeTraining=data['time'],
            endtimeTraining=data['end_time'],
            period_time = data['period_time'],
            nameUser=data['name'],
            numberUser=data['guest_number']
        )

        booking_id = new_schedule.id_key
        await bot.send_message(message.from_user.id, f"Тренировка успешно записана! ID Бронирования: {booking_id}")
        await startcoach(message)
    except Exception as e:
       print(f"Ошибка при сохранении в бд coach: {str(e)}")
       await bot.send_message(message.from_user.id,"Произошла ошибка")
       await startcoach(message)



async def add_regular_customer_to_db(callback_query,data):
    try:
     Regular_customer.create(userName=data['regular_name'],userNumber=data['regular_number'])
     await bot.send_message(callback_query.from_user.id,f"Вы успешно добавили постоянного клиента {data['regular_name']}")
    except:
        print(f'Ошибка при сохранении данных в БД Regular_Customer: {str(e)}')


async def check_regular_customer(callback_query, data):
    select_number = data['number']
    try:

        record = Regular_customer.get(Regular_customer.userNumber == select_number)
        if record is None:
            return 0
        else:
            sale = table1.select().where(table1.guestNumber == select_number).first()
            if sale:
                sale.guestSkidka = 4
                sale.save()
                print(f'Обновлена скидка у постоянного клиента с номером {select_number}')
            else:
                print(f'Не найдена запись о постоянном клиенте с номером {select_number}')
    except Regular_customer.DoesNotExist:
        return 0
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")

async def delete_from_remainder(callback_query,user_id_key):
    bookings=table1.select().where(table1.id_key == user_id_key)
    user_id=bookings.user_id
    bookings.delete_instance()
    await bot.send_message(user_id,"Ваша бронь была отменена! Денежные средства вернутся в течении 7 рабочих дней!")
