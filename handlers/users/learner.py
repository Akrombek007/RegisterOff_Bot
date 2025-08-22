from keyboards.inline import keyboard, langauage_keyboard, user_menu, akademik_keyboard, hemis_keyboard, \
    faculty_keyboard, contract_keyboard, admins_message
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
        await message.answer("Xizmat turini tanlang:", reply_markup=user_menu)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("langauage_"))
    @handle_errors
    async def process_contact(message: types.Message, state: FSMContext):
        await message.answer("Xush kelibsiz! Xizmat turini tanlang:", reply_markup=user_menu)
        user_id = str(message.from_user.id)
        await db.add(User(
            telegram_id=user_id,
            username=message.from_user.username or "",
            telegram_name=message.from_user.full_name,
            status=False
        ))

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("user_"))
    @handle_errors
    async def info_1(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data.split("_")
        if data[1] == "info_1":
            await callback.message.answer("Akademik faoliyat bo'yicha murojaatlar!", reply_markup=akademik_keyboard)
        elif data[1] == "info_2":
            await callback.message.answer("Hemis tizimi yuzasidan murojaatlar!", reply_markup=hemis_keyboard)
        elif data[1] == "info_3":
            await callback.message.answer("Fakeltet va turar joylarni manzili (lokatsiya)",
                                          reply_markup=faculty_keyboard)
        elif data[1] == "info_4":
            await callback.message.answer("To'lovlar masalasi bo'yicha murojaatlar!", reply_markup=contract_keyboard)
        elif data[1] == "info_5":
            await callback.message.answer("Savol va takliflar bo'yicha adminga murojaat!", reply_markup=admins_message)


    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("akademik_"))
    @handle_errors
    async def akademik_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data.split("_")
        if data[1] == "akademik_1":
            await callback.message.answer("O'zbekistondagi xorijiy va nodavlat OTMlardan o'qishni ko'chirish bo'yicha murojaatlar!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_2":
            await callback.message.answer("Xorijiy OTMlardan o'qishni ko'chirish bo'yicha murojaatlar!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_3":
            await callback.message.answer("Grandlar va tanlovlar haqida ma'lumotlar!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_4":
            await callback.message.answer("Ilmiy konferensiyalar haqida ma'lumotlar!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_5":
            await callback.message.answer("Innovatsion g'oya va startaplarga ro'yxatdan o'tish haqida ma'lumotlar!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_6":
            await callback.message.answer("Nomli va nizomiy atoqli olimlari stipendiyalari haqida ma'lumot!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_7":
            await callback.message.answer("Universitetga ikkinchi ta'lim shakliga o'qishga topshirish!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_8":
            await callback.message.answer("Magistraturaga o'qishga hujjat topshirish!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_9":
            await callback.message.answer("Qo'shma ta'limga hujjat topshirish (innovatsion pedagog)!", reply_markup=akademik_keyboard)
        elif data[1] == "akademik_10":
            await callback.message.answer("Ma'sul xodim bilan bog'lanish!", reply_markup=akademik_keyboard)







