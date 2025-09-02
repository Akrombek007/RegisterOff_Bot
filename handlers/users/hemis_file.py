from utils.db_api.core import DatabaseService1
from file_service import hemis_file_path_
from aiogram.dispatcher import FSMContext
from LoggingService import LoggerService
from functools import wraps
from aiogram import types
from loader import dp
import logging
from keyboards.inline import hemis_keyboard, user_menu

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

HEMIS_INFO_MAP = {
"hemis_2": ("reyting", "HEMIS dasturidan reyting qaydonomasini olish"),
"hemis_3": ("Dars", "Dars jadvallari haqida ma'lumot olish"),
"hemis_4": ("nazorat", "Nazorat jadvallari haqida ma'lumot"),
"hemis_5": ("reja", "O‘quv rejasi haqida ma‘lumot"),
"hemis_6": ("resurs", "Fanlarning resurslari haqida ma‘lumot"),
"hemis_7": ("davomat", "Talabaning darslardan qoldirgan soatlari (davomat)"),
"hemis_8": ("buyruq", "Talabaning buyruqlari haqida ma‘lumot"),
"hemis_9": ("hemis_info", "Universitetda o'qiyotganligi to'g'risidagi ma'lumotnoma olish")
}

class HemisHandler:
    @staticmethod
    @dp.callback_query_handler(lambda c: c.data == "info_2")
    @handle_errors
    async def handle_main_menu(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.delete()
        await callback.message.answer("Siz Hemis tizimini tanladingiz \U0001F5A5", reply_markup=hemis_keyboard)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("hemis_"))
    @handle_errors
    async def handle_hemis_sections(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        info = HEMIS_INFO_MAP.get(data)
        folder_name, caption = info
        path_file = await hemis_file_path_(folder_name)

        for idx, path_ in enumerate(path_file, start=1):
            with open(path_, "rb") as photo:
                await callback.message.answer_photo(photo, caption=f"{idx}-rasm")

        await callback.message.answer('Xizmat turini tanlang:', reply_markup=user_menu)