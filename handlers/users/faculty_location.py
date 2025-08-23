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
        data = callback.data
        if callback.data == "faculty_1":
            await callback.message.answer("Quyidagi aniq fanlar maktabi joylashuvi")
        elif callback.data == "faculty_2":
            await callback.message.answer("Quyidagi tabiiy fanlar fakulteti joylashuvi")
        elif callback.data == "faculty_3":
            await callback.message.answer("Quyidagi Pedagogika psixologiya va inklyuziv ta’lim fakulteti joylashuvi")
        elif callback.data == "faculty_4":
            await callback.message.answer("Quyidagi Filologiya fakulteti joylashuvi")
        elif callback.data == "faculty_5":
            await callback.message.answer("Quyidagi Maktabgacha va boshlang‘ich ta’lim fakulteti joylashuvi")
        elif callback.data == "faculty_6":
            await callback.message.answer("Quyidagi Professional ta’lim va san’at fakulteti joylashuvi")
        elif callback.data == "faculty_7":
            await callback.message.answer("Quyidagi Tarix fakulteti joylashuvi")
        elif callback.data == "faculty_8":
            await callback.message.answer("Quyidagi Harbiy ta’lim fakulteti joylashuvi")
        elif callback.data == "faculty_9":
            await callback.message.answer(
                "Quyidagi Innovatsion pedagogika qo‘shma ta'lim oliy maktabi fakulteti joylashuvi")

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("flat_"))
    @handle_errors
    async def student_flat_func(callback: types.CallbackQuery, state: FSMContext):
        data = callback.data
        if callback.data == "flat_1":
            await callback.message.answer("Quyidagi Oqtepa texnikumga tegishli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_2":
            await callback.message.answer("Quyidagi 5-sonli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_3":
            await callback.message.answer("Quyidagi 7-sonli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_4":
            await callback.message.answer("Quyidagi 8-sonli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_5":
            await callback.message.answer("Quyidagi 9-sonli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_6":
            await callback.message.answer("Quyidagi 10-sonli talabalar turar joyi joylashuvi")
        elif callback.data == "flat_7":
            await callback.message.answer("Quyidagi DXSH talabar turar joyi joylashuvi")
