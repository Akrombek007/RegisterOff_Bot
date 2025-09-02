from keyboards.inline import faculty_keyboard, location_keyboard, student_flat_keyboard
from aiogram.dispatcher import FSMContext
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


class LocationHandler:
    @staticmethod
    @dp.callback_query_handler(lambda c: c.data == "info_3")
    @handle_errors
    async def hemis_func(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("📍 Siz lokatsiyani tanladingiz", reply_markup=location_keyboard)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("location_"))
    @handle_errors
    async def location_faculty_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        if data == "location_one":
            await callback.message.answer("Fakultetlar manzili 📍", reply_markup=faculty_keyboard)
        elif data == "location_two":
            await callback.message.answer("Talabaning turar joy manzili 📍", reply_markup=student_flat_keyboard)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("faculty_"))
    @handle_errors
    async def faculty_location_func(callback: types.CallbackQuery, state: FSMContext):
        faculty_locations = {
            "faculty_1": {
                "title": "Quyidagi aniq fanlar maktabi joylashuvi",
                "coords": (41.2914297, 69.2550864)
            },
            "faculty_2": {
                "title": "Quyidagi tabiiy fanlar fakulteti joylashuvi",
                "coords": (41.2711424, 69.1885274)
            },
            "faculty_3": {
                "title": "Quyidagi Pedagogika psixologiya va inklyuziv ta’lim fakulteti joylashuvi",
                "coords": (41.2716659, 69.2057483)
            },
            "faculty_4": {
                "title": "Quyidagi Filologiya fakulteti joylashuvi",
                "coords": (41.2642537, 69.2307141)
            },
            "faculty_5": {
                "title": "Quyidagi Maktabgacha va boshlang‘ich ta’lim fakulteti joylashuvi",
                "coords": (41.2716659, 69.2057483)
            },
            "faculty_6": {
                "title": "Quyidagi Professional ta’lim va san’at fakulteti joylashuvi",
                "coords": (41.2914297, 69.2550864)
            },
            "faculty_7": {
                "title": "Quyidagi Tarix fakulteti joylashuvi",
                "coords": (41.2914297, 69.2550864)
            },
            "faculty_8": {
                "title": "Quyidagi Harbiy ta’lim fakulteti joylashuvi",
                "coords": (41.2415391, 69.3329777)
            },
            "faculty_9": {
                "title": "Quyidagi Innovatsion pedagogika qo‘shma ta'lim oliy maktabi fakulteti joylashuvi",
                "coords": (41.2716659, 69.2057483)
            }
        }

        key = callback.data
        info = faculty_locations.get(key)

        if info:
            await callback.message.answer(info["title"])
            lat, lon = info["coords"]
            await callback.message.answer_location(latitude=lat, longitude=lon)

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("flat_"))
    @handle_errors
    async def student_flat_func(callback: types.CallbackQuery, state: FSMContext):
        flat_locations = {
            "flat_1": {
                "title": "Quyidagi Oqtepa texnikumga tegishli talabalar turar joyi joylashuvi",
                "coords": (41.2987179, 69.2137509)
            },
            "flat_2": {
                "title": "Quyidagi 5-sonli talabalar turar joyi joylashuvi",
                "coords": (41.2849723, 69.2354544)
            },
            "flat_3": {
                "title": "Quyidagi 7-sonli talabalar turar joyi joylashuvi",
                "coords": (41.2849723, 69.2354544)
            },
            "flat_4": {
                "title": "Quyidagi 8-sonli talabalar turar joyi joylashuvi",
                "coords": (41.2849723, 69.2354544)
            },
            "flat_5": {
                "title": "Quyidagi 9-sonli talabalar turar joyi joylashuvi",
                "coords": (41.2849723, 69.2354544)
            },
            "flat_6": {
                "title": "Quyidagi 10-sonli talabalar turar joyi joylashuvi",
                "coords": (41.286967, 69.2255179)
            },
            "flat_7": {
                "title": "Quyidagi DXSH talabar turar joyi joylashuvi",
                "coords": (41.2642537, 69.2307141)
            }
        }
        key = callback.data
        info = flat_locations.get(key)

        if info:
            await callback.message.answer(info["title"])
            lat, lon = info["coords"]
            await callback.message.answer_location(latitude=lat, longitude=lon)
