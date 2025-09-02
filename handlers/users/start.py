from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.core import DatabaseService1, User
from data.config import engine, ADMIN_M1
from LoggingService import LoggerService
from keyboards .inline import langauage_keyboard
from aiogram.types import Message
from loader import dp

# logger = LoggerService().get_logger()
db = DatabaseService1(logger=LoggerService())


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    if str(message.from_user.id) in ['685098494', '170906603912', '5506760681']:
        await message.answer("Buyruqni yuboring! /hisobot")
    elif str(message.from_user.id) not in '':
        await message.delete()
        await message.answer("Tilni tanlang!", reply_markup=langauage_keyboard)