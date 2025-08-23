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


class PaymentHandler:
    @staticmethod
    @dp.callback_query_handler(lambda c: c.data == "info_4")
    @handle_errors
    async def payment_func(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Kerakli xizma turini tanlang:", reply_markup=contract_keyboard)


    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("contract_"))
    @handle_errors
    async def payment_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        if callback.data == "contract_1":
            await callback.message.answer("To'lovni qabul qilish")
        elif callback.data == "contract_2":
            await callback.message.answer("Talabalar turar joyiga ariza berish va shartnoma olish")
        elif callback.data == "contract_3":
            await callback.message.answer("Fanlardan qayta o‘qishga ariza berish va shartnoma olish")
        elif callback.data == "contract_4":
            await callback.message.answer("Stipendiya to’g’risida ma’lumot olish")
        elif callback.data == "contract_5":
            await callback.message.answer("Ijara shartnomasiga ariza berish")
        elif callback.data == "contract_6":
            await callback.message.answer("Ortiqcha to’lovni qaytarish bo’yicha (kantrakt, qayta o’qish, yotoqxona)")
        elif callback.data == "contract_7":
            await callback.message.answer("Ma’sul xodim bilan bog’lanish")





