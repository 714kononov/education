import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from bot.core.aiogram import dp

calendar_callback = CallbackData('btnChecDateForSchedule', 'act', 'year', 'month', 'day')

async def start_calendar(
    year: int = datetime.now().year,
    month: int = datetime.now().month
) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=7)
    now=datetime.now()
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(
        f"сегодня {datetime.strftime(now,'%d/%m/%Y')}",
        callback_data="IGNORE"
    ))

    inline_kb.row()
    for day in ["ПН", "ВТ", "Ср", "ЧТ", "ПТ", "СБ", "ВС"]:
        inline_kb.insert(InlineKeyboardButton(day, callback_data="DISABLED"))

    today = datetime.now()
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        inline_kb.row()
        for day in week:
            if day == 0:
                inline_kb.insert(InlineKeyboardButton(" ", callback_data="DISABLED"))
                continue
            date = datetime(year, month, day)
            if today <= date <= today + timedelta(days=30):
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=calendar_callback.new("DAY", year, month, day)
                ))
            else:
                inline_kb.insert(InlineKeyboardButton(" ", callback_data="DISABLED"))
    now_month=datetime.now()
    inline_kb.row()
    inline_kb.insert(InlineKeyboardButton(
        "▶️ Следующий месяц", callback_data=f'btnChecDateForSchedule:{datetime.strftime(now_month,"%d/%m/%Y")}:NEXT_MONTH'
    ))

    return inline_kb



