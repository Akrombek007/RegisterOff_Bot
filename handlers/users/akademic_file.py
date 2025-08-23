from keyboards.inline import langauage_keyboard, user_menu, akademik_keyboard, hemis_keyboard, \
    faculty_keyboard, contract_keyboard, admins_message, location_keyboard, student_flat_keyboard
from utils.db_api.core import DatabaseService1, User
from aiogram.dispatcher import FSMContext
from LoggingService import LoggerService
from functools import wraps
from aiogram import types
from loader import dp
import logging

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


class AkademikHandler:
    @staticmethod
    @dp.callback_query_handler(lambda c: c.data == "info_1")
    @handle_errors
    async def akademik_func(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Siz akademik faoliyatni tanladingiz 📚", reply_markup=akademik_keyboard)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("akademik_"))
    @handle_errors
    async def akademik_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        print(data)
        if data == "akademik_1":
            await callback.message.answer(
                "O'zbekistondagi xorijiy va nodavlat OTMlardan o'qishni ko'chirish bo'yicha murojaatlar!",
                reply_markup=akademik_keyboard)
        elif data == "akademik_2":
            await callback.message.answer("Xorijiy OTMlardan o'qishni ko'chirish bo'yicha murojaatlar!",
                                          reply_markup=akademik_keyboard)
        elif data == "akademik_3":
            await callback.message.answer("Grandlar va tanlovlar haqida ma'lumotlar!", reply_markup=akademik_keyboard)
        elif data == "akademik_4":
            await callback.message.answer("Ilmiy konferensiyalar haqida ma'lumotlar!", reply_markup=akademik_keyboard)
        elif data == "akademik_5":
            await callback.message.answer("Innovatsion g'oya va startaplarga ro'yxatdan o'tish haqida ma'lumotlar!",
                                          reply_markup=akademik_keyboard)
        elif data == "akademik_6":
            await callback.message.answer("Nomli va nizomiy atoqli olimlari stipendiyalari haqida ma'lumot!",
                                          reply_markup=akademik_keyboard)
        elif data == "akademik_7":
            await callback.message.answer("Universitetga ikkinchi ta'lim shakliga o'qishga topshirish!",
                                          reply_markup=akademik_keyboard)
        elif data == "akademik_8":
            await callback.message.answer("Magistraturaga o'qishga hujjat topshirish!", reply_markup=akademik_keyboard)
        elif data == "akademik_9":
            await callback.message.answer("Qo'shma ta'limga hujjat topshirish (innovatsion pedagog)!",
                                          reply_markup=akademik_keyboard)
        elif data == "akademik_10":
            await callback.message.answer("Ma'sul xodim bilan bog'lanish!", reply_markup=akademik_keyboard)
        await callback.answer()
