from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db_api.verification import VerificationService
from utils.db_api.core import DatabaseService1
from LoggingService import LoggerService
from loader import dp, bot
import logging

# Initialize services
db = DatabaseService1(logger=LoggerService())
verification_service = VerificationService(db)

@dp.callback_query_handler(lambda c: c.data.startswith(('verify_approve_', 'verify_reject_')))
async def handle_verification_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        # Parse the callback data
        action, request_id = callback.data.split('_', 2)[1:]
        request_id = int(request_id)
        
        # Get the verification request
        request = await verification_service.update_verification_status(
            request_id=request_id,
            status="approved" if action == "approve" else "rejected",
            admin_id=callback.from_user.id,
            comment=""  # You can add a comment field if needed
        )
        
        if not request:
            await callback.answer("❌ Xatolik yuz berdi. So'rov topilmadi.", show_alert=True)
            return
        
        # Prepare the response message
        status_text = "✅ Tasdiqlandi" if action == "approve" else "❌ Rad etildi"
        admin_mention = f"@{callback.from_user.username}" if callback.from_user.username else "Admin"
        
        # Update the original admin message
        try:
            await callback.message.edit_text(
                f"{status_text} by {admin_mention}\n\n" + callback.message.html_text,
                reply_markup=None
            )
        except Exception as e:
            logging.error(f"Error updating admin message: {e}")
        
        # Notify the user
        user_message = (
            f"🎉 Sizning HEMIS hisobingiz muvaffaqiyatli tasdiqlandi!\n\n"
            f"📇 JSHSHIR: {request.jshshir}\n"
            f"👤 Ism Familiya: {request.full_name}\n\n"
            "/start buyrug'i orqali bosh menyuga qayting."
        ) if action == "approve" else (
            f"❌ Sizning HEMIS hisobingiz tasdiqlanmadi.\n\n"
            "Iltimos, ma'lumotlaringizni tekshirib, qaytadan urinib ko'ring yoki "
            "administratorlar bilan bog'laning."
        )
        
        try:
            await bot.send_message(
                chat_id=request.user.telegram_id,
                text=user_message
            )
        except Exception as e:
            logging.error(f"Error notifying user {request.user.telegram_id}: {e}")
            # Try to send a message to the admin if user notification fails
            await callback.message.answer(
                f"⚠️ Foydalanuvchiga xabar yuborib bo'lmadi. "
                f"User ID: {request.user.telegram_id}"
            )
        
        await callback.answer(f"{status_text}!")
        
    except Exception as e:
        logging.exception("Error in handle_verification_callback")
        await callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.", show_alert=True)

# Command to list all pending verification requests
@dp.message_handler(commands=["verify_requests"], is_admin=True)
async def list_verification_requests(message: types.Message):
    """List all pending verification requests (admin only)"""
    requests = await verification_service.get_pending_requests()
    
    if not requests:
        await message.answer("⏳ Hozircha tasdiqlash so'rovlari mavjud emas.")
        return
    
    response = []
    for req in requests:
        response.append(
            f"🆔 {req.id}\n"
            f"👤 {req.full_name}\n"
            f"📇 JSHSHIR: {req.jshshir}\n"
            f"📅 {req.created_date} {req.created_time}\n"
            f"🔗 User ID: {req.user_id}"
        )
    
    # Split into multiple messages if too long
    current_msg = ""
    for req_text in response:
        if len(current_msg) + len(req_text) > 4000:  # Telegram message limit
            await message.answer(current_msg)
            current_msg = ""
        current_msg += f"\n\n{req_text}"
    
    if current_msg:
        await message.answer(f"⏳ Kutilayotgan tasdiqlash so'rovlari:\n{current_msg}")
