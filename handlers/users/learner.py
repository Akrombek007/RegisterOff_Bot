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


class BotHandler:
    @staticmethod
    @dp.message_handler(commands=["start"])
    @handle_errors
    async def start(message: types.Message, state: FSMContext):
        await state.reset_state(with_data=True)
        await message.answer("Xizmat turini tanlang:", reply_markup=user_menu)
        await db.add(User(
            username=message.from_user.username,
            telegram_number='',
            telegram_id=message.from_user.id,
            telegram_name=message.from_user.first_name
        ))

    @staticmethod
    @dp.callback_query_handler(lambda c: c.data.startswith("langauage_"))
    @handle_errors
    async def process_contact(callback_query: types.CallbackQuery, state: FSMContext):
        await callback_query.message.delete()
        await callback_query.message.answer("Xush kelibsiz! Xizmat turini tanlang:", reply_markup=user_menu)
        if not await db.get(User, filters={'telegram_id': str(callback_query.from_user.id)}):
            await db.add(User(
                username=callback_query.from_user.username or '',
                telegram_number='',
                telegram_id=f'{callback_query.from_user.id}',
                telegram_name=callback_query.from_user.full_name
            ))
