from utils.db_api.core import DatabaseService1, User, SupportRequest
from keyboards.inline import user_menu, validate_jshshir_fullname
from LoggingService import LoggerService
from data.config import ADMIN_M1
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

@dp.callback_query_handler(lambda c: c.data == "support_admin")
async def start_password_reset(callback: types.CallbackQuery):
    await callback.message.delete()
    data = await db.get(User, filters={'telegram_id': callback.from_user.id})
    print(data[0], data)
    # if data[0].faculty == '':
    #     return await callback.message.answer("❌ Siz tizimda ro‘yxatdan o‘tmagansiz.")
    await callback.message.answer(
        "🛠 Siz admin bilan bog‘lanishni tanladingiz.\n\n"
        "📌 *Eslatma:* Yozgan savollaringiz tizimda saqlanadi. "
        "Iltimos, odob doirasida muloqot qiling va muammoni aniq tushuntiring.\n\n"
        "⏳ *Javoblar adminlarning bandlik darajasiga qarab yuboriladi.*\n\n"
        "✍️ Endi savolingizni yuborishingiz mumkin.",
        parse_mode="Markdown"
    )

