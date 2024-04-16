from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.handlers.main_handler import *

class Human(StatesGroup):
    Name=State()
    Number=State()
    ChechNumber=State()

class Admin(StatesGroup):
    note=State()

class Guest(StatesGroup):
    Name=State()
    Number=State()

class RegularCustomer(StatesGroup):
    Name=State()
    Number=State()








