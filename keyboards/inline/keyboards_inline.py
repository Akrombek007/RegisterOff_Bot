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


langauage_keyboard = InlineKeyboardMarkup(row_width=3)
langauage_keyboard.add(
    InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="langauage_uz"),
    InlineKeyboardButton("🇷🇺 Rus tili", callback_data="langauage_ru"),
    InlineKeyboardButton("eng Ingliz tili", callback_data="langauage_eng"),
)

user_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Akademik faoliyat bo'yicha murojaatlar!", callback_data="info_1"),
    ],
    [
        InlineKeyboardButton(text="Hemis tizimi yuzasidan murojaatlar!", callback_data="info_2"),
    ],
    [
        InlineKeyboardButton(text="Fakeltet va turar joylarni manzili (lokatsiya)", callback_data="info_3"),
    ],
    [
        InlineKeyboardButton(text="To'lovlar masalasi bo'yicha murojaatlar!", callback_data="info_4"),
    ],
    [
        InlineKeyboardButton(text="Savol va takliflar bo'yicha adminga murojaat!", callback_data="info_5"),
    ]
])
'''

'''


contract_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Yangi o'quv yili uchun to'lov-shartnomasiga ariza berish va shartnoma olish", callback_data="contract_1")
    ],
    [
        InlineKeyboardButton(text="Talabalar turar joyiga ariza berish va shartnoma olish", callback_data="contract_2")
    ],
    [
        InlineKeyboardButton(text="Fanlardan qayta o‘qishga ariza berish va shartnoma olish", callback_data="contract_3")
    ],
    [
        InlineKeyboardButton(text="Stipendiya to’g’risida ma’lumot olish", callback_data="contract_4")
    ],
    [
        InlineKeyboardButton(text="Ijara shartnomasiga ariza berish", callback_data="contract_5")
    ],
    [
        InlineKeyboardButton(text="Ortiqcha to’lovni qaytarish bo’yicha (kantrakt, qayta o’qish, yotoqxona) ---> ariza example bilan qaysi xonaga uchrashliyligi", callback_data="contract_6")
    ],
    [
        InlineKeyboardButton(text="Ma’sul xodim bilan bog’lanish (Fakultet bo’yicha)", callback_data="contract_7")
    ]
])


faculty_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Aniq fanlar maktabi", callback_data="faculty_1")
    ],
    [
        InlineKeyboardButton(text="Tabiiy fanlar fakulteti", callback_data="faculty_2")
    ],
    [
        InlineKeyboardButton(text="Pedagogika psixologiya va inklyuziv ta’lim fakulteti ", callback_data="faculty_3")
    ],
    [
        InlineKeyboardButton(text="Filologiya fakulteti", callback_data="faculty_4"),
    ],
    [
        InlineKeyboardButton(text='Maktabgacha va boshlang‘ich ta’lim fakulteti', callback_data="faculty_5")
    ],
    [
        InlineKeyboardButton(text='Professional ta’lim va san’at fakulteti', callback_data="faculty_6")
    ],
    [
        InlineKeyboardButton(text='Tarix fakulteti', callback_data="faculty_7")
    ],
    [
        InlineKeyboardButton(text='Harbiy ta’lim fakulteti', callback_data="faculty_8")
    ],
    [
        InlineKeyboardButton(text='Innovatsion pedagogika o‘zbek-belarus qo‘shma fakulteti', callback_data="faculty_9")
    ]
])


hemis_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="HEMIS login parollarini qayta tiklab berish", callback_data="hemis_1")
    ],
    [
        InlineKeyboardButton(text="HEMIS dasturidan reyting qaydonomasini olish", callback_data="hemis_2")
    ],
    [
        InlineKeyboardButton(text="Dars jadvallari haqida ma'lumot olish", callback_data="hemis_3")
    ],
    [
        InlineKeyboardButton(text="Nazorat jadvallari haqida ma'lumot", callback_data="hemis_4")
    ],
    [
        InlineKeyboardButton(text="O‘quv rejasi haqida ma‘lumot", callback_data="hemis_5")
    ],
    [
        InlineKeyboardButton(text="Fanlarning resurslari haqida ma‘lumot", callback_data="hemis_6")
    ],
    [
        InlineKeyboardButton(text="Talabaning darslardan qoldirgan soatlari (davomat)", callback_data="hemis_7")
    ],
    [
        InlineKeyboardButton(text="Talabaning buyruqlari haqida ma‘lumot", callback_data="hemis_8")
    ],
    [
        InlineKeyboardButton(text="Universitetda o'qiyotganligi to'g'risidagi ma'lumotnoma olish", callback_data="hemis_9")
    ],
    [
        InlineKeyboardButton(text="Bitiruv varoq'ini olish (bitiruvchilar)", callback_data="hemis_10")
    ],
    [
        InlineKeyboardButton(text="Chaqiruv qog’ozini yuklab olish (sirtqi)", callback_data="hemis_11")
    ],
    [
        InlineKeyboardButton(text=" Ma’sul xodim bilan bog’lanish (Fakultet bo’yicha", callback_data="hemis_12")
    ]
])


akademik_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="O'zbekistondagi xorijiy va nodavlat OTMlardan o'qishni ko'chirish bo'yicha murojaatlar!",
            callback_data="akademik_1")
    ],
    [
        InlineKeyboardButton(text="Xorijdan o'qishni ko'chirish bo'yicha murojaatlar!", callback_data="akademik_2")
    ],
    [
        InlineKeyboardButton(text="Grandlar va tanlovlar haqida ma'lumotlar!", callback_data="akademik_3")
    ],
    [
        InlineKeyboardButton(text="Ilmiy konferensiyalar haqida ma'lumotlar!", callback_data="akademik_4")
    ],
    [
        InlineKeyboardButton(text="Innovatsion g'oya va startaplarga ro'yxatdan o'tish haqida ma'lumotlar!", callback_data="akademik_5")
    ],
    [
        InlineKeyboardButton(text="Nomli va nizomiy atoqli olimlari stipendiyalari haqida ma'lumot!", callback_data="akademik_6")
    ],
    [
        InlineKeyboardButton(text="Universitetga ikkinchi ta'lim shakliga o'qishga topshirish!", callback_data="akademik_7")
    ],
    [
        InlineKeyboardButton(text="Magistraturaga o'qishga hujjat topshirish!", callback_data="akademik_8")
    ],
    [
        InlineKeyboardButton(text="Qo'shma ta'limga hujjat topshirish (innovatsion pedagog)!", callback_data="akademik_9")
    ],
    [
        InlineKeyboardButton(text="Ma'sul xodim bilan bog'lanish!", callback_data="akademik_10")
    ]
]
)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = KeyboardButton(text="📞 Telefon raqamingizni yuboring", request_contact=True)
keyboard.add(button)

admins_message = InlineKeyboardMarkup(row_width=1)
admins_message.add(InlineKeyboardButton(text="Ma'sul xodim bilan bog'lanish", callback_data="admins_message"))
