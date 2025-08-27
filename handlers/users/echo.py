from aiogram.types import ContentType
from aiogram import types
from loader import dp

BLOCKED_TYPES = [
    ContentType.PHOTO,
    ContentType.DOCUMENT,
    ContentType.VIDEO,
    ContentType.AUDIO,
    ContentType.VOICE,
    ContentType.STICKER,
    ContentType.CONTACT,
    ContentType.LOCATION,
    ContentType.ANIMATION,
]

@dp.message_handler(content_types=BLOCKED_TYPES)
async def block_unexpected_files(message: types.Message):
    readable_type = {
        ContentType.PHOTO: "📷 rasm",
        ContentType.DOCUMENT: "📄 hujjat",
        ContentType.VIDEO: "🎥 video",
        ContentType.AUDIO: "🎵 audio",
        ContentType.VOICE: "🎙 ovozli xabar",
        ContentType.STICKER: "🔖 sticker",
        ContentType.CONTACT: "👤 kontakt",
        ContentType.LOCATION: "📍 joylashuv",
        ContentType.ANIMATION: "📹 gif"
    }.get(message.content_type, "❓ noma’lum fayl")

    await message.answer(
        f"Xurmatli {message.from_user.full_name}, siz ruxsat etilmagan ma'lumot yubordingiz: {readable_type}.\n"
        "Iltimos, matn shaklida ma'lumot yuboring yoki /start buyrug'ini bosing."
    )
