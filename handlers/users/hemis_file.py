from utils.db_api.core import DatabaseService1, User
from file_service import hemis_file_path_
from aiogram.dispatcher import FSMContext
from LoggingService import LoggerService
from functools import wraps
from aiogram import types
from loader import dp
import logging
from keyboards.inline import hemis_keyboard
from os import path

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

async def hemis_file_func(callback: types.CallbackQuery):
    images = ["uz_01.png", "uz_02.png", "uz_03.png", "uz_04.png"]
    for img in images:
        path_file = hemis_file_path_(img)
        if path.exists(path):
            with open(path_file, "rb") as photo:
                await callback.message.answer_photo(photo)
        else:
            await callback.message.answer(f"❌ {img} topilmadi")

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


class HemisHandler:
    @staticmethod
    @dp.callback_query_handler(lambda c: c.data == "info_2")
    @handle_errors
    async def hemis_func(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("Siz Hemis tizimini tanladingiz 🖥", reply_markup=hemis_keyboard)


    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("hemis_"))
    @handle_errors
    async def hemis_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        if callback.data == "hemis_1":
            await callback.message.answer(
                "HEMIS login parolni qayta tiklash uchun jshshir va Ism Familiyangizni to'liq kiriting!")
        elif callback.data == "hemis_2":
            path_file = await hemis_file_path_("reyting")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("HEMIS dasturidan reyting qaydonomasini olish")
        elif callback.data == "hemis_3":
            path_file = await hemis_file_path_("Dars")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Dars jadvallari haqida ma'lumot olish")
        elif callback.data == "hemis_4":
            path_file = await hemis_file_path_("nazorat")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Nazorat jadvallari haqida ma'lumot")
        elif callback.data == "hemis_5":
            path_file = await hemis_file_path_("reja")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("O‘quv rejasi haqida ma‘lumot")
        elif callback.data == "hemis_6":
            path_file = await hemis_file_path_("resurs")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Fanlarning resurslari haqida ma‘lumot")
        elif callback.data == "hemis_7":
            path_file = await hemis_file_path_("davomat")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Talabaning darslardan qoldirgan soatlari (davomat)")
        elif callback.data == "hemis_8":
            path_file = await hemis_file_path_("buyruq")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Talabaning buyruqlari haqida ma‘lumot")
        elif callback.data == "hemis_9":
            path_file = await hemis_file_path_("hemis_info")
            number = 1
            for path_ in path_file:
                with open(path_, "rb") as photo:
                    await callback.message.answer_photo(photo, caption=f"{number}-rasm")
                number += 1
            await callback.message.answer("Universitetda o'qiyotganligi to'g'risidagi ma'lumotnoma olish")
        # elif callback.data == "hemis_10":
        #     path_file = await hemis_file_path_("reyting")
        #     number = 1
        #     for path_ in path_file:
        #         with open(path_, "rb") as photo:
        #             await callback.message.answer_photo(photo, caption=f"{number}-rasm")
        #         number += 1
        #     await callback.message.answer("Bitiruv varoq'ini olish (bitiruvchilar)")
        # elif callback.data == "hemis_11":
        #     await callback.message.answer("Chaqiruv qog’ozini yuklab olish (sirtqi)")
        # elif callback.data == "hemis_12":
        #     await callback.message.answer("Ma’sul xodim bilan bog’lanish (Fakultet bo’yicha)")

