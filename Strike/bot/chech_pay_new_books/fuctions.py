from datetime import datetime, timedelta
from bot.database.model import table1
import asyncio


async def delete_notpay_books():
    try:
        # Assuming that your model has a field 'pay'
        books = table1.select().where(table1.pay == "Не оплачено")
        print('Поиск не оплаченных бронирований')

        for book in books:
            time_now = datetime.now()
            current_time = time_now.strftime('%d/%m/%Y %H:%M')
            books_time = datetime.strptime(book.createTime, '%d/%m/%Y %H:%M')
            time_plus_15 = books_time + timedelta(minutes=15)

            if time_plus_15 < time_now:
                book.delete_instance()
    except table1.DoesNotExist:
        print('Не оплаченных бронирований нету')
        return 1


async def delete_not_pay():
    while True:
        await delete_notpay_books()
        await asyncio.sleep(60)


async def main_pay_or_not():
    await asyncio.create_task(delete_not_pay())
