from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

response_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ XA", callback_data="yes"),
    ],
    [
        InlineKeyboardButton(text="❌ Orqaga", callback_data="no"),
    ]
])

til_shakli_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="1"),
    ],
    [
        InlineKeyboardButton(text="🇷🇺 Rus tili", callback_data="2"),
    ],
    [
        InlineKeyboardButton(text="eng Ingliz tili", callback_data="3"),
    ]
])


async def keyboard_func(user_id, message, faculty):
    choose_admin = InlineKeyboardMarkup(row_width=2)
    approve_btn = InlineKeyboardButton("✅ Tasdiqlash",
                                       callback_data=f"approve_{user_id}_{message.message_id}_{faculty}")
    reject_btn = InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}_{message.message_id}_{faculty}")
    choose_admin.add(approve_btn, reject_btn)
    return choose_admin


keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = KeyboardButton(text="📞 Telefon raqamingizni yuboring", request_contact=True)
keyboard.add(button)
