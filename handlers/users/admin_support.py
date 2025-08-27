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


# ✅ 2. Foydalanuvchi tomonidan yuborilgan JSHSHIR + Ism Familiya
@dp.message_handler(lambda msg: msg.reply_to_message is not None)
async def process_support_request(message: types.Message):
    # Kontekstni aniqlash: faqat HEMISga javobmi?
    if "HEMIS login parolni tiklash" not in message.reply_to_message.text:
        return
    user_telegram_id = str(message.from_user.id)
    user = await db.get(User, filters={'telegram_id': user_telegram_id})
    if not user:
        return await message.answer("❌ Siz tizimda ro‘yxatdan o‘tmagansiz.")

    support_id = await db.add(SupportRequest(
        user_id=user_telegram_id,
        admin_id=str(ADMIN_M2),
        question_text=message.text,
        feedback=False,
    ))

    if not support_id:
        return await message.answer("❌ Murojaat saqlanmadi. Iltimos, keyinroq urinib ko‘ring.")

    # Admin xabarini yuboramiz va message_id ni qaytarib olamiz
    try:
        admin_message = await dp.bot.send_message(
            chat_id=ADMIN_M2,
            text=(
                f"🆘 Yangi murojaat:\n"
                f"👤 Foydalanuvchi: {user[0].full_name} | ID: {user_telegram_id}\n"
                f"📥 Murojaat: {message.text}\n\n"
                f"🔁 Shu xabar ustiga reply qilib javob yuboring"
            )
        )

        # message_id ni saqlaymiz
        await db.update_by_field(
            model=SupportRequest,
            field_name="id",
            field_value=support_id,
            updates={"message_id": str(admin_message.message_id)}
        )

        await message.answer("✅ Murojaatingiz yuborildi. Admin tez orada siz bilan bog‘lanadi.")
    except Exception as e:
        logging.error(f"Xatolik admin xabarini yuborishda: {e}")
        await message.answer("❌ Xatolik yuz berdi. Keyinroq urinib ko‘ring.")


# ✅ 3. Admin javobi (/reply_ID javob matni)
@dp.message_handler(lambda msg: msg.reply_to_message is not None)
async def handle_admin_reply(message: types.Message):
    replied_msg_id = str(message.reply_to_message.message_id)

    support_list = await db.get(SupportRequest, filters={'message_id': replied_msg_id})
    if not support_list:
        return await message.answer("❌ Ushbu reply bog‘liq murojaat topilmadi.")

    support = support_list[0]

    user_list = await db.get(User, filters={'telegram_id': support.user_id})
    if not user_list:
        return await message.answer("❌ Foydalanuvchi topilmadi.")

    user = user_list[0]

    # Javobni yangilash
    await db.update_by_field(
        model=SupportRequest,
        field_name="id",
        field_value=support.id,
        updates={
            "answer_text": message.text,
            "admin_id": str(ADMIN_M2)
        }
    )

    await dp.bot.send_message(
        chat_id=user.telegram_id,
        text=f"✅ Admin javobi:\n{message.text}\nXizmat turini tanlang:", reply_markup=user_menu
    )
    await message.answer("✅ Javob foydalanuvchiga yuborildi.")


@dp.message_handler()
async def handle_unexpected_messages(message: types.Message):
    await message.reply(
        "❗ Iltimos, faqat ko‘rsatilgan formatda ma’lumot kiriting:\n"
        "`12345678901234 Ism Familiya`\n"
        "Yoki /start buyrug‘i orqali menyuga qayting."
    )
