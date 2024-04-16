from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from bot.core.aiogram import dp, bot
from bot.core.states import Guest
from bot.database.control import delete_booking, confirm_booking, save_coach_shedule_to_db
from bot.database.model import tableCoach
from bot.menus.coach import access_book_for_coach, show_coach_delete, show_coach_confirm, get_calendar, \
    time_for_schedule, current_time_coach, choose_table_for_schedule, startcoach, time_training



@dp.callback_query_handler(text="btnshowbookcoach")
async def access_book(callback_query):
    await callback_query.answer()
    await access_book_for_coach(callback_query)


@dp.callback_query_handler(text="btnCreateSchedule")
async def create_schedule(callback_query):
    await callback_query.answer()
    await get_calendar(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('btnChecDateForSchedule'))
async def check_coach_schedule(callback_query, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        sp = callback_query.data.split(":")
        data['act'] = sp[1]
        data["day"] = sp[4]
        data['year'] = datetime.now().year
        data['month'] = datetime.now().month
        date = f"{data['day']}/{data['month']}/{data['year']}"
        data["coach_date"] = date
        print(f'{date}')
        await get_time_from_coach(callback_query,state)

@dp.callback_query_handler(lambda c: c.data.startswith('btnTimeForCoach'))
async def get_time_from_coach(callback_query, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        if len(sp) >= 3:
            data['time'] = f'{sp[1]}:{sp[2]}'
            print(data['time'])
            await current_time_coach(callback_query, data)
        else:
            print("Неправильный формат data['time']")


@dp.callback_query_handler(lambda c: c.data.startswith('btnPeriodTime'))
async def get_time_from_coach(callback_query, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['time'] = f'{sp[1]}:{sp[2]}'
        await time_training(callback_query,data)


@dp.callback_query_handler(lambda c: c.data.startswith('btnChoosePlaceSchedule'))
async def get_guest_name_from_coach(callback_query, state:FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        if callback_query.data=="btnChoosePlaceSchedule:По факту":
            data['period_time']=f'1 час + наигранное время'
        else:
            data['period_time']=sp[1]
        await choose_table_for_schedule(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('btnGetPlace'))
async def get_guest_name_from_coach(callback_query, state:FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['place'] = sp[1]

        if data['period_time']=='1 час + наигранное время':
            data['end_time']="Ожидает завершения"
        else:
            start_time = datetime.strptime(data.get("time"), "%H:%M")
            period_delta = timedelta(hours=int(data['period_time']))
            end_time = start_time + period_delta
            data['end_time'] = end_time.strftime("%H:%M")
            print(data['end_time'])

        await bot.send_message(callback_query.from_user.id,"Теперь введите имя Вашего ученика: ")
        await Guest.Name.set()


@dp.message_handler(state=Guest.Name)
async def get_name(message,state:FSMContext):
    async with state.proxy() as data:
        print(f"Name: {message.text}")
        data['name']=message.text
        await bot.send_message(message.from_user.id,"Теперь номер телефона ученика: ")
        await Guest.Number.set()

@dp.message_handler(state=Guest.Number)
async def get_number_from_coach_to_user(message,state:FSMContext):
    async with state.proxy() as data:
        print(f'Number Guest:{message.text}')
        data['guest_number'] = message.text
        user_id=message.from_user.id
        await state.finish()
        await save_coach_shedule_to_db(message,data,user_id)


@dp.callback_query_handler(text="btnshowbooking")
async def show_book(callback_query):
    await callback_query.answer()
    await show_coach_delete(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith('btndeleteforcoach'))
async def delete_for_coach(callback_query, state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(f'{callback_query.data}')
        sp = callback_query.data.split(":")
        booking_id = sp[1]
        print(booking_id)
        data['id'] = booking_id
        source=sp[2]
        data['source'] = sp[2]
        await delete_booking(callback_query,booking_id,source)



@dp.callback_query_handler(lambda c: c.data.startswith('btnconfirmbook'))
async def confirm_for_coach(callback_query, state: FSMContext):
    await callback_query.answer()
    await show_coach_confirm(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith('btnconfirmcoach'))
async def delete_for_coach(callback_query, state: FSMContext):
    async with state.proxy() as data:
        await callback_query.answer()
        print(f'{callback_query.data}')
        sp = callback_query.data.split(":")
        booking_id = sp[1]
        user_id = sp[2]# Получаем id бронирования из callback_query.data
        data['id'] = booking_id  # Сохраняем id бронирования в state для дальнейшего использования
        await confirm_booking(callback_query, booking_id,user_id)

