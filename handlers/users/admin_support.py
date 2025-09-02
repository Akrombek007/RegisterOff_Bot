from datetime import datetime
from pytz import timezone
from utils.db_api.core import DatabaseService1, User, SupportRequest
from keyboards.inline import user_menu, validate_jshshir_fullname
from LoggingService import LoggerService
from data.config import ADMIN_M2
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


# ✅ 1. Hemis parol tiklashni boshlovchi tugma
@dp.callback_query_handler(lambda c: c.data == "hemis_1")
# @handle_errors
async def start_password_reset(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "HEMIS login parolni tiklash uchun JSHSHIR va Ism Familiyangizni to‘liq kiriting.\n"
        "(Masalan: 12345678901234 Anvarov Anvar)",
        reply_markup=types.ForceReply(selective=True)
    )


@dp.message_handler(lambda msg: msg.reply_to_message and "HEMIS login parolni tiklash" in msg.reply_to_message.text)
async def process_support_request(message: types.Message):
    user_telegram_id = str(message.from_user.id)

    user_list = await db.get(User, filters={'telegram_id': user_telegram_id})
    if not user_list:
        return await message.answer("❌ Siz tizimda ro‘yxatdan o‘tmagansiz.")

    user = user_list[0]

    # DBga yozamiz
    support_id = await db.add(SupportRequest(
        user_id=user_telegram_id,
        admin_id=str(ADMIN_M2),
        question_text=message.text,
        feedback=False
    ))

    if not support_id:
        return await message.answer("❌ Murojaat saqlanmadi. Keyinroq urinib ko‘ring.")

    # Admin'ga yuboramiz
    admin_msg = await dp.bot.send_message(
        chat_id=ADMIN_M2,
        text=(f"🆘 Yangi murojaat:\n"
              f"👤 {user.full_name} | ID: {user_telegram_id}\n"
              f"📥 {message.text}\n\n"
              f"✉️ Reply qilib javob yuboring.")
    )

    # adminning reply uchun message_id sini saqlaymiz
    await db.update_by_field(
        model=SupportRequest,
        field_name="id",
        field_value=support_id,
        updates={"message_id": str(admin_msg.message_id)}
    )
    await message.answer("✅ Murojaatingiz yuborildi. Admin tez orada siz bilan bog‘lanadi.")


# ✅ Admin reply xabari (faqat reply bo‘lsa va foydalanuvchi xabari ustiga yozilgan bo‘lsa)
@dp.message_handler(lambda msg: msg.reply_to_message is not None and msg.from_user.id == int(ADMIN_M2))
async def handle_admin_reply(message: types.Message):
    replied_id = str(message.reply_to_message.message_id)

    support_list = await db.get(SupportRequest, filters={'message_id': replied_id})
    if not support_list:
        return await message.answer("❌ Bu xabarga bog‘liq murojaat topilmadi.")

    support = support_list[0]

    user_list = await db.get(User, filters={'telegram_id': support.user_id})
    if not user_list:
        return await message.answer("❌ Foydalanuvchi topilmadi.")

    user = user_list[0]

    await db.update_by_field(
        model=SupportRequest,
        field_name="id",
        field_value=support.id,
        updates={
            "answer_text": message.text,
            "admin_id": str(ADMIN_M2),
            "end_date": str(datetime.now(timezone('Asia/Tashkent')).strftime("%Y-%m-%d")),
            "end_time": str(datetime.now(timezone('Asia/Tashkent')).strftime("%H:%M:%S"))
        }
    )

    await dp.bot.send_message(
        chat_id=user.telegram_id,
        text=f"✅ Admin javobi:\n{message.text}\nXizmat turini tanlang:",
        reply_markup=user_menu
    )

    await message.answer("✅ Javob foydalanuvchiga yuborildi.")
