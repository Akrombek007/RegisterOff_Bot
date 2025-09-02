from utils.db_api.core import DatabaseService1, User, SupportRequest
from keyboards.inline import faculty_keyboard, user_menu
from aiogram.dispatcher import FSMContext
from LoggingService import LoggerService
from datetime import datetime
from functools import wraps
from aiogram import types
from pytz import timezone
from data.config import *
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


# === Faculty to admin mapping ===
FACULTY_ADMIN_MAP = {
    'faculty_1': ADMIN_ANIQ_HARBIY,
    'faculty_2': ADMIN_TABIIY_MAGISTR,
    'faculty_3': ADMIN_PED_PSIX,
    "faculty_4": ADMIN_INO_FILOLOG,
    'faculty_5': ADMIN_MAKTABGACHA_BOSHLANGICH,
    'faculty_6': ADMIN_PROF_T,
    'faculty_7': ADMIN_PROF_T,
    'faculty_8': ADMIN_ANIQ_HARBIY,
    'faculty_9': ADMIN_INO_FILOLOG,
}
ADMIN_ALL_IDS = [ADMIN_INO_FILOLOG, ADMIN_TABIIY_MAGISTR, ADMIN_MAKTABGACHA_BOSHLANGICH, ADMIN_PROF_T, ADMIN_M1,
                 ADMIN_PED_PSIX, ADMIN_ANIQ_HARBIY]


# === 1. Admin bilan bog'lanish ===
@dp.callback_query_handler(lambda c: c.data == "support_admin")
async def support_entry(callback: types.CallbackQuery):
    await callback.message.delete()
    user_id = str(callback.from_user.id)
    user = await db.get(User, filters={"telegram_id": user_id})

    if not user:
        return await callback.message.answer("❌ Tizimda ro‘yxatdan o‘tmagansiz.")

    user = user[0]
    if not user.faculty:
        await callback.message.answer("Iltimos, avval fakultetingizni tanlang:", reply_markup=faculty_keyboard)
    else:
        await callback.message.answer(
            text=(
                "🛠 Siz admin bilan bog‘lanishni tanladingiz.\n\n"
                "📌 *Eslatma:* Yozgan savollaringiz tizimda saqlanadi. "
                "Iltimos, odob doirasida muloqot qiling va muammoni aniq tushuntiring.\n\n"
                "⏳ *Javoblar adminlarning bandlik darajasiga qarab yuboriladi.*\n\n"
                "✍️ Endi savolingizni yuborishingiz mumkin."
            ),
            parse_mode="Markdown",
            reply_markup=types.ForceReply(selective=True)
        )


# === 2. Fakultetni tanlaganida saqlash ===
@dp.callback_query_handler(lambda c: c.data.startswith("faculty_"))
async def set_faculty(callback: types.CallbackQuery):
    faculty_name = callback.data.replace("faculty_", "")
    await db.update_by_field(
        model=User,
        field_name="telegram_id",
        field_value=str(callback.from_user.id),
        updates={"faculty": f"faculty_{faculty_name}"}
    )
    await callback.message.edit_text(f"✅ {faculty_name} fakulteti tanlandi.")

    await callback.message.answer(
        text=(
            "🛠 Siz admin bilan bog‘lanishni tanladingiz.\n\n"
            "📌 *Eslatma:* Yozgan savollaringiz tizimda saqlanadi. "
            "Iltimos, odob doirasida muloqot qiling va muammoni aniq tushuntiring.\n\n"
            "⏳ *Javoblar adminlarning bandlik darajasiga qarab yuboriladi.*\n\n"
            "✍️ Endi savolingizni yuborishingiz mumkin."
        ),
        parse_mode="Markdown",
        reply_markup=types.ForceReply(selective=True)
    )


# === 3. Foydalanuvchi savolini qabul qilish ===
@dp.message_handler(
    lambda msg: msg.reply_to_message and "admin bilan bog‘lanishni tanladingiz" in msg.reply_to_message.text)
async def handle_support_message(message: types.Message):
    user_id = str(message.from_user.id)
    user = await db.get(User, filters={"telegram_id": user_id})

    if not user:
        return await message.answer("❌ Siz tizimda ro‘yxatdan o‘tmagansiz.")

    user = user[0]
    faculty = user.faculty
    if not faculty or faculty not in FACULTY_ADMIN_MAP:
        return await message.answer("❌ Fakultet aniqlanmadi yoki noto‘g‘ri. /start orqali qaytadan urinib ko‘ring.")

    admin_id = FACULTY_ADMIN_MAP[faculty]

    # Saqlash
    support_id = await db.add(SupportRequest(
        user_id=user_id,
        admin_id=admin_id,
        question_text=message.text,
        feedback=False
    ))

    if not support_id:
        return await message.answer("❌ Savolingiz saqlanmadi. Keyinroq urinib ko‘ring.")

    admin_msg = await dp.bot.send_message(
        chat_id=admin_id,
        text=(
            f"📨 Yangi savol ({faculty}):\n"
            f"👤 {user.full_name} | ID: {user_id}\n"
            f"💬 {message.text}\n\n"
            f"🔁 Savolga javob yozish uchun reply qiling."
        )
    )

    await db.update_by_field(
        model=SupportRequest,
        field_name="id",
        field_value=support_id,
        updates={"message_id": str(admin_msg.message_id)}
    )

    await message.answer("✅ Savolingiz yuborildi. Admin imkon qadar tez javob beradi.")


# ✅ Admin reply handler — har bir admin o‘z fakultetiga tegishli foydalanuvchiga javob beradi
@dp.message_handler(lambda msg: msg.reply_to_message is not None and str(msg.chat.id) in ADMIN_ALL_IDS)
async def handle_admin_reply(message: types.Message):
    replied_msg_id = str(message.reply_to_message.message_id)
    print(replied_msg_id)
    # Murojaatni aniqlash (message_id orqali)
    support_list = await db.get(SupportRequest, filters={'message_id': replied_msg_id})
    print(support_list)
    if not support_list:
        return await message.answer("❌ Bu xabarga bog‘liq murojaat topilmadi.")
    support = support_list[0]

    # Foydalanuvchini aniqlash
    user_list = await db.get(User, filters={'telegram_id': support.user_id})
    if not user_list:
        return await message.answer("❌ Foydalanuvchi topilmadi.")

    user = user_list[0]

    # Murojaatga javobni DB'ga yozish
    await db.update_by_field(
        model=SupportRequest,
        field_name="id",
        field_value=support.id,
        updates={
            "answer_text": message.text,
            "admin_id": str(message.from_user.id),
            "end_date": str(datetime.now(timezone('Asia/Tashkent')).strftime("%Y-%m-%d")),
            "end_time": str(datetime.now(timezone('Asia/Tashkent')).strftime("%H:%M:%S"))
        }
    )

    # Foydalanuvchiga yuborish
    try:
        await dp.bot.send_message(
            chat_id=user.telegram_id,
            text=(
                f"✅ Sizning murojaatingizga javob berildi:\n"
                f"{message.text}\n\n"
                f"⬇️ Quyidagi menyudan xizmatni tanlang:"
            ),
            reply_markup=user_menu)
        await message.answer("✅ Javob foydalanuvchiga yuborildi.")
    except Exception as e:
        logging.error(f"Javob yuborishda xatolik: {e}")
        await message.answer("❌ Javob yuborilmadi. Foydalanuvchi bilan aloqa uzilgan bo‘lishi mumkin.")
