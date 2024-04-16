import types

from aiogram.dispatcher import FSMContext

from bot.core.aiogram import dp, bot
from bot.core.states import Admin, RegularCustomer
from bot.database.control import delete_from_admin, add_note_db, sale_db, add_regular_customer_to_db
from bot.menus.admin import get_booking_today, create_booking_keyboard, startadmin, yes_no, \
    show_all_bookings_with_notes, add_sale, show_all_bookings_with_sale


@dp.callback_query_handler(lambda c: c.data.startswith("btnAddNote"))
async def add_note(callback_query):
    await callback_query.answer()
    await show_all_bookings_with_notes(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith("btnSendNote"))
async def confirm_note(callback_query,state:FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['number_to_note'] = sp[1]
        await bot.send_message(callback_query.from_user.id, f"Введите заметку для записи №{data['number_to_note']}: ")
        await Admin.note.set()

@dp.message_handler(state=Admin.note)
async def confirm_note(message,state:FSMContext):
    async with state.proxy() as data:
        data["note"] = message.text
        print(f"Note: {message.text}")
        await add_note_db(message, data)
        await state.finish()


@dp.callback_query_handler(text="btnTodayBook")
async def booking_today(callback_query):
    await callback_query.answer()
    await get_booking_today(callback_query)


@dp.callback_query_handler(text="btnAllBook")
async def all_book(callback_query):
    await callback_query.answer()
    await create_booking_keyboard(callback_query, page_number=0)


@dp.callback_query_handler(lambda c: c.data.startswith("btnShowNext"))
async def show_next(callback_query):
    await callback_query.answer()
    sp = callback_query.data.split(":")
    next_page = int(sp[1])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await create_booking_keyboard(callback_query, next_page)

@dp.callback_query_handler(lambda c: c.data.startswith("btnConfirm"))
async def confirm_delete(callback_query):
    await callback_query.answer()
    print(callback_query.data)
    sp = callback_query.data.split(":")
    number_delete = sp[1]
    await yes_no(callback_query, number_delete)

@dp.callback_query_handler(lambda c: c.data.startswith("btnDeleteAdmin"))
async def delete_admin(callback_query):
    await callback_query.answer()
    print(callback_query.data)
    sp = callback_query.data.split(":")
    number_delete = sp[1]
    await delete_from_admin(callback_query, number_delete)

@dp.callback_query_handler(text="btnMainAdmin")
async def go_main(callback_query):
    await callback_query.answer()
    await startadmin(callback_query)

@dp.callback_query_handler(text='btnSale')
async def sale_for_user(callback_query, state:FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        await show_all_bookings_with_sale(callback_query)

@dp.callback_query_handler(lambda c: c.data.startswith("btnSaleConfirm"))
async def sale_save_data(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        data['id_to_sale'] = sp [1]
        await add_sale(callback_query)


@dp.callback_query_handler(lambda c: c.data.startswith("btnSale"))
async def sale_save_db(callback_query,state: FSMContext):
    await callback_query.answer()
    async with state.proxy() as data:
        print(callback_query.data)
        sp = callback_query.data.split(":")
        if sp[1]=="День рождения":
            data['sale']=1
            print(data['sale'])
        if sp[1]=="Студент":
            data['sale']=2
            print(data['sale'])
        if sp[1]=="Пенсионер":
            data['sale']=3
            print(data['sale'])
        await sale_db(callback_query,data)



@dp.callback_query_handler(lambda c: c.data.startswith('btnRegularCustomer'))
async def add_Regular_Customer(callback_query):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, text='Введите имя постоянного клиента: ')
    await RegularCustomer.Name.set()

@dp.message_handler(state=RegularCustomer.Name)
async def add_Regular_Customer_name(message, state: FSMContext):
    async with state.proxy() as data:
        print(f'Имя: {message.text}')
        data['regular_name'] = message.text
        await bot.send_message(message.from_user.id, text='Введите номер телефона постоянного клиента: ')
        await RegularCustomer.Number.set()

@dp.message_handler(state=RegularCustomer.Number)
async def add_Regular_Customer_number(message, state: FSMContext):
    async with state.proxy() as data:
        print(f'Номер телефона: {message.text}')
        data['regular_number'] = message.text
        await add_regular_customer_to_db(message, data)
        await state.finish()
        await startadmin(message)


