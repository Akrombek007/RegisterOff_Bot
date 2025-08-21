from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.core import DatabaseService1, User
from data.config import engine, ADMIN_M1
from LoggingService import LoggerService
from keyboards .inline import keyboard
from aiogram.types import Message
from loader import dp

# logger = LoggerService().get_logger()
db = DatabaseService1(logger=LoggerService())


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    if str(message.from_user.id) in ['685098494', '1709066039', '5506760681']:
        await message.answer("Buyruqni yuboring! /hisobot")
    elif str(message.from_user.id) in '':
        await message.answer("Telegram kontaktangizni yuboring.", reply_markup=keyboard)