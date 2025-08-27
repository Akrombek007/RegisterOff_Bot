import re
def validate_jshshir_fullname(text: str) -> tuple[bool, str]:
    """
    JSHSHIR + ism familiya tekshiruv funksiyasi.
    Format: 14 xonali JSHSHIR + bitta oraliq + Ism Familiya (lotin harflarida)
    """
    parts = text.strip().split(" ", 1)

    if len(parts) < 2:
        return False, "❌ Iltimos, JSHSHIR va ism familiyangizni to‘liq kiriting."

    jshshir, full_name = parts
    if not re.fullmatch(r"\d{14}", jshshir):
        return False, "❌ JSHSHIR 14 ta raqamdan iborat bo‘lishi kerak."

    if not re.fullmatch(r"[A-Za-z‘ʼʼʻ\s\-]{3,}", full_name):
        return False, "❌ Ism familiya faqat lotin harflarida va to‘liq yozilishi kerak."

    return True, ""