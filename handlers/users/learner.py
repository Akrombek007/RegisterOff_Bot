from utils.db_api.core import DatabaseService1, User
from data.config import ADMIN_M2, DATABASE_URL
from aiogram.dispatcher import FSMContext
from LoggingService import LoggerService
from states.button import Learning
from datetime import datetime
from functools import wraps
from asyncio import sleep
from aiogram import types
from loader import dp
from re import match
import logging
import re


# Fayl junatishni bloklash uchun handler
dp.message_handler(content_types=[types.ContentType.DOCUMENT,
                                  types.ContentType.PHOTO,
                                  types.ContentType.VIDEO,
                                  types.ContentType.AUDIO,
                                  types.ContentType.VOICE,
                                  types.ContentType.VIDEO_NOTE])


async def block_file_upload(message: types.Message):
    await message.answer(
        "❌ Fayl yuborish imkoniyati o'chirilgan.\nBotga fayl yuborish mumkin emas.\nIltimos, /start buyruqini yuboring.")
    return False  # Handler chain'ni to'xtatish uchun


# Logging config
logging.basicConfig(
    filename='bot.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# logger = LoggerService().get_logger()
db = DatabaseService1(logger=LoggerService())


def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Xatolik: {func.__name__}: {e}")
            if isinstance(args[0], types.CallbackQuery):
                await args[0].answer("❌ Xatolik yuz berdi. Qaytadan urinib ko‘ring.")
            elif isinstance(args[0], types.Message):
                await args[0].answer("❌ Noto‘g‘ri amal. Qaytadan urinib ko‘ring.")
            return None

    return wrapper


class BotHandler:
    @staticmethod
    @dp.message_handler(commands=["start"])
    @handle_errors
    async def start(message: types.Message, state: FSMContext):
        await state.reset_state(with_data=True)
        await message.answer("Xizmat turini tanlang:")

    @staticmethod
    @dp.message_handler(content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
    @handle_errors
    async def process_contact(message: types.Message, state: FSMContext):
        if message.content_type != types.ContentType.CONTACT:
            await message.answer("❗ Iltimos, tugma orqali kontakt yuboring.")
            return
        user_id = str(message.from_user.id)
        contact = message.contact
        if await db.get(User, filters={'telegram_id': user_id}):
            await message.answer("✅ Siz ro'yxatdan o'tgansiz. Xizmat turini tanlang:")
        elif contact.user_id == message.from_user.id:
            await db.add(User(
                telegram_id=user_id,
                username=message.from_user.username or "",
                telegram_name=message.from_user.full_name,
                telegram_number=contact.phone_number,
                status=False,
                test_point='1'
            )
            )  # Sevimli , Mening yurtim,
            await state.update_data({"telegram_number": contact.phone_number})
            await message.answer("Xizmat turini tanlang:")
        else:
            await message.answer("❌ Bu kontakt sizga tegishli emas. Iltimos, o‘z kontaktingizni yuboring.")

